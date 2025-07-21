import {
  BadRequestException,
  HttpException,
  HttpStatus,
  Injectable,
  InternalServerErrorException,
  NotFoundException,
} from '@nestjs/common';
import { HttpService } from '@nestjs/axios';

const BASE_URL = 'https://api.stlouisfed.org/fred';

@Injectable()
export class FredManager {
  constructor(private readonly api: HttpService) {}

  async getSources() {
    const sourcesUrl = `${BASE_URL}/sources?api_key=${process.env.FRED_KEY}&file_type=json`;
    const sourcesResponse = await this.api.axiosRef.get(sourcesUrl);
    this.checkFredException(sourcesResponse);
    return sourcesResponse.data;
  }

  async getReleases(source: any) {
    const releasesUrl = `${BASE_URL}/source/releases?source_id=${source.id}&api_key=${process.env.FRED_KEY}&file_type=json`;
    const releasesResponse = await this.api.axiosRef.get(releasesUrl);
    this.checkFredException(releasesResponse);
    return releasesResponse.data;
  }

  async getSeries(release: any) {
    const seriesUrl = `${BASE_URL}/release/series?release_id=${release.id}&api_key=${process.env.FRED_KEY}&file_type=json`;
    const seriesResponse = await this.api.axiosRef.get(seriesUrl);
    this.checkFredException(seriesResponse);
    return seriesResponse.data;
  }

  private checkFredException(response: any) {
    if (response.status === HttpStatus.BAD_REQUEST) {
      throw new BadRequestException(response.data.error_message);
    }
    if (response.status === HttpStatus.NOT_FOUND) {
      throw new NotFoundException(response.data.error_message);
    }
    if (response.status === HttpStatus.INTERNAL_SERVER_ERROR) {
      throw new InternalServerErrorException(response.data.error_message);
    }
    if (response.status === HttpStatus.TOO_MANY_REQUESTS) {
      throw new HttpException(
        response.data.error_message,
        HttpStatus.TOO_MANY_REQUESTS,
      );
    }
    return response;
  }
}
