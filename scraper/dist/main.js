"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = require("@nestjs/core");
const app_module_1 = require("./app.module");
const typeorm_transactional_1 = require("typeorm-transactional");
const apify_1 = require("apify");
const stock_scraper_1 = require("./scraper/stock.scraper");
const fund_scraper_1 = require("./scraper/fund.scraper");
const bond_scraper_1 = require("./scraper/bond.scraper");
const etf_scraper_1 = require("./scraper/etf.scraper");
const forex_pair_scraper_1 = require("./scraper/forex-pair.scraper");
const cryptocurrency_scraper_1 = require("./scraper/cryptocurrency.scraper");
const commodity_scraper_1 = require("./scraper/commodity.scraper");
const economy_scraper_1 = require("./scraper/economy.scraper");
const country_enum_1 = require("./util/enum/country.enum");
const indicator_enum_1 = require("./util/enum/indicator.enum");
const news_enum_1 = require("./util/enum/news.enum");
const miraeasset_scraper_1 = require("./scraper/miraeasset.scraper");
const futuresnow_scraper_1 = require("./scraper/futuresnow.scraper");
const newstoday_scraper_1 = require("./scraper/newstoday.scraper");
async function main() {
    (0, typeorm_transactional_1.initializeTransactionalContext)();
    const countries = Object.values(country_enum_1.COUNTRY_TYPE);
    const app = await core_1.NestFactory.create(app_module_1.AppModule);
    await app.init();
    const { indicatorType, countryType, newsType } = await apify_1.Actor.getInput();
    if (indicatorType) {
        if (indicatorType === indicator_enum_1.INDICATOR_TYPE.STOCK_TYPE) {
            if (countryType) {
                await app.get(stock_scraper_1.StockScraper).scrape(countryType);
            }
            else {
                for (const country of countries) {
                    await app.get(stock_scraper_1.StockScraper).scrape(country);
                }
            }
        }
        else if (indicatorType === indicator_enum_1.INDICATOR_TYPE.FUND_TYPE) {
            if (countryType) {
                await app.get(fund_scraper_1.FundScraper).scrape(countryType);
            }
            else {
                for (const country of countries) {
                    await app.get(fund_scraper_1.FundScraper).scrape(country);
                }
            }
        }
        else if (indicatorType === indicator_enum_1.INDICATOR_TYPE.BOND_TYPE) {
            if (countryType) {
                await app.get(bond_scraper_1.BondScraper).scrape(countryType);
            }
            else {
                for (const country of countries) {
                    await app.get(bond_scraper_1.BondScraper).scrape(country);
                }
            }
        }
        else if (indicatorType === indicator_enum_1.INDICATOR_TYPE.ETF_TYPE) {
            if (countryType) {
                await app.get(etf_scraper_1.EtfScraper).scrape(countryType);
            }
            else {
                for (const country of countries) {
                    await app.get(etf_scraper_1.EtfScraper).scrape(country);
                }
            }
        }
        else if (indicatorType === indicator_enum_1.INDICATOR_TYPE.FOREX_PAIR_TYPE) {
            await app.get(forex_pair_scraper_1.ForexPairScraper).scrape();
        }
        else if (indicatorType === indicator_enum_1.INDICATOR_TYPE.CRYPTOCURRENCY_TYPE) {
            await app.get(cryptocurrency_scraper_1.CryptocurrencyScraper).scrape();
        }
        else if (indicatorType === indicator_enum_1.INDICATOR_TYPE.COMMODITY_TYPE) {
            await app.get(commodity_scraper_1.CommodityScraper).scrape();
        }
        else if (indicatorType === indicator_enum_1.INDICATOR_TYPE.ECONOMY_TYPE) {
            await app.get(economy_scraper_1.EconomyScraper).scrape();
        }
        else if (indicatorType === indicator_enum_1.INDICATOR_TYPE.INDEX_TYPE) {
            console.log('Index scraping not implemented yet');
        }
        else {
            throw new Error(`Unknown indicator type: ${indicatorType}`);
        }
    }
    else {
        if (!newsType) {
            throw new Error('No input provided');
        }
        if (newsType === news_enum_1.NEWS_TYPE.MIRAE_ASSET) {
            await app.get(miraeasset_scraper_1.MiraeAssetScraper).scrape();
        }
        else if (newsType === news_enum_1.NEWS_TYPE.YOUTUBE) {
            await app.get(futuresnow_scraper_1.FutureSnowScraper).scrape();
        }
        else if (newsType === news_enum_1.NEWS_TYPE.NEWS_TODAY) {
            await app.get(newstoday_scraper_1.NewsTodayScraper).scrape();
        }
    }
    console.log('Scraping finished successfully');
}
apify_1.Actor.main(main);
//# sourceMappingURL=main.js.map