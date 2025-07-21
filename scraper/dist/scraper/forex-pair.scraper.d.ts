import { TwelveManager } from '../util/manager/twelve.manager';
import { ForexPairEntity } from '../entity/forex-pair.entity';
import { Repository } from 'typeorm';
import { InvestingManager } from '../util/manager/investing.manager';
export declare class ForexPairScraper {
    private readonly twelveManager;
    private readonly investingManager;
    private readonly forexPairEntityRepository;
    private readonly logger;
    private readonly BATCH_SIZE;
    constructor(twelveManager: TwelveManager, investingManager: InvestingManager, forexPairEntityRepository: Repository<ForexPairEntity>);
    scrape(): Promise<void>;
}
