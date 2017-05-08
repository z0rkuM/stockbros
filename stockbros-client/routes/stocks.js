var express = require('express');
var router = express.Router();
var stockService = require('../services/stockService.js');

/* GET stocks listing. */
router.get('/', function(req, res, next) {
  // Use the method loadStocks form stockService to get all the stocks
    stockService.loadStocks(function(stocks, err) {
        if (err) {
            console.error('Error al recuperar las acciones');
            res.render('error', {
                message: 'Se ha producido un error. Contacte con el administrador.',
                error: null
            });
        } else {
            console.log('Acciones recuperadas:', stocks);
            res.render('stocks', {stocks: stocks});
        }
    });
});

module.exports = router;
