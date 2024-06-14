import http
from flask import Flask, jsonify
from flask_cors import CORS

from api.oanda_api import OandaAPI
from scraping.bloomberg_com import bloomberg_com
from scraping.investing_com import get_pair


app = Flask(__name__)
CORS(app)


def get_response(data):
    if data is None:
        return jsonify({'message': 'error getting data'}), http.HTTPStatus.NOT_FOUND
    else:
        return jsonify(data)


@app.route('/api/test')
def test():
    return jsonify({'message': 'hello startup!'})
    

@app.route('/api/headlines')
def headlines():
    return get_response(bloomberg_com())


@app.route('/api/account')
def account():
    return get_response(OandaAPI().get_account_summary())


@app.route('/api/technicals/<pair>')
def technicals(pair):
    data = get_pair(pair, 'dict')
    return get_response(data)
    

@app.route('/api/prices/<pair>/<granularity>/<count>')
def prices(pair, granularity, count):
    api = OandaAPI()
    dict_candles = api.web_api_candles(pair, granularity, count)
    
    return get_response(dict_candles)
    

if __name__ == '__main__':
    app.run(debug=True)
    