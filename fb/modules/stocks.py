#Get Current Stock Price

import json, urllib
import zope.interface

from fb.db import db

from twisted.python import log

import fb.intent as intent
from fb.modules.base import IModule, response

class StocksModule:
	zope.interface.implements(IModule)

	name="Stocks"
	description="Functionality for stock quotes"
	author="Kyle Varga (kyle.varga@bazaarvoice.com)"

	def register(self):
		intent.service.registerCommand("stock", self.stock, self, "Stock Quote", "Returns current Stock Price")
		intent.service.registerCommand("stocktopic", self.stocktopic, self, "Stock Quote  Topic", "Returns current Stock Price to Topic")

	@response
	def stock(self, bot, room, user, args):
		query = ','.join(args)
		url = "http://www.google.com/finance/info?infotype=infoquoteall&q=" + query
		print 'url= ' + url
		stock_response = urllib.urlopen(url)
		stock_results = stock_response.read()
		if len(stock_results) > 0:
			stock_results = stock_results[3:]
			stock_results = stock_results.replace('\\x26','&')
			results = json.loads(stock_results)
			msg = 'Stock Prices for ' + query + '\n'
			for data in results:
				closed = str(float(data["l"]) - float(data["c"]))
				msg += data['name'] + ' Yesterday Close: $' + closed + ' Today Open: $' + data['op'] + ' and is currently at  $' + data["l"] + ' (' + data["cp"] + '% from Close)\n'
		else:
			msg = 'No stocks found for ' + query
		return msg.strip()
		
	@response
	def stocktopic(self, bot, room, user, args):
		query = ','.join(args)
                url = "http://www.google.com/finance/info?infotype=infoquoteall&q=" + query
                print 'url= ' + url
                stock_response = urllib.urlopen(url)
                stock_results = stock_response.read()
                if len(stock_results) > 0:
                        stock_results = stock_results[3:]
                        results = json.loads(stock_results)
                        #msg = 'Stock Prices for ' + query + '\n'
                        for data in results:
                                msg = data['name'] + ' opened at $' + data['op'] + ' and is currently at  $' + data["l"] + ' (' + data["cp"] + '%)\n'
                else:
                        msg = 'No stocks found for ' + query

		room.setTopic(msg.strip())
		return False

module = StocksModule()


