import { TwelveManager } from '../util/manager/twelve.manager';
import { BondEntity } from '../entity/bond.entity';
import { Repository } from 'typeorm';
export declare class BondScraper {
    private readonly twelveManager;
    private readonly bondEntityRepository;
    private readonly logger;
    private readonly BATCH_SIZE;
    constructor(twelveManager: TwelveManager, bondEntityRepository: Repository<BondEntity>);
    scrape(country: string): Promise<void>;
}
