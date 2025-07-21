import { Module } from '@nestjs/common';
import { HttpModule } from '@nestjs/axios';
import { TypeOrmModule } from '@nestjs/typeorm';
import { BondEntity } from './entity/bond.entity';
import { CryptoCurrencyEntity } from './entity/crypto-currency.entity';
import { EtfEntity } from './entity/etf.entity';
import { ForexPairEntity } from './entity/forex-pair.entity';
import { FundEntity } from './entity/fund.entity';
import { IndexEntity } from './entity/index.entity';
import { StockEntity } from './entity/stock.entity';
import { EconomyEntity } from './entity/economy.entity';
import { CommodityEntity } from './entity/commodity.entity';
import { FredManager } from './util/manager/fred.manager';
import { TwelveManager } from './util/manager/twelve.manager';
import { InvestingManager } from './util/manager/investing.manager';
import { NewsManager } from './util/manager/news.manager';
import { StockScraper } from './scraper/stock.scraper';
import { IndexScraper } from './scraper/index.scraper';
import { FundScraper } from './scraper/fund.scraper';
import { ForexPairScraper } from './scraper/forex-pair.scraper';
import { EtfScraper } from './scraper/etf.scraper';
import { EconomyScraper } from './scraper/economy.scraper';
import { CryptocurrencyScraper } from './scraper/cryptocurrency.scraper';
import { CommodityScraper } from './scraper/commodity.scraper';
import { BondScraper } from './scraper/bond.scraper';
import { MiraeAssetScraper } from './scraper/miraeasset.scraper';
import { IndicatorScheduler } from './scheduler/indicator.scheduler';
import { ConfigModule } from '@nestjs/config';
import { TypeormConfig } from './config/typeorm.config';
import { addTransactionalDataSource } from 'typeorm-transactional';
import { DataSource } from 'typeorm';
import { FutureSnowScraper } from './scraper/futuresnow.scraper';
import { NewsTodayScraper } from './scraper/newstoday.scraper';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
    }),
    HttpModule.registerAsync({
      useFactory: () => ({
        timeout: 60000,
        maxRedirects: 5,
      }),
    }),
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      useClass: TypeormConfig,
      async dataSourceFactory(options) {
        if (!options) {
          throw new Error('Invalid options passed');
        }
        return addTransactionalDataSource(new DataSource(options));
      },
    }),
    TypeOrmModule.forFeature([
      BondEntity,
      CryptoCurrencyEntity,
      EtfEntity,
      ForexPairEntity,
      FundEntity,
      IndexEntity,
      StockEntity,
      EconomyEntity,
      CommodityEntity,
    ]),
  ],
  controllers: [],
  providers: [
    FredManager,
    TwelveManager,
    InvestingManager,
    NewsManager,
    StockScraper,
    IndexScraper,
    FundScraper,
    ForexPairScraper,
    EtfScraper,
    EconomyScraper,
    CryptocurrencyScraper,
    CommodityScraper,
    BondScraper,
    MiraeAssetScraper,
    IndicatorScheduler,
    FutureSnowScraper,
    NewsTodayScraper,
  ],
})
export class AppModule {}
