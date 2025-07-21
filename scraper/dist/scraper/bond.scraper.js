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
var BondScraper_1;
Object.defineProperty(exports, "__esModule", { value: true });
exports.BondScraper = void 0;
const common_1 = require("@nestjs/common");
const twelve_manager_1 = require("../util/manager/twelve.manager");
const typeorm_1 = require("@nestjs/typeorm");
const bond_entity_1 = require("../entity/bond.entity");
const typeorm_2 = require("typeorm");
const typeorm_transactional_1 = require("typeorm-transactional");
const indicator_enum_1 = require("../util/enum/indicator.enum");
let BondScraper = BondScraper_1 = class BondScraper {
    constructor(twelveManager, bondEntityRepository) {
        this.twelveManager = twelveManager;
        this.bondEntityRepository = bondEntityRepository;
        this.logger = new common_1.Logger(BondScraper_1.name);
        this.BATCH_SIZE = 500;
    }
    async scrape(country) {
        const responseBody = await this.twelveManager.getReferenceData(indicator_enum_1.INDICATOR_TYPE.BOND_TYPE, country);
        const data = responseBody.result.list;
        const bondEntities = Array.from(new Map(data.map((bond) => [
            `${bond.symbol}-${bond.name}-${bond.exchange}`,
            {
                extraIndex: null,
                symbol: bond.symbol,
                indicatorType: indicator_enum_1.INDICATOR_TYPE.BOND_TYPE,
                name: bond.name,
                unit: '%',
                currency: bond.currency,
                exchange: bond.exchange,
                micCode: bond.mic_code,
                country: bond.country,
                type: bond.type,
            },
        ])).values());
        for (let i = 0; i < bondEntities.length; i += this.BATCH_SIZE) {
            const batch = bondEntities.slice(i, i + this.BATCH_SIZE);
            try {
                await this.bondEntityRepository
                    .createQueryBuilder()
                    .insert()
                    .values(batch)
                    .orUpdate([
                    'extraIndex',
                    'unit',
                    'country',
                    'currency',
                    'exchange',
                    'micCode',
                    'type',
                ], ['symbol', 'name', 'exchange'])
                    .execute();
                this.logger.log(`Inserted batch of ${batch.length} bonds for ${country}`);
            }
            catch (error) {
                this.logger.error(`Failed to insert bonds data for ${country}:`, error);
                return;
            }
        }
    }
};
exports.BondScraper = BondScraper;
__decorate([
    (0, typeorm_transactional_1.Transactional)(),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [String]),
    __metadata("design:returntype", Promise)
], BondScraper.prototype, "scrape", null);
exports.BondScraper = BondScraper = BondScraper_1 = __decorate([
    (0, common_1.Injectable)(),
    __param(1, (0, typeorm_1.InjectRepository)(bond_entity_1.BondEntity)),
    __metadata("design:paramtypes", [twelve_manager_1.TwelveManager,
        typeorm_2.Repository])
], BondScraper);
//# sourceMappingURL=bond.scraper.js.map