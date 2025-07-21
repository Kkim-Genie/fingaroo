import { IndexEntity } from '../entity/index.entity';
import { Repository } from 'typeorm';
export declare class IndexScraper {
    private readonly indexEntityRepository;
    private readonly logger;
    private readonly BATCH_SIZE;
    constructor(indexEntityRepository: Repository<IndexEntity>);
    scrape(): Promise<void>;
}
