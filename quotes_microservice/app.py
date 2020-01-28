from flask import Flask
from flask import request
import yfinance as yf
import json

app = Flask(__name__)

@app.route("/quote")
def display_quote():
	symbol = request.args.get('symbol')
	if symbol is None:
		symbol = "AAPL"
	quote = yf.Ticker(symbol)

	return quote.info

@app.route("/history")
def display_history():
	symbol = request.args.get('symbol')
	if symbol is None:
		symbol = "AAPL"
	quote = yf.Ticker(symbol)
	
	hist = quote.history(period="1y", interval="1mo")
	data = hist.to_json()

	return data


if __name__ == "__main__":
	app.run(debug=True)