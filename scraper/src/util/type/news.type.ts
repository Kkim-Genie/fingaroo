import { NEWS_TYPE } from '../enum/news.enum';
export type NewsType = (typeof NEWS_TYPE)[keyof typeof NEWS_TYPE];

export type News = {
  date: string;
  title: string;
  link: string;
  content: string;
  company: string;
  keywords: string;
};
