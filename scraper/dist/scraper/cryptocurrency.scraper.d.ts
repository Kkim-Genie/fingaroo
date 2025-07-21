import { TwelveManager } from '../util/manager/twelve.manager';
import { CryptoCurrencyEntity } from '../entity/crypto-currency.entity';
import { Repository } from 'typeorm';
import { InvestingManager } from '../util/manager/investing.manager';
export declare class CryptocurrencyScraper {
    private readonly twelveManager;
    private readonly investingManager;
    private readonly cryptoCurrencyEntityRepository;
    private readonly logger;
    private readonly BATCH_SIZE;
    constructor(twelveManager: TwelveManager, investingManager: InvestingManager, cryptoCurrencyEntityRepository: Repository<CryptoCurrencyEntity>);
    scrape(): Promise<void>;
}
