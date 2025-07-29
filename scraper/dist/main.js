"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = require("@nestjs/core");
const app_module_1 = require("./app.module");
const apify_1 = require("apify");
const news_enum_1 = require("./util/enum/news.enum");
const miraeasset_scraper_1 = require("./scraper/miraeasset.scraper");
const nate_scraper_1 = require("./scraper/nate.scraper");
async function main() {
    const app = await core_1.NestFactory.create(app_module_1.AppModule);
    await app.init();
    const { newsType } = await apify_1.Actor.getInput();
    if (!newsType) {
        throw new Error("No input provided");
    }
    if (newsType === news_enum_1.NEWS_TYPE.MIRAE_ASSET) {
        await app.get(miraeasset_scraper_1.MiraeAssetScraper).scrape();
    }
    else if (newsType === news_enum_1.NEWS_TYPE.NATE) {
        await app.get(nate_scraper_1.NateScraper).scrape();
    }
    console.log("Scraping finished successfully");
}
apify_1.Actor.main(main);
//# sourceMappingURL=main.js.map