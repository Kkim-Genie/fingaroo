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
var EtfScraper_1;
Object.defineProperty(exports, "__esModule", { value: true });
exports.EtfScraper = void 0;
const common_1 = require("@nestjs/common");
const twelve_manager_1 = require("../util/manager/twelve.manager");
const etf_entity_1 = require("../entity/etf.entity");
const typeorm_1 = require("@nestjs/typeorm");
const typeorm_2 = require("typeorm");
const investing_manager_1 = require("../util/manager/investing.manager");
const typeorm_transactional_1 = require("typeorm-transactional");
const indicator_enum_1 = require("../util/enum/indicator.enum");
let EtfScraper = EtfScraper_1 = class EtfScraper {
    constructor(twelveManager, investingManager, etfEntityRepository) {
        this.twelveManager = twelveManager;
        this.investingManager = investingManager;
        this.etfEntityRepository = etfEntityRepository;
        this.logger = new common_1.Logger(EtfScraper_1.name);
        this.BATCH_SIZE = 500;
    }
    async scrape(country) {
        const responseBody = await this.twelveManager.getReferenceData(indicator_enum_1.INDICATOR_TYPE.ETF_TYPE, country);
        const rank = await this.investingManager.loadEtfRank();
        const data = responseBody.data;
        const etfEntities = Array.from(new Map(data.map((etf) => [
            `${etf.symbol}-${etf.name}-${etf.exchange}`,
            {
                extraIndex: rank.has(etf.symbol) ? -1 * rank.get(etf.symbol) : null,
                symbol: etf.symbol,
                indicatorType: indicator_enum_1.INDICATOR_TYPE.ETF_TYPE,
                name: etf.name,
                unit: etf.currency,
                currency: etf.currency,
                exchange: etf.exchange,
                micCode: etf.mic_code,
                country: etf.country,
                type: etf.type,
            },
        ])).values());
        for (let i = 0; i < etfEntities.length; i += this.BATCH_SIZE) {
            const batch = etfEntities.slice(i, i + this.BATCH_SIZE);
            try {
                await this.etfEntityRepository
                    .createQueryBuilder()
                    .insert()
                    .values(batch)
                    .orUpdate([
                    'extraIndex',
                    'unit',
                    'currency',
                    'exchange',
                    'micCode',
                    'country',
                    'figiCode',
                ], ['symbol', 'name', 'exchange'])
                    .execute();
                this.logger.log(`Inserted batch of ${batch.length} etfs for ${country}`);
            }
            catch (error) {
                this.logger.error(`Failed to insert etfs data for ${country}:`, error);
                return;
            }
        }
    }
};
exports.EtfScraper = EtfScraper;
__decorate([
    (0, typeorm_transactional_1.Transactional)(),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [String]),
    __metadata("design:returntype", Promise)
], EtfScraper.prototype, "scrape", null);
exports.EtfScraper = EtfScraper = EtfScraper_1 = __decorate([
    (0, common_1.Injectable)(),
    __param(2, (0, typeorm_1.InjectRepository)(etf_entity_1.EtfEntity)),
    __metadata("design:paramtypes", [twelve_manager_1.TwelveManager,
        investing_manager_1.InvestingManager,
        typeorm_2.Repository])
], EtfScraper);
//# sourceMappingURL=etf.scraper.js.map