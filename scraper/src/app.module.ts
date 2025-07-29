import { Module } from "@nestjs/common";
import { HttpModule } from "@nestjs/axios";

import { NewsManager } from "./util/manager/news.manager";
import { MiraeAssetScraper } from "./scraper/miraeasset.scraper";
import { NateScraper } from "./scraper/nate.scraper";
import { ConfigModule } from "@nestjs/config";

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
  ],
  controllers: [],
  providers: [NewsManager, MiraeAssetScraper, NateScraper],
})
export class AppModule {}
