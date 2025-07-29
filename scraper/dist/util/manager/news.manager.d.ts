import { OnModuleDestroy, OnModuleInit } from "@nestjs/common";
import { News } from "../type/news.type";
import { HttpService } from "@nestjs/axios";
export declare class NewsManager implements OnModuleDestroy, OnModuleInit {
    private readonly api;
    private readonly logger;
    private browser;
    private page;
    constructor(api: HttpService);
    onModuleInit(): Promise<any>;
    onModuleDestroy(): Promise<any>;
    loadMiraeAssetNews(): Promise<News[]>;
    loadNateNews(): Promise<News[]>;
}
