import { BaseEntity } from './base.entity';
import { IndicatorType } from '../../util/type/indicator.type';
export declare abstract class BaseIndicatorEntity extends BaseEntity {
    id: string;
    index: number;
    extraIndex: number;
    symbol: string;
    indicatorType: IndicatorType;
    name: string;
    unit: string;
}
