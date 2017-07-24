export class Stock {
  constructor(public chart_time_period: string,
              public date_update: string,
              public market: string,
              public percent: string,
              public price: string,
              public stock: string,
              public uri: string) {
  }
}