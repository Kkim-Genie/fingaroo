import { OnModuleDestroy, OnModuleInit } from '@nestjs/common';
export declare class InvestingManager implements OnModuleDestroy, OnModuleInit {
    private readonly logger;
    private browser;
    private page;
    constructor();
    onModuleInit(): Promise<any>;
    onModuleDestroy(): Promise<any>;
    loadCryptocurrencyRank(): Promise<Map<string, number>>;
    loadEtfRank(): Promise<Map<string, number>>;
    loadForexPairRank(): Promise<Map<string, number>>;
    loadFundRank(): Promise<Map<string, number>>;
    loadStockRank(country: string): Promise<Map<string, number>>;
    private mapObjectToMap;
}
