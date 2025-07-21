import { HttpService } from '@nestjs/axios';
import { IndicatorType } from '../type/indicator.type';
export declare class TwelveManager {
    private readonly api;
    constructor(api: HttpService);
    getReferenceData(indicatorType: IndicatorType, country?: string): Promise<any>;
    getStatistics(symbol: string, micCode: string): Promise<any>;
    getExchangeRate(sourceCurrency: string, targetCurrency?: string): Promise<any>;
    private convertIndicatorTypeToTwelveIndicatorType;
    private getReferenceDataUri;
    private checkTwelveException;
}
