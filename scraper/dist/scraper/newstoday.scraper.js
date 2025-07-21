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
var NewsTodayScraper_1;
Object.defineProperty(exports, "__esModule", { value: true });
exports.NewsTodayScraper = void 0;
const axios_1 = require("@nestjs/axios");
const common_1 = require("@nestjs/common");
const news_manager_1 = require("../util/manager/news.manager");
const typeorm_transactional_1 = require("typeorm-transactional");
let NewsTodayScraper = NewsTodayScraper_1 = class NewsTodayScraper {
    constructor(newsManager, httpService) {
        this.newsManager = newsManager;
        this.httpService = httpService;
        this.logger = new common_1.Logger(NewsTodayScraper_1.name);
    }
    async scrape() {
        const news = await this.newsManager.loadNewsToday();
        const apiUrl = `${process.env.AI_ADMIN_URL}/news`;
        try {
            const response = await this.httpService.axiosRef.post(apiUrl, {
                news,
            });
            console.log('POST response:', response.data);
        }
        catch (error) {
            console.error('POST error:', error);
        }
    }
};
exports.NewsTodayScraper = NewsTodayScraper;
__decorate([
    (0, typeorm_transactional_1.Transactional)(),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], NewsTodayScraper.prototype, "scrape", null);
exports.NewsTodayScraper = NewsTodayScraper = NewsTodayScraper_1 = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [news_manager_1.NewsManager,
        axios_1.HttpService])
], NewsTodayScraper);
//# sourceMappingURL=newstoday.scraper.js.map