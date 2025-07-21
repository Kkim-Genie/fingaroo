"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var InvestingManager_1;
Object.defineProperty(exports, "__esModule", { value: true });
exports.InvestingManager = void 0;
const common_1 = require("@nestjs/common");
const puppeteer_1 = require("puppeteer");
const country_enum_1 = require("../enum/country.enum");
let InvestingManager = InvestingManager_1 = class InvestingManager {
    constructor() {
        this.logger = new common_1.Logger(InvestingManager_1.name);
    }
    async onModuleInit() {
        this.browser = await puppeteer_1.default.launch({
            pipe: true,
            headless: true,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
            ],
        });
        this.page = await this.browser.newPage();
        await this.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36');
        await this.page.setExtraHTTPHeaders({
            'Accept-Language': 'en-US,en;q=0.9',
            Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            Referer: 'https://www.google.com/',
        });
        this.page.setDefaultNavigationTimeout(60000);
        await this.page.setRequestInterception(true);
        this.page.on('request', (req) => {
            const resourceType = req.resourceType();
            if (resourceType === 'image' ||
                resourceType === 'media' ||
                resourceType === 'font') {
                req.abort();
            }
            else {
                req.continue();
            }
        });
    }
    async onModuleDestroy() {
        if (this.page) {
            await this.page.close();
        }
        if (this.browser) {
            await this.browser.close();
        }
    }
    async loadCryptocurrencyRank() {
        try {
            await this.page.goto('https://www.investing.com/crypto/currencies', {
                waitUntil: 'networkidle2',
            });
            await new Promise((resolve) => setTimeout(resolve, 2000));
            const loadMoreButtonExists = await this.page.evaluate(() => {
                const spans = Array.from(document.querySelectorAll('span'));
                const loadMoreSpan = spans.find((span) => span.textContent && span.textContent.trim() === 'Load more');
                return !!loadMoreSpan;
            });
            if (loadMoreButtonExists) {
                await this.page.evaluate(() => {
                    const spans = Array.from(document.querySelectorAll('span'));
                    const loadMoreSpan = spans.find((span) => span.textContent && span.textContent.trim() === 'Load more');
                    if (loadMoreSpan) {
                        loadMoreSpan.click();
                        if (loadMoreSpan.parentElement) {
                            loadMoreSpan.parentElement.click();
                        }
                    }
                });
                await new Promise((resolve) => setTimeout(resolve, 2000));
            }
            const result = await this.page.evaluate(() => {
                const tables = document.querySelectorAll('table');
                let maxRowsTable = tables[0];
                let maxRows = maxRowsTable.querySelectorAll('tr').length;
                for (let i = 1; i < tables.length; i++) {
                    const rowCount = tables[i].querySelectorAll('tr').length;
                    if (rowCount > maxRows) {
                        maxRows = rowCount;
                        maxRowsTable = tables[i];
                    }
                }
                const results = [];
                const rows = maxRowsTable.querySelectorAll('tbody > tr');
                for (let i = 0; i < rows.length; i++) {
                    const row = rows[i];
                    const cells = row.querySelectorAll('td');
                    if (cells.length >= 4) {
                        const cell = cells[3];
                        const spans = cell.querySelectorAll('span');
                        if (spans.length > 1) {
                            const symbol = spans[1].textContent?.trim() || '';
                            if (symbol && symbol.length > 0 && symbol.length <= 10) {
                                results.push({ rank: i, symbol });
                                continue;
                            }
                        }
                        const divs = cell.querySelectorAll('div');
                        if (divs.length > 1) {
                            const div = divs[1];
                            const divSpans = div.querySelectorAll('span');
                            if (divSpans.length > 1) {
                                const symbol = divSpans[1].textContent?.trim() || '';
                                if (symbol && symbol.length > 0 && symbol.length <= 10) {
                                    results.push({ rank: i, symbol });
                                    continue;
                                }
                            }
                        }
                        const cellText = cell.textContent?.trim() || '';
                        const symbolMatch = cellText.match(/[A-Z]{2,8}/);
                        if (symbolMatch && symbolMatch[0]) {
                            results.push({ rank: i, symbol: symbolMatch[0] });
                        }
                    }
                }
                return results;
            });
            return this.mapObjectToMap(result);
        }
        catch (error) {
            this.logger.error(`크롤링 중 오류 발생: ${error.message}`);
            throw new Error(`암호화폐 데이터를 가져오는 중 오류가 발생했습니다: ${error.message}`);
        }
    }
    async loadEtfRank() {
        try {
            await this.page.goto('https://www.investing.com/etfs/usa-etfs', {
                waitUntil: 'networkidle2',
            });
            await new Promise((resolve) => setTimeout(resolve, 2000));
            const etfData = await this.page.evaluate(() => {
                const etfTable = document.getElementById('etfs');
                if (!etfTable) {
                    const tables = Array.from(document.querySelectorAll('table'));
                    for (const table of tables) {
                        if (table.className.includes('etfs') ||
                            table.getAttribute('data-test') === 'etf-table' ||
                            table.querySelector('th')?.textContent?.includes('ETF')) {
                            return extractFromTable(table);
                        }
                    }
                    if (tables.length > 0) {
                        let largestTable = tables[0];
                        let maxRows = largestTable.querySelectorAll('tr').length;
                        for (let i = 1; i < tables.length; i++) {
                            const rowCount = tables[i].querySelectorAll('tr').length;
                            if (rowCount > maxRows) {
                                maxRows = rowCount;
                                largestTable = tables[i];
                            }
                        }
                        return extractFromTable(largestTable);
                    }
                    return [];
                }
                return extractFromTable(etfTable);
                function extractFromTable(table) {
                    const results = [];
                    const rows = table.querySelectorAll('tbody > tr');
                    for (let i = 0; i < rows.length; i++) {
                        const row = rows[i];
                        const symbolCells = Array.from(row.querySelectorAll('td')).filter((td) => td.className.includes('symbol'));
                        if (symbolCells.length > 0) {
                            const aTag = symbolCells[0].querySelector('a');
                            if (aTag) {
                                const symbol = aTag.textContent?.trim() || '';
                                if (symbol) {
                                    results.push({ rank: i, symbol });
                                    continue;
                                }
                            }
                        }
                        const cells = row.querySelectorAll('td');
                        for (const cell of cells) {
                            const aTag = cell.querySelector('a');
                            if (aTag) {
                                const text = aTag.textContent?.trim() || '';
                                if (/^[A-Z]{2,5}$/.test(text)) {
                                    results.push({ rank: i, symbol: text });
                                    break;
                                }
                            }
                        }
                    }
                    return results;
                }
            });
            return this.mapObjectToMap(etfData);
        }
        catch (error) {
            this.logger.error(`ETF 크롤링 중 오류 발생: ${error.message}`);
            throw new Error(`ETF 데이터를 가져오는 중 오류가 발생했습니다: ${error.message}`);
        }
    }
    async loadForexPairRank() {
        try {
            await this.page.goto('https://www.investing.com/currencies/streaming-forex-rates-majors', {
                waitUntil: 'networkidle2',
            });
            await new Promise((resolve) => setTimeout(resolve, 2000));
            const largestTableIndex = await this.page.evaluate(() => {
                const tables = document.querySelectorAll('table');
                if (tables.length === 0)
                    return -1;
                let maxIndex = 0;
                let maxRows = tables[0].querySelectorAll('tr').length;
                for (let i = 1; i < tables.length; i++) {
                    const rowCount = tables[i].querySelectorAll('tr').length;
                    if (rowCount > maxRows) {
                        maxRows = rowCount;
                        maxIndex = i;
                    }
                }
                return maxIndex;
            });
            if (largestTableIndex === -1)
                return this.mapObjectToMap([]);
            const forexData = await this.page.evaluate((tableIndex) => {
                const results = [];
                try {
                    const tables = document.querySelectorAll('table');
                    const table = tables[tableIndex];
                    const rows = table.querySelectorAll('tbody > tr');
                    for (let i = 0; i < rows.length; i++) {
                        const row = rows[i];
                        const cells = row.querySelectorAll('td');
                        if (cells.length <= 1)
                            continue;
                        const cell = cells[1];
                        const cellText = cell.textContent?.trim() || '';
                        const currencyPairRegex = /[A-Z]{3}\/[A-Z]{3}/;
                        const matches = cellText.match(currencyPairRegex);
                        if (matches && matches[0]) {
                            results.push({ rank: i, symbol: matches[0] });
                            continue;
                        }
                        const div = cell.querySelector('div');
                        if (!div)
                            continue;
                        const a = div.querySelector('a');
                        if (!a)
                            continue;
                        const h4 = a.querySelector('h4');
                        if (!h4)
                            continue;
                        const spans = h4.querySelectorAll('span');
                        if (spans.length <= 1)
                            continue;
                        const span = spans[1];
                        const symbol = span.textContent?.trim() || '';
                        if (symbol)
                            results.push({ rank: i, symbol: symbol });
                    }
                    return results;
                }
                catch (error) {
                    this.logger.error(error);
                    return results;
                }
            }, largestTableIndex);
            return this.mapObjectToMap(forexData);
        }
        catch (error) {
            this.logger.error(`Forex Pair 크롤링 중 오류 발생: ${error.message}`);
            throw new Error(`Forex Pair 데이터를 가져오는 중 오류가 발생했습니다: ${error.message}`);
        }
    }
    async loadFundRank() {
        try {
            await this.page.goto('https://www.investing.com/funds/major-funds', {
                waitUntil: 'networkidle2',
            });
            await new Promise((resolve) => setTimeout(resolve, 2000));
            const fundData = await this.page.evaluate(() => {
                const fundTable = document.getElementById('cr_fund');
                if (!fundTable) {
                    const tables = Array.from(document.querySelectorAll('table'));
                    for (const table of tables) {
                        if (table.className.includes('funds') ||
                            table.getAttribute('data-test') === 'fund-table' ||
                            table.querySelector('th')?.textContent?.includes('Fund')) {
                            return extractFromTable(table);
                        }
                    }
                    if (tables.length > 0) {
                        let largestTable = tables[0];
                        let maxRows = largestTable.querySelectorAll('tr').length;
                        for (let i = 1; i < tables.length; i++) {
                            const rowCount = tables[i].querySelectorAll('tr').length;
                            if (rowCount > maxRows) {
                                maxRows = rowCount;
                                largestTable = tables[i];
                            }
                        }
                        return extractFromTable(largestTable);
                    }
                    return [];
                }
                return extractFromTable(fundTable);
                function extractFromTable(table) {
                    const results = [];
                    const rows = table.querySelectorAll('tbody > tr');
                    for (let i = 0; i < rows.length; i++) {
                        const row = rows[i];
                        const symbolCells = Array.from(row.querySelectorAll('td')).filter((td) => td.className.includes('symbol'));
                        if (symbolCells.length > 0) {
                            const symbol = symbolCells[0].textContent?.trim() || '';
                            if (symbol) {
                                results.push({ rank: i, symbol });
                                continue;
                            }
                        }
                        const cells = row.querySelectorAll('td');
                        for (let j = 0; j < Math.min(3, cells.length); j++) {
                            const cell = cells[j];
                            const text = cell.textContent?.trim() || '';
                            if (/^[A-Z0-9]{2,10}$/.test(text)) {
                                results.push({ rank: i, symbol: text });
                                break;
                            }
                        }
                    }
                    return results;
                }
            });
            return this.mapObjectToMap(fundData);
        }
        catch (error) {
            this.logger.error(`Fund 크롤링 중 오류 발생: ${error.message}`);
            throw new Error(`Fund 데이터를 가져오는 중 오류가 발생했습니다: ${error.message}`);
        }
    }
    async loadStockRank(country) {
        try {
            const countries = [
                { name: country_enum_1.COUNTRY_TYPE.UNITED_STATES, id: '5', globalRank: 300 },
                { name: country_enum_1.COUNTRY_TYPE.CHINA, id: '37', globalRank: 100 },
                { name: country_enum_1.COUNTRY_TYPE.SOUTH_KOREA, id: '11', globalRank: 200 },
            ];
            const allStocks = [];
            let globalRank = countries.find((c) => c.name === country)?.globalRank;
            const countryId = countries.find((c) => c.name === country)?.id;
            await this.page.goto(`https://www.investing.com/stock-screener/?sp=country::${countryId}|sector::a|industry::a|equityType::a%3Ceq_market_cap;1`, { waitUntil: 'networkidle2' });
            await this.page.waitForSelector('#screenerTableWrapper', {
                timeout: 10000,
            });
            const countryStocks = await this.page.evaluate(() => {
                const results = [];
                const tableWrapper = document.querySelector('#screenerTableWrapper');
                const rows = tableWrapper.querySelectorAll('tbody tr');
                for (let i = 0; i < rows.length && results.length < 100; i++) {
                    const row = rows[i];
                    const symbolCell = row.querySelector('th div.flex.items-center a');
                    results.push(symbolCell.textContent.split(' ')[0]);
                }
                return results;
            });
            countryStocks.forEach((symbol) => {
                allStocks.push({
                    symbol: symbol,
                    rank: globalRank--,
                });
                if (allStocks.length >= 300)
                    return;
            });
            return this.mapObjectToMap(allStocks);
        }
        catch (error) {
            this.logger.error(`주식 순위 크롤링 중 오류 발생: ${error.message}`);
            throw new Error(`주식 순위 데이터를 가져오는 중 오류가 발생했습니다: ${error.message}`);
        }
    }
    mapObjectToMap(rankObject) {
        return rankObject.reduce((map, item) => {
            map.set(item.symbol, item.rank);
            return map;
        }, new Map());
    }
};
exports.InvestingManager = InvestingManager;
exports.InvestingManager = InvestingManager = InvestingManager_1 = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [])
], InvestingManager);
//# sourceMappingURL=investing.manager.js.map