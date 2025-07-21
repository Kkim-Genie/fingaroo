import { TwelveManager } from '../util/manager/twelve.manager';
import { EtfEntity } from '../entity/etf.entity';
import { Repository } from 'typeorm';
import { InvestingManager } from '../util/manager/investing.manager';
export declare class EtfScraper {
    private readonly twelveManager;
    private readonly investingManager;
    private readonly etfEntityRepository;
    private readonly logger;
    private readonly BATCH_SIZE;
    constructor(twelveManager: TwelveManager, investingManager: InvestingManager, etfEntityRepository: Repository<EtfEntity>);
    scrape(country: string): Promise<void>;
}
