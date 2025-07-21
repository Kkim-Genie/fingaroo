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
var CommodityScraper_1;
Object.defineProperty(exports, "__esModule", { value: true });
exports.CommodityScraper = void 0;
const common_1 = require("@nestjs/common");
const twelve_manager_1 = require("../util/manager/twelve.manager");
const commodity_entity_1 = require("../entity/commodity.entity");
const typeorm_1 = require("@nestjs/typeorm");
const typeorm_2 = require("typeorm");
const typeorm_transactional_1 = require("typeorm-transactional");
const indicator_enum_1 = require("../util/enum/indicator.enum");
let CommodityScraper = CommodityScraper_1 = class CommodityScraper {
    constructor(twelveManager, commodityEntityRepository) {
        this.twelveManager = twelveManager;
        this.commodityEntityRepository = commodityEntityRepository;
        this.logger = new common_1.Logger(CommodityScraper_1.name);
        this.BATCH_SIZE = 500;
    }
    async scrape() {
        const responseBody = await this.twelveManager.getReferenceData(indicator_enum_1.INDICATOR_TYPE.COMMODITY_TYPE);
        const data = responseBody.data;
        const commodityEntities = Array.from(new Map(data.map((commodity) => [
            `${commodity.symbol}-${commodity.name}`,
            {
                extraIndex: null,
                symbol: commodity.symbol,
                indicatorType: indicator_enum_1.INDICATOR_TYPE.COMMODITY_TYPE,
                name: commodity.name,
                unit: (commodity.symbol + '/').split('/')[1],
                category: commodity.category,
                description: commodity.description,
            },
        ])).values());
        for (let i = 0; i < commodityEntities.length; i += this.BATCH_SIZE) {
            const batch = commodityEntities.slice(i, i + this.BATCH_SIZE);
            try {
                await this.commodityEntityRepository
                    .createQueryBuilder()
                    .insert()
                    .values(batch)
                    .orUpdate(['extraIndex', 'unit', 'category', 'description'], ['symbol', 'name'])
                    .execute();
                this.logger.log(`Inserted batch of ${batch.length} commodities`);
            }
            catch (error) {
                this.logger.error(`Failed to insert commodities data:`, error);
                return;
            }
        }
    }
};
exports.CommodityScraper = CommodityScraper;
__decorate([
    (0, typeorm_transactional_1.Transactional)(),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], CommodityScraper.prototype, "scrape", null);
exports.CommodityScraper = CommodityScraper = CommodityScraper_1 = __decorate([
    (0, common_1.Injectable)(),
    __param(1, (0, typeorm_1.InjectRepository)(commodity_entity_1.CommodityEntity)),
    __metadata("design:paramtypes", [twelve_manager_1.TwelveManager,
        typeorm_2.Repository])
], CommodityScraper);
//# sourceMappingURL=commodity.scraper.js.map