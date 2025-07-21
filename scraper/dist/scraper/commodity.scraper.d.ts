import { TwelveManager } from '../util/manager/twelve.manager';
import { CommodityEntity } from '../entity/commodity.entity';
import { Repository } from 'typeorm';
export declare class CommodityScraper {
    private readonly twelveManager;
    private readonly commodityEntityRepository;
    private readonly logger;
    private readonly BATCH_SIZE;
    constructor(twelveManager: TwelveManager, commodityEntityRepository: Repository<CommodityEntity>);
    scrape(): Promise<void>;
}
