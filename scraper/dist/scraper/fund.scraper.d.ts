import { TwelveManager } from '../util/manager/twelve.manager';
import { FundEntity } from '../entity/fund.entity';
import { Repository } from 'typeorm';
import { InvestingManager } from '../util/manager/investing.manager';
export declare class FundScraper {
    private readonly twelveManager;
    private readonly investingManager;
    private readonly fundEntityRepository;
    private readonly logger;
    private readonly BATCH_SIZE;
    constructor(twelveManager: TwelveManager, investingManager: InvestingManager, fundEntityRepository: Repository<FundEntity>);
    scrape(country: string): Promise<void>;
}
