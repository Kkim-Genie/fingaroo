"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var IndicatorScheduler_1;
Object.defineProperty(exports, "__esModule", { value: true });
exports.IndicatorScheduler = void 0;
const common_1 = require("@nestjs/common");
const bond_scraper_1 = require("../scraper/bond.scraper");
const commodity_scraper_1 = require("../scraper/commodity.scraper");
const cryptocurrency_scraper_1 = require("../scraper/cryptocurrency.scraper");
const economy_scraper_1 = require("../scraper/economy.scraper");
const etf_scraper_1 = require("../scraper/etf.scraper");
const forex_pair_scraper_1 = require("../scraper/forex-pair.scraper");
const fund_scraper_1 = require("../scraper/fund.scraper");
const index_scraper_1 = require("../scraper/index.scraper");
const stock_scraper_1 = require("../scraper/stock.scraper");
let IndicatorScheduler = IndicatorScheduler_1 = class IndicatorScheduler {
    constructor(bondScraper, commodityScraper, cryptocurrencyScraper, economyScraper, etfScraper, forexPairScraper, fundScraper, indexScraper, stockScraper) {
        this.bondScraper = bondScraper;
        this.commodityScraper = commodityScraper;
        this.cryptocurrencyScraper = cryptocurrencyScraper;
        this.economyScraper = economyScraper;
        this.etfScraper = etfScraper;
        this.forexPairScraper = forexPairScraper;
        this.fundScraper = fundScraper;
        this.indexScraper = indexScraper;
        this.stockScraper = stockScraper;
        this.logger = new common_1.Logger(IndicatorScheduler_1.name);
        this.countries = ['United States', 'South Korea', 'China'];
    }
    async saveStockList() {
        for (const country of this.countries) {
            await this.stockScraper.scrape(country);
            this.logger.log(`Success to insert stocks data (${country})`);
        }
    }
    async saveForexPairList() {
        await this.forexPairScraper.scrape();
        this.logger.log('Success to insert forex_pairs data');
    }
    async saveCryptocurrencyList() {
        await this.cryptocurrencyScraper.scrape();
        this.logger.log('Success to insert cryptocurrencies data');
    }
    async saveFundList() {
        for (const country of this.countries) {
            await this.fundScraper.scrape(country);
            this.logger.log(`Success to insert funds data (${country})`);
        }
    }
    async saveBondList() {
        for (const country of this.countries) {
            await this.bondScraper.scrape(country);
            this.logger.log(`Success to insert bonds data (${country})`);
        }
    }
    async saveEtfList() {
        for (const country of this.countries) {
            await this.etfScraper.scrape(country);
            this.logger.log(`Success to insert etfs data (${country})`);
        }
    }
    async saveCommodityList() {
        await this.commodityScraper.scrape();
        this.logger.log('Success to insert commodities data');
    }
    async saveIndexList() {
        throw new common_1.NotImplementedException('아직 구현되지 않았습니다(Twelve Data API 추가 시 작업 예정).');
    }
    async saveEconomyList() {
        await this.economyScraper.scrape();
        this.logger.log('Success to insert economies data');
    }
};
exports.IndicatorScheduler = IndicatorScheduler;
exports.IndicatorScheduler = IndicatorScheduler = IndicatorScheduler_1 = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [bond_scraper_1.BondScraper,
        commodity_scraper_1.CommodityScraper,
        cryptocurrency_scraper_1.CryptocurrencyScraper,
        economy_scraper_1.EconomyScraper,
        etf_scraper_1.EtfScraper,
        forex_pair_scraper_1.ForexPairScraper,
        fund_scraper_1.FundScraper,
        index_scraper_1.IndexScraper,
        stock_scraper_1.StockScraper])
], IndicatorScheduler);
//# sourceMappingURL=indicator.scheduler.js.map