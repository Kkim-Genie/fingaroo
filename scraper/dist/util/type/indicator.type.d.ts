import { INDICATOR_TYPE } from '../enum/indicator.enum';
export type IndicatorType = (typeof INDICATOR_TYPE)[keyof typeof INDICATOR_TYPE];
