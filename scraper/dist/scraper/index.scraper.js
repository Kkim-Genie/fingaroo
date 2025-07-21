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
var IndexScraper_1;
Object.defineProperty(exports, "__esModule", { value: true });
exports.IndexScraper = void 0;
const common_1 = require("@nestjs/common");
const index_entity_1 = require("../entity/index.entity");
const typeorm_1 = require("@nestjs/typeorm");
const typeorm_2 = require("typeorm");
const typeorm_transactional_1 = require("typeorm-transactional");
let IndexScraper = IndexScraper_1 = class IndexScraper {
    constructor(indexEntityRepository) {
        this.indexEntityRepository = indexEntityRepository;
        this.logger = new common_1.Logger(IndexScraper_1.name);
        this.BATCH_SIZE = 500;
    }
    async scrape() {
        throw new common_1.NotImplementedException('아직 구현되지 않았습니다(Twelve Data API 추가 시 작업 예정).');
    }
};
exports.IndexScraper = IndexScraper;
__decorate([
    (0, typeorm_transactional_1.Transactional)(),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], IndexScraper.prototype, "scrape", null);
exports.IndexScraper = IndexScraper = IndexScraper_1 = __decorate([
    (0, common_1.Injectable)(),
    __param(0, (0, typeorm_1.InjectRepository)(index_entity_1.IndexEntity)),
    __metadata("design:paramtypes", [typeorm_2.Repository])
], IndexScraper);
//# sourceMappingURL=index.scraper.js.map