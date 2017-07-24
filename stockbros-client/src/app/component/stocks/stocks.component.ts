import { Component, OnInit } from '@angular/core';

import { StocksService } from '../../service/stocks.service';

@Component({
  selector: 'app-stocks',
  templateUrl: './stocks.component.html',
  styleUrls: ['./stocks.component.css']
})
export class StocksComponent implements OnInit {

  constructor(
    private stocksService: StocksService
  ) { }

  ngOnInit() {
    console.log('************************Inicio*******************************');
    this.stocksService.getStocks();
    console.log('*************************Fin*********************************');
    console.log('stocks number: ' + this.stocksService.results.length);
  }

}
