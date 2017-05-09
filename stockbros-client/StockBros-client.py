#!flask/bin/python
from flask import Flask, make_response, render_template


#Create application object
app = Flask(__name__)
#app.config["DEBUG"] = True

#########################
#Error control functions#
#########################
#TODO: CREAR RESPUESTA PARA HTML, NO JSON
#@app.errorhandler(404)
#def not_found(error):
#	return make_response(404)
	
#@app.errorhandler(400)
#def not_found(error):
#	return make_response(400)
	
@app.route('/StockBros-client')
def index():
    return render_template('index.html')
	
if __name__ == '__main__':
	app.run()
