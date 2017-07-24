import { Injectable } from '@angular/core';
import { Headers, Http, RequestOptions } from '@angular/http';
import { Stock } from './class/stock';

import 'rxjs/add/operator/toPromise';
import 'rxjs/Rx';

@Injectable()
export class StocksService {

  private stocksUrl = 'http://91.117.52.106/StockBros/stocks';

    results: Stock[];

    constructor (private http: Http) {
        this.results = [];
     }

    getStocks() {
        let promise = new Promise((resolve, reject) => {

            this.http.get(this.stocksUrl, this.jwt())
                .toPromise()
                .then(
                    response => {
                        this.results = response.json().stocks.map((item: any) => {
                            return new Stock(
                                item.chart_time_period,
                                item.date_update,
                                item.market,
                                item.percent,
                                item.price,
                                item.stock,
                                item.uri
                            );
                        });
                        resolve();
                    },
                    msg => {
                        reject(msg);
                    }
                );
        });
        return promise;
    }

    private jwt() {
        // create authorization header
        const base64hash = 'Basic ' + localStorage.getItem('b64Hash');
        const headers = new Headers({ 'Authorization': base64hash });
        return new RequestOptions({ headers: headers });
    }

}
