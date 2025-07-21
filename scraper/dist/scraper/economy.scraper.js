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
var EconomyScraper_1;
Object.defineProperty(exports, "__esModule", { value: true });
exports.EconomyScraper = void 0;
const common_1 = require("@nestjs/common");
const fred_manager_1 = require("../util/manager/fred.manager");
const economy_entity_1 = require("../entity/economy.entity");
const typeorm_1 = require("@nestjs/typeorm");
const typeorm_2 = require("typeorm");
const typeorm_transactional_1 = require("typeorm-transactional");
const indicator_enum_1 = require("../util/enum/indicator.enum");
let EconomyScraper = EconomyScraper_1 = class EconomyScraper {
    constructor(fredManager, economyEntityRepository) {
        this.fredManager = fredManager;
        this.economyEntityRepository = economyEntityRepository;
        this.logger = new common_1.Logger(EconomyScraper_1.name);
        this.BATCH_SIZE = 500;
        this.FREQUENCY_WHITELIST = [
            'Annual',
            'Semiannual',
            'Quarterly',
            'Monthly',
            'Biweekly',
            'Weekly',
            'Daily',
        ];
    }
    async scrape() {
        const sourcesResponseBody = await this.fredManager.getSources();
        const sources = sourcesResponseBody.sources;
        for (const source of sources) {
            const releasesResponseData = await this.fredManager.getReleases(source);
            await new Promise((resolve) => setTimeout(resolve, 500));
            const releases = releasesResponseData.releases;
            for (const release of releases) {
                const seriesResponseData = await this.fredManager.getSeries(release);
                await new Promise((resolve) => setTimeout(resolve, 500));
                const seriess = seriesResponseData.seriess;
                const economyEntities = Array.from(new Map(seriess
                    .filter((series) => this.FREQUENCY_WHITELIST.some((freq) => series.frequency?.includes(freq)))
                    .map((series) => [
                    `${series.id}-${series.title}`,
                    {
                        extraIndex: series.popularity ?? null,
                        symbol: series.id,
                        indicatorType: indicator_enum_1.INDICATOR_TYPE.ECONOMY_TYPE,
                        name: series.title,
                        unit: series.units_short,
                        frequency: series.frequency,
                        frequencyShort: series.frequency_short,
                        seasonalAdjustment: series.seasonal_adjustment,
                        seasonalAdjustmentShort: series.seasonal_adjustment_short,
                        unitDescription: series.units,
                        popularity: series.popularity ?? null,
                        notes: series.notes,
                    },
                ])).values());
                for (let i = 0; i < economyEntities.length; i += this.BATCH_SIZE) {
                    const batch = economyEntities.slice(i, i + this.BATCH_SIZE);
                    try {
                        await this.economyEntityRepository
                            .createQueryBuilder()
                            .insert()
                            .values(batch)
                            .orUpdate([
                            'extraIndex',
                            'unit',
                            'frequency',
                            'frequencyShort',
                            'seasonalAdjustment',
                            'seasonalAdjustmentShort',
                            'unitDescription',
                            'popularity',
                            'notes',
                        ], ['symbol', 'name'])
                            .execute();
                        this.logger.log(`Inserted batch of ${batch.length} economies`);
                    }
                    catch (error) {
                        this.logger.error(`Failed to insert economies data:`, error);
                        return;
                    }
                }
            }
        }
    }
};
exports.EconomyScraper = EconomyScraper;
__decorate([
    (0, typeorm_transactional_1.Transactional)(),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], EconomyScraper.prototype, "scrape", null);
exports.EconomyScraper = EconomyScraper = EconomyScraper_1 = __decorate([
    (0, common_1.Injectable)(),
    __param(1, (0, typeorm_1.InjectRepository)(economy_entity_1.EconomyEntity)),
    __metadata("design:paramtypes", [fred_manager_1.FredManager,
        typeorm_2.Repository])
], EconomyScraper);
//# sourceMappingURL=economy.scraper.js.map