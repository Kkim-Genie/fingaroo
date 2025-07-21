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
Object.defineProperty(exports, "__esModule", { value: true });
exports.FundScraper = void 0;
const common_1 = require("@nestjs/common");
const forex_pair_scraper_1 = require("./forex-pair.scraper");
const twelve_manager_1 = require("../util/manager/twelve.manager");
const fund_entity_1 = require("../entity/fund.entity");
const typeorm_1 = require("@nestjs/typeorm");
const typeorm_2 = require("typeorm");
const investing_manager_1 = require("../util/manager/investing.manager");
const typeorm_transactional_1 = require("typeorm-transactional");
const indicator_enum_1 = require("../util/enum/indicator.enum");
let FundScraper = class FundScraper {
    constructor(twelveManager, investingManager, fundEntityRepository) {
        this.twelveManager = twelveManager;
        this.investingManager = investingManager;
        this.fundEntityRepository = fundEntityRepository;
        this.logger = new common_1.Logger(forex_pair_scraper_1.ForexPairScraper.name);
        this.BATCH_SIZE = 500;
    }
    async scrape(country) {
        const responseBody = await this.twelveManager.getReferenceData(indicator_enum_1.INDICATOR_TYPE.FUND_TYPE, country);
        const rank = await this.investingManager.loadFundRank();
        const data = responseBody.result.list;
        const fundEntities = Array.from(new Map(data.map((fund) => [
            `${fund.symbol}-${fund.name}-${fund.exchange}`,
            {
                extraIndex: rank.has(fund.symbol)
                    ? -1 * rank.get(fund.symbol)
                    : null,
                symbol: fund.symbol,
                indicatorType: indicator_enum_1.INDICATOR_TYPE.FUND_TYPE,
                name: fund.name,
                unit: fund.currency,
                currency: fund.currency,
                exchange: fund.exchange,
                micCode: fund.mic_code,
                country: fund.country,
                type: fund.type,
                figiCode: fund.figi_code,
            },
        ])).values());
        for (let i = 0; i < fundEntities.length; i += this.BATCH_SIZE) {
            const batch = fundEntities.slice(i, i + this.BATCH_SIZE);
            try {
                await this.fundEntityRepository
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
                ], ['symbol', 'name', 'exchange'])
                    .execute();
                this.logger.log(`Inserted batch of ${batch.length} funds for ${country}`);
            }
            catch (error) {
                this.logger.error(`Failed to insert funds data for ${country}:`, error);
                return;
            }
        }
    }
};
exports.FundScraper = FundScraper;
__decorate([
    (0, typeorm_transactional_1.Transactional)(),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [String]),
    __metadata("design:returntype", Promise)
], FundScraper.prototype, "scrape", null);
exports.FundScraper = FundScraper = __decorate([
    (0, common_1.Injectable)(),
    __param(2, (0, typeorm_1.InjectRepository)(fund_entity_1.FundEntity)),
    __metadata("design:paramtypes", [twelve_manager_1.TwelveManager,
        investing_manager_1.InvestingManager,
        typeorm_2.Repository])
], FundScraper);
//# sourceMappingURL=fund.scraper.js.map