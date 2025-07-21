import { BaseIndicatorEntity } from './common/base-indicator.entity';
export declare class StockEntity extends BaseIndicatorEntity {
    currency: string;
    exchange: string;
    micCode: string;
    country: string;
    type: string;
    figiCode: string;
    marketCapitalization: number;
}
