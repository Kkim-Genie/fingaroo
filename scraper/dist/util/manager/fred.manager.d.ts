import { HttpService } from '@nestjs/axios';
export declare class FredManager {
    private readonly api;
    constructor(api: HttpService);
    getSources(): Promise<any>;
    getReleases(source: any): Promise<any>;
    getSeries(release: any): Promise<any>;
    private checkFredException;
}
