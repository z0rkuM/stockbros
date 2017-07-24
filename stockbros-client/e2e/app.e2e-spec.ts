import { StockBrosClientPage } from './app.po';

describe('stock-bros-client App', () => {
  let page: StockBrosClientPage;

  beforeEach(() => {
    page = new StockBrosClientPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
