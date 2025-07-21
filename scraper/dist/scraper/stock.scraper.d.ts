import { TwelveManager } from '../util/manager/twelve.manager';
import { StockEntity } from '../entity/stock.entity';
import { Repository } from 'typeorm';
import { InvestingManager } from '../util/manager/investing.manager';
export declare class StockScraper {
    private readonly twelveManager;
    private readonly investingManager;
    private readonly stockEntityRepository;
    private readonly logger;
    private readonly BATCH_SIZE;
    constructor(twelveManager: TwelveManager, investingManager: InvestingManager, stockEntityRepository: Repository<StockEntity>);
    scrape(country: string): Promise<void>;
}
