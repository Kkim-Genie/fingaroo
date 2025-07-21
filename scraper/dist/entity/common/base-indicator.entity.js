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
exports.BaseIndicatorEntity = void 0;
const typeorm_1 = require("typeorm");
const base_entity_1 = require("./base.entity");
class BaseIndicatorEntity extends base_entity_1.BaseEntity {
}
exports.BaseIndicatorEntity = BaseIndicatorEntity;
__decorate([
    (0, typeorm_1.PrimaryGeneratedColumn)('uuid'),
    __metadata("design:type", String)
], BaseIndicatorEntity.prototype, "id", void 0);
__decorate([
    (0, typeorm_1.Column)({ generated: 'increment' }),
    __metadata("design:type", Number)
], BaseIndicatorEntity.prototype, "index", void 0);
__decorate([
    (0, typeorm_1.Column)({
        type: 'double precision',
        nullable: true,
        transformer: {
            to: (value) => value,
            from: (value) => (value ? Number(value) : null),
        },
    }),
    __metadata("design:type", Number)
], BaseIndicatorEntity.prototype, "extraIndex", void 0);
__decorate([
    (0, typeorm_1.Column)(),
    __metadata("design:type", String)
], BaseIndicatorEntity.prototype, "symbol", void 0);
__decorate([
    (0, typeorm_1.Column)(),
    __metadata("design:type", String)
], BaseIndicatorEntity.prototype, "indicatorType", void 0);
__decorate([
    (0, typeorm_1.Column)(),
    __metadata("design:type", String)
], BaseIndicatorEntity.prototype, "name", void 0);
__decorate([
    (0, typeorm_1.Column)(),
    __metadata("design:type", String)
], BaseIndicatorEntity.prototype, "unit", void 0);
//# sourceMappingURL=base-indicator.entity.js.map