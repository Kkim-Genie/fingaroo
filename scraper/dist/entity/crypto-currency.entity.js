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
Object.defineProperty(exports, "__esModule", { value: true });
exports.CryptoCurrencyEntity = void 0;
const typeorm_1 = require("typeorm");
const base_indicator_entity_1 = require("./common/base-indicator.entity");
let CryptoCurrencyEntity = class CryptoCurrencyEntity extends base_indicator_entity_1.BaseIndicatorEntity {
};
exports.CryptoCurrencyEntity = CryptoCurrencyEntity;
__decorate([
    (0, typeorm_1.Column)('jsonb', { nullable: true }),
    __metadata("design:type", Array)
], CryptoCurrencyEntity.prototype, "availableExchanges", void 0);
__decorate([
    (0, typeorm_1.Column)({ nullable: true }),
    __metadata("design:type", String)
], CryptoCurrencyEntity.prototype, "currencyBase", void 0);
__decorate([
    (0, typeorm_1.Column)({ nullable: true }),
    __metadata("design:type", String)
], CryptoCurrencyEntity.prototype, "currencyQuote", void 0);
exports.CryptoCurrencyEntity = CryptoCurrencyEntity = __decorate([
    (0, typeorm_1.Unique)(['symbol', 'name']),
    (0, typeorm_1.Entity)({ name: 'cryptocurrencies' })
], CryptoCurrencyEntity);
//# sourceMappingURL=crypto-currency.entity.js.map