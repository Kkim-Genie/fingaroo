import { BaseIndicatorEntity } from './common/base-indicator.entity';
export declare class EconomyEntity extends BaseIndicatorEntity {
    frequency: string;
    frequencyShort: string;
    seasonalAdjustment: string;
    seasonalAdjustmentShort: string;
    unitDescription: string;
    popularity: number;
    notes: string;
}
