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
import * as cheerio from "cheerio";
import axios from "axios";
import * as iconv from "iconv-lite";

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
      let i = 0;
      while (current <= today && i++ < 10) {
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
                type: "miraeasset",
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
      const results: News[] = [];
      let current = dayjs();
      let start = dayjs("2025-05-01");
      let today = dayjs().tz("Asia/Seoul");
      let idx = 0;

      let pageNum = 1;

      // 페이지를 순차적으로 처리하면서 바로 제목과 링크 추출
      while (pageNum <= 2) {
        const url = `https://news.nate.com/subsection?cate=eco01&mid=n0305&type=c&date=${current.format("YYYYMMDD")}&page=${pageNum}`;
        const iconv = require("iconv-lite");

        try {
          const response = await this.api.axiosRef.get(url, {
            responseType: "arraybuffer",
            responseEncoding: "binary",
            headers: {
              "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
              "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
              Accept:
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
              Referer: "https://www.google.com/",
            },
          });

          const html = iconv.decode(Buffer.from(response.data), "EUC-KR");
          const $ = cheerio.load(html);
          const titles: NateNewsTitle[] = [];

          // 현재 페이지에서 바로 제목과 링크 추출
          $(".mduSubjectList div a").each((i, element) => {
            const $element = $(element);
            const link = $element.attr("href") || "";
            const title = $element.find("span.tb h2.tit").text().trim();

            if (title && link) {
              titles.push({ idx: idx, title, link });
              idx++;
            }
          });

          for (const title of titles) {
            const link = "https:" + title.link;
            try {
              const detailRes = await axios.get(link, {
                responseType: "arraybuffer",
                headers: {
                  "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
                },
              });
              const detailHtml = iconv.decode(detailRes.data, "euc-kr");
              const $$ = cheerio.load(detailHtml);

              // 🔹 본문 텍스트 (p 태그 + textNode 합침)
              let content = "";
              $$("#realArtcContents")
                .contents()
                .each((i, el) => {
                  if (el.type === "text") {
                    content += $$(el).text().trim();
                  } else if (el.type === "tag" && el.name === "p") {
                    content += $$(el).text().trim();
                  }
                });

              results.push({
                date: current.format("YYYY-MM-DD"),
                title: title.title,
                link: title.link,
                content: content.trim(),
                type: "nate",
              });
            } catch (e) {
              console.error(`본문 크롤링 실패: ${title.link}`, e.message);
            }
          }

          pageNum++;
        } catch (error) {
          this.logger.error(
            `Error processing page ${pageNum}: ${error.message}`
          );
          break;
        }
      }

      return results;
    } catch (error) {
      this.logger.error(`크롤링 중 오류 발생: ${error.message}`);
      throw new Error(
        `네이트 뉴스 데이터를 가져오는 중 오류가 발생했습니다: ${error.message}`
      );
    }
  }
}
