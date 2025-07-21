import {
  Injectable,
  Logger,
  OnModuleDestroy,
  OnModuleInit,
} from '@nestjs/common';
import * as dayjs from 'dayjs';
import * as utc from 'dayjs/plugin/utc';
import * as timezone from 'dayjs/plugin/timezone';
import puppeteer from 'puppeteer';
import { News } from '../type/news.type';
import { HttpService } from '@nestjs/axios';

// Extend dayjs with plugins
dayjs.extend(utc);
dayjs.extend(timezone);

@Injectable()
export class NewsManager implements OnModuleDestroy, OnModuleInit {
  private readonly logger: Logger = new Logger(NewsManager.name);

  private browser;
  private page;

  constructor(private readonly api: HttpService) {}

  async onModuleInit(): Promise<any> {
    this.browser = await puppeteer.launch({
      pipe: true,
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--disable-gpu',
      ],
    });

    this.page = await this.browser.newPage();

    await this.page.setUserAgent(
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    );

    await this.page.setExtraHTTPHeaders({
      'Accept-Language': 'en-US,en;q=0.9',
      Accept:
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
      Referer: 'https://www.google.com/',
    });

    this.page.setDefaultNavigationTimeout(60000);
    await this.page.setRequestInterception(true);
    this.page.on('request', (req) => {
      const resourceType = req.resourceType();
      if (
        resourceType === 'image' ||
        resourceType === 'media' ||
        resourceType === 'font'
      ) {
        req.abort();
      } else {
        req.continue();
      }
    });
  }

  async onModuleDestroy(): Promise<any> {
    if (this.page) {
      await this.page.close();
    }
    if (this.browser) {
      await this.browser.close();
    }
  }

  async loadMiraeAssetNews(): Promise<News[]> {
    try {
      const apiUrl = `${process.env.AI_ADMIN_URL}/news/miraeasset/latest`;
      const response = await this.api.axiosRef.get(apiUrl);
      const latestDate: string = response.data; // YYYY-MM-DD

      const results: News[] = [];
      let current = dayjs(latestDate).add(1, 'day');
      const today = dayjs().tz('Asia/Seoul');
      while (current <= today) {
        const year = current.format('YYYY');
        const month = current.format('MM');
        const day = current.format('DD');
        const url = [
          'https://securities.miraeasset.com/bbs/board/message/list.do?',
          'from=&categoryId=1578&selectedId=1578&searchType=2&searchText=',
          `&searchStartYear=${year}&searchStartMonth=${month}&searchStartDay=${day}`,
          `&searchEndYear=${year}&searchEndMonth=${month}&searchEndDay=${day}`,
        ].join('');
        console.log('url', url);
        await this.page.goto(url, {
          waitUntil: 'networkidle2',
        });
        await new Promise((resolve) => setTimeout(resolve, 2000));

        // Find all handles for the target links
        const linkSelector = 'td.left div.subject a';
        const linkHandles = await this.page.$$(linkSelector);
        let found = false;
        for (let i = 0; i < linkHandles.length; i++) {
          const handle = linkHandles[i];
          const text = await this.page.evaluate(
            (el) => el.textContent?.trim() || '',
            handle,
          );
          if (text.includes('AI 데일리 글로벌 마켓 브리핑')) {
            found = true;
            await Promise.all([
              handle.click(),
              this.page.waitForNavigation({ waitUntil: 'networkidle2' }),
            ]);
            await new Promise((resolve) => setTimeout(resolve, 2000));
            // Extract the content from the detail page
            const result = await this.page.evaluate(() => {
              const title =
                document
                  .querySelector('th.bbs_detailTitle h4')
                  ?.textContent?.trim() || '';
              const content =
                document.querySelector('td.bbs_detail_view')?.textContent || '';
              return {
                title,
                content,
                company: 'miraeasset',
                keywords: '',
                link: window.location.href,
              };
            });
            results.push({
              ...result,
              date: current.format('YYYY-MM-DD'),
            });
            // Go back to the list page for next link (if any)
            await this.page.goBack({ waitUntil: 'networkidle2' });
            await new Promise((resolve) => setTimeout(resolve, 2000));
          }
        }
        if (!found) {
          this.logger.log(
            `${current.format('YYYY-MM-DD')} No matching article found`,
          );
        }
        current = current.add(1, 'day');
      }
      return results;
    } catch (error) {
      this.logger.error(`크롤링 중 오류 발생: ${error.message}`);
      throw new Error(
        `미래에셋 데이터를 가져오는 중 오류가 발생했습니다: ${error.message}`,
      );
    }
  }

  async loadFutureSnowNews(): Promise<News[]> {
    try {
      const apiUrl = `${process.env.AI_ADMIN_URL}/news/youtube_futuresnow/latest`;
      const response = await this.api.axiosRef.get(apiUrl);
      const latestDate: string = response.data; //YYYY-MM-DD
      await this.page.goto('https://www.youtube.com/@futuresnow/posts', {
        waitUntil: 'networkidle2',
      });

      await new Promise((resolve) => setTimeout(resolve, 2000));

      let results = [];
      let found = false;
      let scrollCount = 0;

      while (!found && scrollCount < 30) {
        console.log('scrollCount', scrollCount);
        results = await this.page.evaluate(() => {
          const elements = Array.from(
            document.querySelectorAll('ytd-backstage-post-thread-renderer'),
          );
          return elements
            .map((el) => {
              const contentElement = el.querySelector(
                'yt-formatted-string#content-text',
              );
              const postText = contentElement?.textContent?.trim() || '';

              // Extract date in YYYY년 MM월 DD일 format
              const datePattern =
                /【미국 증시 요약 ｜\s*(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일/;
              const dateMatch = postText.match(datePattern);

              // Format date as YYYY-MM-DD if found
              let formattedDate = '';
              if (dateMatch) {
                const year = dateMatch[1];
                const month = dateMatch[2].padStart(2, '0');
                const day = dateMatch[3].padStart(2, '0');
                formattedDate = `${year}-${month}-${day}`;
              } else {
                return null; // If it doesn't match our pattern, skip this post
              }

              return {
                content: postText,
                company: 'youtube_futuresnow',
                keywords: '',
                link: 'https://www.youtube.com/@futuresnow/community',
                date: formattedDate,
              };
            })
            .filter((x) => x !== null);
        });

        found = results.some((x) => x.date === latestDate);
        await this.page.mouse.wheel({ deltaY: 5000 });
        await new Promise((resolve) => setTimeout(resolve, 2000));

        scrollCount++;
      }
      console.log('results', results);
      results = results.filter((x) => dayjs(x.date).isAfter(dayjs(latestDate)));

      if (results.length === 0) {
        this.logger.log('No matching FutureSnow posts found');
        return null;
      }

      return results.map((x) => ({
        ...x,
        title: `【미국 증시 요약 ｜${dayjs(x.date).format('YYYY년 MM월 DD일')}】`,
      }));
    } catch (error) {
      this.logger.error(`크롤링 중 오류 발생: ${error.message}`);
      throw new Error(
        `퓨처스노우 데이터를 가져오는 중 오류가 발생했습니다: ${error.message}`,
      );
    }
  }

  async loadNewsToday(): Promise<News[]> {
    try {
      const apiUrl = `${process.env.AI_ADMIN_URL}/news/newstoday/latest`;
      const response = await this.api.axiosRef.get(apiUrl);
      const latestDate: string = response.data; // YYYY-MM-DD

      const results: News[] = [];

      let crawlCount = 0;

      let current = dayjs(latestDate).add(1, 'day');
      while (current <= dayjs() && crawlCount < 5) {
        const pageUrl = `https://futuresnow.gitbook.io/newstoday/${current.format('YYYY-MM-DD')}/news/today/bloomberg`;
        console.log('pageUrl', pageUrl);

        await this.page.goto(pageUrl, { waitUntil: 'networkidle2' });
        await new Promise((resolve) => setTimeout(resolve, 3000));

        // 무한 스크롤
        let lastHeight = await this.page.evaluate('document.body.scrollHeight');
        while (true) {
          await this.page.evaluate(
            'window.scrollTo(0, document.body.scrollHeight)',
          );
          await new Promise((resolve) => setTimeout(resolve, 1000));
          const newHeight = await this.page.evaluate(
            'document.body.scrollHeight',
          );
          if (newHeight === lastHeight) break;
          lastHeight = newHeight;
        }

        // h2, p 태그 추출 및 기사 파싱
        const articles = await this.page.evaluate(() => {
          const elements = Array.from(document.querySelectorAll('h2, p'));
          const articles: { title: string; content: string }[] = [];
          let article: { title: string | null; content: string[] } = {
            title: null,
            content: [],
          };

          for (const el of elements) {
            const tag = el.tagName.toLowerCase();
            const text = el.textContent?.trim() || '';
            if (!text) continue;
            if (tag === 'h2') {
              if (article.title && article.content.length) {
                articles.push({
                  title: article.title,
                  content: article.content.join('\n'),
                });
              }
              article = { title: text, content: [] };
            } else if (tag === 'p') {
              article.content.push(text);
            }
          }
          if (article.title && article.content.length) {
            articles.push({
              title: article.title,
              content: article.content.join('\n'),
            });
          }
          return articles;
        });

        // News 타입에 맞게 변환
        results.push(
          ...articles.map((a) => ({
            title: a.title,
            content: a.content,
            company: 'newstoday',
            keywords: '',
            link: pageUrl,
            date: current.format('YYYY-MM-DD'),
          })),
        );

        crawlCount++;

        current = current.add(1, 'day');
      }

      return results.filter((x) => x.title !== 'Page not found');
    } catch (error) {
      this.logger.error(`크롤링 중 오류 발생: ${error.message}`);
      throw new Error(
        `뉴스투데이 데이터를 가져오는 중 오류가 발생했습니다: ${error.message}`,
      );
    }
  }
}
