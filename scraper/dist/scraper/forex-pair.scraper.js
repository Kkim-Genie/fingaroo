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
var ForexPairScraper_1;
Object.defineProperty(exports, "__esModule", { value: true });
exports.ForexPairScraper = void 0;
const common_1 = require("@nestjs/common");
const twelve_manager_1 = require("../util/manager/twelve.manager");
const forex_pair_entity_1 = require("../entity/forex-pair.entity");
const typeorm_1 = require("@nestjs/typeorm");
const typeorm_2 = require("typeorm");
const investing_manager_1 = require("../util/manager/investing.manager");
const typeorm_transactional_1 = require("typeorm-transactional");
const indicator_enum_1 = require("../util/enum/indicator.enum");
let ForexPairScraper = ForexPairScraper_1 = class ForexPairScraper {
    constructor(twelveManager, investingManager, forexPairEntityRepository) {
        this.twelveManager = twelveManager;
        this.investingManager = investingManager;
        this.forexPairEntityRepository = forexPairEntityRepository;
        this.logger = new common_1.Logger(ForexPairScraper_1.name);
        this.BATCH_SIZE = 500;
    }
    async scrape() {
        const responseBody = await this.twelveManager.getReferenceData(indicator_enum_1.INDICATOR_TYPE.FOREX_PAIR_TYPE);
        const rank = await this.investingManager.loadForexPairRank();
        const data = responseBody.data;
        const forexPairEntities = Array.from(new Map(data.map((forexPair) => [
            `${forexPair.symbol}-${forexPair.name}`,
            {
                extraIndex: rank.has(forexPair.symbol)
                    ? -1 * rank.get(forexPair.symbol)
                    : null,
                symbol: forexPair.symbol,
                indicatorType: indicator_enum_1.INDICATOR_TYPE.FOREX_PAIR_TYPE,
                name: forexPair.currency_base,
                unit: forexPair.currency_quote,
                currencyGroup: forexPair.currency_group,
                currencyBase: forexPair.currency_base,
                currencyQuote: forexPair.currency_quote,
            },
        ])).values());
        for (let i = 0; i < forexPairEntities.length; i += this.BATCH_SIZE) {
            const batch = forexPairEntities.slice(i, i + this.BATCH_SIZE);
            try {
                await this.forexPairEntityRepository
                    .createQueryBuilder()
                    .insert()
                    .values(batch)
                    .orUpdate([
                    'extraIndex',
                    'unit',
                    'currencyGroup',
                    'currencyBase',
                    'currencyQuote',
                ], ['symbol', 'name'])
                    .execute();
                this.logger.log(`Inserted batch of ${batch.length} forex_pairs`);
            }
            catch (error) {
                this.logger.error(`Failed to insert forex_pairs data:`, error);
                return;
            }
        }
    }
};
exports.ForexPairScraper = ForexPairScraper;
__decorate([
    (0, typeorm_transactional_1.Transactional)(),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], ForexPairScraper.prototype, "scrape", null);
exports.ForexPairScraper = ForexPairScraper = ForexPairScraper_1 = __decorate([
    (0, common_1.Injectable)(),
    __param(2, (0, typeorm_1.InjectRepository)(forex_pair_entity_1.ForexPairEntity)),
    __metadata("design:paramtypes", [twelve_manager_1.TwelveManager,
        investing_manager_1.InvestingManager,
        typeorm_2.Repository])
], ForexPairScraper);
//# sourceMappingURL=forex-pair.scraper.js.map