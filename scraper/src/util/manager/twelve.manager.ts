import {
  BadRequestException,
  HttpException,
  HttpStatus,
  Injectable,
  NotFoundException,
  NotImplementedException,
} from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { IndicatorType } from '../type/indicator.type';
import { INDICATOR_TYPE } from '../enum/indicator.enum';

const BASE_URL = 'https://api.twelvedata.com';

@Injectable()
export class TwelveManager {
  constructor(private readonly api: HttpService) {}

  async getReferenceData(indicatorType: IndicatorType, country: string = null) {
    const requestUrl = this.getReferenceDataUri(indicatorType, country);
    const response = await this.api.axiosRef.get(requestUrl);
    return this.checkTwelveException(response.data);
  }

  async getStatistics(symbol: string, micCode: string) {
    const requestUrl: string = `${BASE_URL}/statistics?symbol=${symbol}&mic_code=${micCode}&apikey=${process.env.TWELVE_KEY}`;
    const response = await this.api.axiosRef.get(requestUrl);
    return this.checkTwelveException(response.data);
  }

  async getExchangeRate(
    sourceCurrency: string,
    targetCurrency: string = 'USD',
  ) {
    const requestUrl: string = `${BASE_URL}/exchange_rate?symbol=${sourceCurrency}/${targetCurrency}&apikey=${process.env.TWELVE_KEY}`;
    const response = await this.api.axiosRef.get(requestUrl);
    return this.checkTwelveException(response.data);
  }

  private convertIndicatorTypeToTwelveIndicatorType(
    indicatorType: IndicatorType,
  ): string {
    if (indicatorType === INDICATOR_TYPE.STOCK_TYPE) return 'stocks';
    if (indicatorType === INDICATOR_TYPE.FOREX_PAIR_TYPE) return 'forex_pairs';
    if (indicatorType === INDICATOR_TYPE.CRYPTOCURRENCY_TYPE)
      return 'cryptocurrencies';
    if (indicatorType === INDICATOR_TYPE.FUND_TYPE) return 'funds';
    if (indicatorType === INDICATOR_TYPE.BOND_TYPE) return 'bonds';
    if (indicatorType === INDICATOR_TYPE.ETF_TYPE) return 'etfs';
    if (indicatorType === INDICATOR_TYPE.COMMODITY_TYPE) return 'commodities';
    if (indicatorType === INDICATOR_TYPE.INDEX_TYPE) return 'indices';
  }

  private getReferenceDataUri(
    indicatorType: IndicatorType,
    country: string = null,
  ): string {
    const convertedIndicatorType =
      this.convertIndicatorTypeToTwelveIndicatorType(indicatorType);
    if (
      indicatorType === INDICATOR_TYPE.STOCK_TYPE ||
      indicatorType === INDICATOR_TYPE.FUND_TYPE ||
      indicatorType === INDICATOR_TYPE.BOND_TYPE ||
      indicatorType === INDICATOR_TYPE.ETF_TYPE
    ) {
      return `${BASE_URL}/${convertedIndicatorType}?country=${country}&apikey=${process.env.TWELVE_KEY}`;
    } else if (
      indicatorType === INDICATOR_TYPE.FOREX_PAIR_TYPE ||
      indicatorType === INDICATOR_TYPE.CRYPTOCURRENCY_TYPE ||
      indicatorType === INDICATOR_TYPE.COMMODITY_TYPE
    ) {
      return `${BASE_URL}/${convertedIndicatorType}?apikey=${process.env.TWELVE_KEY}`;
    }
    throw new NotImplementedException(
      '시스템에 등록되지 않은 Asset Type 입니다.',
    );
  }

  private checkTwelveException(responseBody: any) {
    if (responseBody.status === 'error') {
      if (responseBody.code === HttpStatus.BAD_REQUEST) {
        throw new BadRequestException();
      }
      if (responseBody.code === HttpStatus.NOT_FOUND) {
        throw new NotFoundException('');
      }
      if (responseBody.code === HttpStatus.TOO_MANY_REQUESTS) {
        throw new HttpException(
          'Too Many Requests for Twelve Data API',
          HttpStatus.TOO_MANY_REQUESTS,
        );
      }
    }
    return responseBody;
  }
}
