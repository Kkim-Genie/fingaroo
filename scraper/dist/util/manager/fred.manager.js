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
exports.FredManager = void 0;
const common_1 = require("@nestjs/common");
const axios_1 = require("@nestjs/axios");
const BASE_URL = 'https://api.stlouisfed.org/fred';
let FredManager = class FredManager {
    constructor(api) {
        this.api = api;
    }
    async getSources() {
        const sourcesUrl = `${BASE_URL}/sources?api_key=${process.env.FRED_KEY}&file_type=json`;
        const sourcesResponse = await this.api.axiosRef.get(sourcesUrl);
        this.checkFredException(sourcesResponse);
        return sourcesResponse.data;
    }
    async getReleases(source) {
        const releasesUrl = `${BASE_URL}/source/releases?source_id=${source.id}&api_key=${process.env.FRED_KEY}&file_type=json`;
        const releasesResponse = await this.api.axiosRef.get(releasesUrl);
        this.checkFredException(releasesResponse);
        return releasesResponse.data;
    }
    async getSeries(release) {
        const seriesUrl = `${BASE_URL}/release/series?release_id=${release.id}&api_key=${process.env.FRED_KEY}&file_type=json`;
        const seriesResponse = await this.api.axiosRef.get(seriesUrl);
        this.checkFredException(seriesResponse);
        return seriesResponse.data;
    }
    checkFredException(response) {
        if (response.status === common_1.HttpStatus.BAD_REQUEST) {
            throw new common_1.BadRequestException(response.data.error_message);
        }
        if (response.status === common_1.HttpStatus.NOT_FOUND) {
            throw new common_1.NotFoundException(response.data.error_message);
        }
        if (response.status === common_1.HttpStatus.INTERNAL_SERVER_ERROR) {
            throw new common_1.InternalServerErrorException(response.data.error_message);
        }
        if (response.status === common_1.HttpStatus.TOO_MANY_REQUESTS) {
            throw new common_1.HttpException(response.data.error_message, common_1.HttpStatus.TOO_MANY_REQUESTS);
        }
        return response;
    }
};
exports.FredManager = FredManager;
exports.FredManager = FredManager = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [axios_1.HttpService])
], FredManager);
//# sourceMappingURL=fred.manager.js.map