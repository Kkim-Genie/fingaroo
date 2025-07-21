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
var CryptocurrencyScraper_1;
Object.defineProperty(exports, "__esModule", { value: true });
exports.CryptocurrencyScraper = void 0;
const common_1 = require("@nestjs/common");
const twelve_manager_1 = require("../util/manager/twelve.manager");
const crypto_currency_entity_1 = require("../entity/crypto-currency.entity");
const typeorm_1 = require("@nestjs/typeorm");
const typeorm_2 = require("typeorm");
const investing_manager_1 = require("../util/manager/investing.manager");
const typeorm_transactional_1 = require("typeorm-transactional");
const indicator_enum_1 = require("../util/enum/indicator.enum");
let CryptocurrencyScraper = CryptocurrencyScraper_1 = class CryptocurrencyScraper {
    constructor(twelveManager, investingManager, cryptoCurrencyEntityRepository) {
        this.twelveManager = twelveManager;
        this.investingManager = investingManager;
        this.cryptoCurrencyEntityRepository = cryptoCurrencyEntityRepository;
        this.logger = new common_1.Logger(CryptocurrencyScraper_1.name);
        this.BATCH_SIZE = 500;
    }
    async scrape() {
        const responseBody = await this.twelveManager.getReferenceData(indicator_enum_1.INDICATOR_TYPE.CRYPTOCURRENCY_TYPE);
        const rank = await this.investingManager.loadCryptocurrencyRank();
        const attachedRank = new Map(Array.from(rank.entries()).map(([key, value]) => [`${key}/USD`, value]));
        const data = responseBody.data;
        const cryptocurrencyEntities = Array.from(new Map(data.map((cryptocurrency) => [
            `${cryptocurrency.symbol}-${cryptocurrency.name}`,
            {
                extraIndex: attachedRank.has(cryptocurrency.symbol)
                    ? -1 * attachedRank.get(cryptocurrency.symbol)
                    : null,
                symbol: cryptocurrency.symbol,
                indicatorType: indicator_enum_1.INDICATOR_TYPE.CRYPTOCURRENCY_TYPE,
                name: cryptocurrency.currency_base,
                unit: cryptocurrency.currency_quote,
                availableExchanges: cryptocurrency.available_exchanges,
                currencyBase: cryptocurrency.currency_base,
                currencyQuote: cryptocurrency.currency_quote,
            },
        ])).values());
        for (let i = 0; i < cryptocurrencyEntities.length; i += this.BATCH_SIZE) {
            const batch = cryptocurrencyEntities.slice(i, i + this.BATCH_SIZE);
            try {
                await this.cryptoCurrencyEntityRepository
                    .createQueryBuilder()
                    .insert()
                    .values(batch)
                    .orUpdate([
                    'extraIndex',
                    'unit',
                    'availableExchanges',
                    'currencyBase',
                    'currencyQuote',
                ], ['symbol', 'name'])
                    .execute();
                this.logger.log(`Inserted batch of ${batch.length} cryptocurrencies`);
            }
            catch (error) {
                this.logger.error(`Failed to insert cryptocurrencies data:`, error);
                return;
            }
        }
    }
};
exports.CryptocurrencyScraper = CryptocurrencyScraper;
__decorate([
    (0, typeorm_transactional_1.Transactional)(),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], CryptocurrencyScraper.prototype, "scrape", null);
exports.CryptocurrencyScraper = CryptocurrencyScraper = CryptocurrencyScraper_1 = __decorate([
    (0, common_1.Injectable)(),
    __param(2, (0, typeorm_1.InjectRepository)(crypto_currency_entity_1.CryptoCurrencyEntity)),
    __metadata("design:paramtypes", [twelve_manager_1.TwelveManager,
        investing_manager_1.InvestingManager,
        typeorm_2.Repository])
], CryptocurrencyScraper);
//# sourceMappingURL=cryptocurrency.scraper.js.map