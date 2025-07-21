"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AppModule = void 0;
const common_1 = require("@nestjs/common");
const axios_1 = require("@nestjs/axios");
const typeorm_1 = require("@nestjs/typeorm");
const bond_entity_1 = require("./entity/bond.entity");
const crypto_currency_entity_1 = require("./entity/crypto-currency.entity");
const etf_entity_1 = require("./entity/etf.entity");
const forex_pair_entity_1 = require("./entity/forex-pair.entity");
const fund_entity_1 = require("./entity/fund.entity");
const index_entity_1 = require("./entity/index.entity");
const stock_entity_1 = require("./entity/stock.entity");
const economy_entity_1 = require("./entity/economy.entity");
const commodity_entity_1 = require("./entity/commodity.entity");
const fred_manager_1 = require("./util/manager/fred.manager");
const twelve_manager_1 = require("./util/manager/twelve.manager");
const investing_manager_1 = require("./util/manager/investing.manager");
const news_manager_1 = require("./util/manager/news.manager");
const stock_scraper_1 = require("./scraper/stock.scraper");
const index_scraper_1 = require("./scraper/index.scraper");
const fund_scraper_1 = require("./scraper/fund.scraper");
const forex_pair_scraper_1 = require("./scraper/forex-pair.scraper");
const etf_scraper_1 = require("./scraper/etf.scraper");
const economy_scraper_1 = require("./scraper/economy.scraper");
const cryptocurrency_scraper_1 = require("./scraper/cryptocurrency.scraper");
const commodity_scraper_1 = require("./scraper/commodity.scraper");
const bond_scraper_1 = require("./scraper/bond.scraper");
const miraeasset_scraper_1 = require("./scraper/miraeasset.scraper");
const indicator_scheduler_1 = require("./scheduler/indicator.scheduler");
const config_1 = require("@nestjs/config");
const typeorm_config_1 = require("./config/typeorm.config");
const typeorm_transactional_1 = require("typeorm-transactional");
const typeorm_2 = require("typeorm");
const futuresnow_scraper_1 = require("./scraper/futuresnow.scraper");
const newstoday_scraper_1 = require("./scraper/newstoday.scraper");
let AppModule = class AppModule {
};
exports.AppModule = AppModule;
exports.AppModule = AppModule = __decorate([
    (0, common_1.Module)({
        imports: [
            config_1.ConfigModule.forRoot({
                isGlobal: true,
            }),
            axios_1.HttpModule.registerAsync({
                useFactory: () => ({
                    timeout: 60000,
                    maxRedirects: 5,
                }),
            }),
            typeorm_1.TypeOrmModule.forRootAsync({
                imports: [config_1.ConfigModule],
                useClass: typeorm_config_1.TypeormConfig,
                async dataSourceFactory(options) {
                    if (!options) {
                        throw new Error('Invalid options passed');
                    }
                    return (0, typeorm_transactional_1.addTransactionalDataSource)(new typeorm_2.DataSource(options));
                },
            }),
            typeorm_1.TypeOrmModule.forFeature([
                bond_entity_1.BondEntity,
                crypto_currency_entity_1.CryptoCurrencyEntity,
                etf_entity_1.EtfEntity,
                forex_pair_entity_1.ForexPairEntity,
                fund_entity_1.FundEntity,
                index_entity_1.IndexEntity,
                stock_entity_1.StockEntity,
                economy_entity_1.EconomyEntity,
                commodity_entity_1.CommodityEntity,
            ]),
        ],
        controllers: [],
        providers: [
            fred_manager_1.FredManager,
            twelve_manager_1.TwelveManager,
            investing_manager_1.InvestingManager,
            news_manager_1.NewsManager,
            stock_scraper_1.StockScraper,
            index_scraper_1.IndexScraper,
            fund_scraper_1.FundScraper,
            forex_pair_scraper_1.ForexPairScraper,
            etf_scraper_1.EtfScraper,
            economy_scraper_1.EconomyScraper,
            cryptocurrency_scraper_1.CryptocurrencyScraper,
            commodity_scraper_1.CommodityScraper,
            bond_scraper_1.BondScraper,
            miraeasset_scraper_1.MiraeAssetScraper,
            indicator_scheduler_1.IndicatorScheduler,
            futuresnow_scraper_1.FutureSnowScraper,
            newstoday_scraper_1.NewsTodayScraper,
        ],
    })
], AppModule);
//# sourceMappingURL=app.module.js.map