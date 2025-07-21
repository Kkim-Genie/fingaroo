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
exports.IndexEntity = void 0;
const typeorm_1 = require("typeorm");
const base_indicator_entity_1 = require("./common/base-indicator.entity");
let IndexEntity = class IndexEntity extends base_indicator_entity_1.BaseIndicatorEntity {
};
exports.IndexEntity = IndexEntity;
__decorate([
    (0, typeorm_1.Column)({ nullable: true }),
    __metadata("design:type", String)
], IndexEntity.prototype, "country", void 0);
__decorate([
    (0, typeorm_1.Column)({ nullable: true }),
    __metadata("design:type", String)
], IndexEntity.prototype, "currency", void 0);
__decorate([
    (0, typeorm_1.Column)({ nullable: true }),
    __metadata("design:type", String)
], IndexEntity.prototype, "exchange", void 0);
__decorate([
    (0, typeorm_1.Column)({ nullable: true }),
    __metadata("design:type", String)
], IndexEntity.prototype, "micCode", void 0);
exports.IndexEntity = IndexEntity = __decorate([
    (0, typeorm_1.Unique)(['symbol', 'name', 'exchange']),
    (0, typeorm_1.Entity)({ name: 'indices' })
], IndexEntity);
//# sourceMappingURL=index.entity.js.map