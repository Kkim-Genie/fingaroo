import { HttpService } from '@nestjs/axios';
import { NewsManager } from 'src/util/manager/news.manager';
export declare class NewsTodayScraper {
    private readonly newsManager;
    private readonly httpService;
    private readonly logger;
    constructor(newsManager: NewsManager, httpService: HttpService);
    scrape(): Promise<void>;
}
