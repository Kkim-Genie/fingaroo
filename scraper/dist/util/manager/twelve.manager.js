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
exports.TwelveManager = void 0;
const common_1 = require("@nestjs/common");
const axios_1 = require("@nestjs/axios");
const indicator_enum_1 = require("../enum/indicator.enum");
const BASE_URL = 'https://api.twelvedata.com';
let TwelveManager = class TwelveManager {
    constructor(api) {
        this.api = api;
    }
    async getReferenceData(indicatorType, country = null) {
        const requestUrl = this.getReferenceDataUri(indicatorType, country);
        const response = await this.api.axiosRef.get(requestUrl);
        return this.checkTwelveException(response.data);
    }
    async getStatistics(symbol, micCode) {
        const requestUrl = `${BASE_URL}/statistics?symbol=${symbol}&mic_code=${micCode}&apikey=${process.env.TWELVE_KEY}`;
        const response = await this.api.axiosRef.get(requestUrl);
        return this.checkTwelveException(response.data);
    }
    async getExchangeRate(sourceCurrency, targetCurrency = 'USD') {
        const requestUrl = `${BASE_URL}/exchange_rate?symbol=${sourceCurrency}/${targetCurrency}&apikey=${process.env.TWELVE_KEY}`;
        const response = await this.api.axiosRef.get(requestUrl);
        return this.checkTwelveException(response.data);
    }
    convertIndicatorTypeToTwelveIndicatorType(indicatorType) {
        if (indicatorType === indicator_enum_1.INDICATOR_TYPE.STOCK_TYPE)
            return 'stocks';
        if (indicatorType === indicator_enum_1.INDICATOR_TYPE.FOREX_PAIR_TYPE)
            return 'forex_pairs';
        if (indicatorType === indicator_enum_1.INDICATOR_TYPE.CRYPTOCURRENCY_TYPE)
            return 'cryptocurrencies';
        if (indicatorType === indicator_enum_1.INDICATOR_TYPE.FUND_TYPE)
            return 'funds';
        if (indicatorType === indicator_enum_1.INDICATOR_TYPE.BOND_TYPE)
            return 'bonds';
        if (indicatorType === indicator_enum_1.INDICATOR_TYPE.ETF_TYPE)
            return 'etfs';
        if (indicatorType === indicator_enum_1.INDICATOR_TYPE.COMMODITY_TYPE)
            return 'commodities';
        if (indicatorType === indicator_enum_1.INDICATOR_TYPE.INDEX_TYPE)
            return 'indices';
    }
    getReferenceDataUri(indicatorType, country = null) {
        const convertedIndicatorType = this.convertIndicatorTypeToTwelveIndicatorType(indicatorType);
        if (indicatorType === indicator_enum_1.INDICATOR_TYPE.STOCK_TYPE ||
            indicatorType === indicator_enum_1.INDICATOR_TYPE.FUND_TYPE ||
            indicatorType === indicator_enum_1.INDICATOR_TYPE.BOND_TYPE ||
            indicatorType === indicator_enum_1.INDICATOR_TYPE.ETF_TYPE) {
            return `${BASE_URL}/${convertedIndicatorType}?country=${country}&apikey=${process.env.TWELVE_KEY}`;
        }
        else if (indicatorType === indicator_enum_1.INDICATOR_TYPE.FOREX_PAIR_TYPE ||
            indicatorType === indicator_enum_1.INDICATOR_TYPE.CRYPTOCURRENCY_TYPE ||
            indicatorType === indicator_enum_1.INDICATOR_TYPE.COMMODITY_TYPE) {
            return `${BASE_URL}/${convertedIndicatorType}?apikey=${process.env.TWELVE_KEY}`;
        }
        throw new common_1.NotImplementedException('시스템에 등록되지 않은 Asset Type 입니다.');
    }
    checkTwelveException(responseBody) {
        if (responseBody.status === 'error') {
            if (responseBody.code === common_1.HttpStatus.BAD_REQUEST) {
                throw new common_1.BadRequestException();
            }
            if (responseBody.code === common_1.HttpStatus.NOT_FOUND) {
                throw new common_1.NotFoundException('');
            }
            if (responseBody.code === common_1.HttpStatus.TOO_MANY_REQUESTS) {
                throw new common_1.HttpException('Too Many Requests for Twelve Data API', common_1.HttpStatus.TOO_MANY_REQUESTS);
            }
        }
        return responseBody;
    }
};
exports.TwelveManager = TwelveManager;
exports.TwelveManager = TwelveManager = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [axios_1.HttpService])
], TwelveManager);
//# sourceMappingURL=twelve.manager.js.map