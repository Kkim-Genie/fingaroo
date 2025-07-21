import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";
import { initializeTransactionalContext } from "typeorm-transactional";
import { Actor } from "apify";
import { NewsType } from "./util/type/news.type";
import { NEWS_TYPE } from "./util/enum/news.enum";
import { MiraeAssetScraper } from "./scraper/miraeasset.scraper";
import { FutureSnowScraper } from "./scraper/futuresnow.scraper";
import { NewsTodayScraper } from "./scraper/newstoday.scraper";

interface InputData {
  newsType?: NewsType;
}

async function main(): Promise<void> {
  initializeTransactionalContext();
  const app = await NestFactory.create(AppModule);
  await app.init();
  const { newsType } = await Actor.getInput<InputData>();
  if (!newsType) {
    throw new Error("No input provided");
  }
  if (newsType === NEWS_TYPE.MIRAE_ASSET) {
    await app.get(MiraeAssetScraper).scrape();
  } else if (newsType === NEWS_TYPE.YOUTUBE) {
    await app.get(FutureSnowScraper).scrape();
  } else if (newsType === NEWS_TYPE.NEWS_TODAY) {
    await app.get(NewsTodayScraper).scrape();
  }
  console.log("Scraping finished successfully");
}
Actor.main(main);
