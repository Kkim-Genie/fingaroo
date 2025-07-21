import { HttpService } from '@nestjs/axios';
import { Injectable, Logger } from '@nestjs/common';
import { NewsManager } from 'src/util/manager/news.manager';
import { Transactional } from 'typeorm-transactional';

@Injectable()
export class FutureSnowScraper {
  private readonly logger: Logger = new Logger(FutureSnowScraper.name);

  constructor(
    private readonly newsManager: NewsManager,
    private readonly httpService: HttpService,
  ) {}

  @Transactional()
  async scrape(): Promise<void> {
    const news = await this.newsManager.loadFutureSnowNews();
    const apiUrl = `${process.env.AI_ADMIN_URL}/news`;
    try {
      const response = await this.httpService.axiosRef.post(apiUrl, { news });
      console.log('POST response:', response.data);
    } catch (error) {
      console.error('POST error:', error);
    }
  }
}
