import { COUNTRY_TYPE } from '../enum/country.enum';

export type CountryType = (typeof COUNTRY_TYPE)[keyof typeof COUNTRY_TYPE];
