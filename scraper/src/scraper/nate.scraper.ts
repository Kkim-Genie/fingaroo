import { Injectable, Logger } from "@nestjs/common";
import { NewsManager } from "src/util/manager/news.manager";
import { HttpService } from "@nestjs/axios";

@Injectable()
export class NateScraper {
  private readonly logger: Logger = new Logger(NateScraper.name);

  constructor(
    private readonly newsManager: NewsManager,
    private readonly httpService: HttpService
  ) {}

  async scrape(): Promise<void> {
    const news = await this.newsManager.loadNateNews();
    console.log("news", news.length);
    const apiUrl = `${process.env.AI_ADMIN_URL}/news`;

    try {
      const response = await this.httpService.axiosRef.post(apiUrl, { news });
      console.log("POST response:", response.data);
    } catch (error) {
      console.error("POST error:", error);
    }
  }
}
