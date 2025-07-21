import { FredManager } from '../util/manager/fred.manager';
import { EconomyEntity } from '../entity/economy.entity';
import { Repository } from 'typeorm';
export declare class EconomyScraper {
    private readonly fredManager;
    private readonly economyEntityRepository;
    private readonly logger;
    private readonly BATCH_SIZE;
    private readonly FREQUENCY_WHITELIST;
    constructor(fredManager: FredManager, economyEntityRepository: Repository<EconomyEntity>);
    scrape(): Promise<void>;
}
