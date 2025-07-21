import { BaseIndicatorEntity } from './common/base-indicator.entity';
export declare class CryptoCurrencyEntity extends BaseIndicatorEntity {
    availableExchanges: string[];
    currencyBase: string;
    currencyQuote: string;
}
