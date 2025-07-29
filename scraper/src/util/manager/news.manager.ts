import {
  Injectable,
  Logger,
  OnModuleDestroy,
  OnModuleInit,
} from "@nestjs/common";
import * as dayjs from "dayjs";
import * as utc from "dayjs/plugin/utc";
import * as timezone from "dayjs/plugin/timezone";
import puppeteer from "puppeteer";
import { NateNewsTitle, News } from "../type/news.type";
import { HttpService } from "@nestjs/axios";

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
      headless: false,
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-accelerated-2d-canvas",
        "--disable-gpu",
      ],
    });

    this.page = await this.browser.newPage();

    await this.page.setUserAgent(
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    );

    await this.page.setExtraHTTPHeaders({
      "Accept-Language": "en-US,en;q=0.9",
      Accept:
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
      Referer: "https://www.google.com/",
    });

    this.page.setDefaultNavigationTimeout(60000);
    await this.page.setRequestInterception(true);
    this.page.on("request", (req) => {
      const resourceType = req.resourceType();
      if (
        resourceType === "image" ||
        resourceType === "media" ||
        resourceType === "font"
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
      let current = dayjs(latestDate).add(1, "day");
      const today = dayjs().tz("Asia/Seoul");
      while (current <= today) {
        const year = current.format("YYYY");
        const month = current.format("MM");
        const day = current.format("DD");
        const url = [
          "https://securities.miraeasset.com/bbs/board/message/list.do?",
          "from=&categoryId=1578&selectedId=1578&searchType=2&searchText=",
          `&searchStartYear=${year}&searchStartMonth=${month}&searchStartDay=${day}`,
          `&searchEndYear=${year}&searchEndMonth=${month}&searchEndDay=${day}`,
        ].join("");
        console.log("url", url);
        await this.page.goto(url, {
          waitUntil: "networkidle2",
        });
        await new Promise((resolve) => setTimeout(resolve, 2000));

        // Find all handles for the target links
        const linkSelector = "td.left div.subject a";
        const linkHandles = await this.page.$$(linkSelector);
        let found = false;
        for (let i = 0; i < linkHandles.length; i++) {
          const handle = linkHandles[i];
          const text = await this.page.evaluate(
            (el) => el.textContent?.trim() || "",
            handle
          );
          if (text.includes("AI 데일리 글로벌 마켓 브리핑")) {
            found = true;
            await Promise.all([
              handle.click(),
              this.page.waitForNavigation({ waitUntil: "networkidle2" }),
            ]);
            await new Promise((resolve) => setTimeout(resolve, 2000));
            // Extract the content from the detail page
            const result = await this.page.evaluate(() => {
              const title =
                document
                  .querySelector("th.bbs_detailTitle h4")
                  ?.textContent?.trim() || "";
              const content =
                document.querySelector("td.bbs_detail_view")?.textContent || "";
              return {
                title,
                content,
                company: "miraeasset",
                keywords: "",
                link: window.location.href,
              };
            });
            results.push({
              ...result,
              date: current.format("YYYY-MM-DD"),
            });
            // Go back to the list page for next link (if any)
            await this.page.goBack({ waitUntil: "networkidle2" });
            await new Promise((resolve) => setTimeout(resolve, 2000));
          }
        }
        if (!found) {
          this.logger.log(
            `${current.format("YYYY-MM-DD")} No matching article found`
          );
        }
        current = current.add(1, "day");
      }
      return results;
    } catch (error) {
      this.logger.error(`크롤링 중 오류 발생: ${error.message}`);
      throw new Error(
        `미래에셋 데이터를 가져오는 중 오류가 발생했습니다: ${error.message}`
      );
    }
  }

  async loadNateNews(): Promise<News[]> {
    try {
      // const apiUrl = `${process.env.AI_ADMIN_URL}/news/miraeasset/latest`;
      // const response = await this.api.axiosRef.get(apiUrl);
      // const latestDate: string = response.data; // YYYY-MM-DD

      const results: News[] = [];
      // let current = dayjs(latestDate).add(1, 'day');
      let current = dayjs();
      // const today = dayjs().tz('Asia/Seoul');

      const titles: NateNewsTitle[] = [];
      let i = 1;
      while (true) {
        const url = `https://news.nate.com/subsection?cate=eco01&mid=n0305&type=c&date=${current.format("YYYYMMDD")}&page=${i}`;
        await this.page.goto(url, {
          waitUntil: "networkidle2",
        });
        await new Promise((resolve) => setTimeout(resolve, 2000));

        const checkSelector = ".mduNoList";
        const checkHandle = await this.page.$$(checkSelector);
        if (checkHandle.length > 0) {
          break;
        }

        const linkSelector = ".mduSubjectList div a";
        const linkHandles = await this.page.$$(linkSelector);

        for (let i = 0; i < linkHandles.length; i++) {
          const handle = linkHandles[i];
          const link = await this.page.evaluate(
            (el) => el.getAttribute("href") || "",
            handle
          );

          const title = await handle.evaluate(
            (el) =>
              el.querySelector("span.tb h2.tit")?.textContent?.trim() || ""
          );

          titles.push({ title, link });
        }
        console.log("page", i, "finished");
        i++;
      }

      console.log("titles", titles.length);

      return results;
    } catch (error) {
      this.logger.error(`크롤링 중 오류 발생: ${error.message}`);
      throw new Error(
        `네이트 뉴스 데이터를 가져오는 중 오류가 발생했습니다: ${error.message}`
      );
    }
  }
}
