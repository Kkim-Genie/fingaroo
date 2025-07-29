import { NewsManager } from "src/util/manager/news.manager";
import { HttpService } from "@nestjs/axios";
export declare class NateScraper {
    private readonly newsManager;
    private readonly httpService;
    private readonly logger;
    constructor(newsManager: NewsManager, httpService: HttpService);
    scrape(): Promise<void>;
}
