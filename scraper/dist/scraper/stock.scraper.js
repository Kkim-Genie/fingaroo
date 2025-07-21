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
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
var StockScraper_1;
Object.defineProperty(exports, "__esModule", { value: true });
exports.StockScraper = void 0;
const common_1 = require("@nestjs/common");
const twelve_manager_1 = require("../util/manager/twelve.manager");
const stock_entity_1 = require("../entity/stock.entity");
const typeorm_1 = require("@nestjs/typeorm");
const typeorm_2 = require("typeorm");
const typeorm_transactional_1 = require("typeorm-transactional");
const indicator_enum_1 = require("../util/enum/indicator.enum");
const investing_manager_1 = require("../util/manager/investing.manager");
let StockScraper = StockScraper_1 = class StockScraper {
    constructor(twelveManager, investingManager, stockEntityRepository) {
        this.twelveManager = twelveManager;
        this.investingManager = investingManager;
        this.stockEntityRepository = stockEntityRepository;
        this.logger = new common_1.Logger(StockScraper_1.name);
        this.BATCH_SIZE = 500;
    }
    async scrape(country) {
        const responseBody = await this.twelveManager.getReferenceData(indicator_enum_1.INDICATOR_TYPE.STOCK_TYPE, country);
        const rank = await this.investingManager.loadStockRank(country);
        const data = responseBody.data;
        const stockEntities = Array.from(new Map(data.map((stock) => [
            `${stock.symbol}-${stock.name}-${stock.exchange}`,
            {
                extraIndex: rank.has(stock.symbol) ? rank.get(stock.symbol) : null,
                symbol: stock.symbol,
                indicatorType: indicator_enum_1.INDICATOR_TYPE.STOCK_TYPE,
                name: stock.name,
                unit: stock.currency,
                currency: stock.currency,
                exchange: stock.exchange,
                micCode: stock.mic_code,
                country: stock.country,
                type: stock.type,
                figiCode: stock.figi_code,
                marketCapitalization: null,
            },
        ])).values());
        for (let i = 0; i < stockEntities.length; i += this.BATCH_SIZE) {
            const batch = stockEntities.slice(i, i + this.BATCH_SIZE);
            try {
                await this.stockEntityRepository
                    .createQueryBuilder()
                    .insert()
                    .values(batch)
                    .orUpdate([
                    'extraIndex',
                    'unit',
                    'country',
                    'currency',
                    'micCode',
                    'exchange',
                    'type',
                    'figiCode',
                    'marketCapitalization',
                ], ['symbol', 'name', 'exchange'])
                    .execute();
                this.logger.log(`Inserted batch of ${batch.length} stocks for ${country}`);
            }
            catch (error) {
                this.logger.error(`Failed to insert stocks data for ${country}:`, error);
                return;
            }
        }
    }
};
exports.StockScraper = StockScraper;
__decorate([
    (0, typeorm_transactional_1.Transactional)(),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [String]),
    __metadata("design:returntype", Promise)
], StockScraper.prototype, "scrape", null);
exports.StockScraper = StockScraper = StockScraper_1 = __decorate([
    (0, common_1.Injectable)(),
    __param(2, (0, typeorm_1.InjectRepository)(stock_entity_1.StockEntity)),
    __metadata("design:paramtypes", [twelve_manager_1.TwelveManager,
        investing_manager_1.InvestingManager,
        typeorm_2.Repository])
], StockScraper);
//# sourceMappingURL=stock.scraper.js.map