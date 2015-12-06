#! /usr/bin/python

from datetime import datetime
from multiprocessing import Process
import os
import sys
from ticker_symbols import NASDAQ, NYSE, AMEX
from yahoo_finance import Share

NUM_SECONDS_TWO_WEEKS = 1209600
NUM_WORK_DAYS_ONE_YEAR = 253
NUM_STOCKS_PER_THREAD = 1000

start_date = '2005-01-01'
end_date = '2015-10-27'

min_ipo_date = datetime.strptime('2005-01-01', "%Y-%m-%d")

stock_exchanges = [NASDAQ(), NYSE(), AMEX()]

def chunks(l, n):
  for i in xrange(0, len(l), n):
    yield l[i:i+n]

def write_and_flush(f, data):
  f.write(data)
  f.write("\n")
  f.flush()

def date_to_string(date):
  year = date.year
  month = date.month
  day = date.day

  return "{}-{}-{}".format(year, month, day)

def create_file(filename):
  if not os.path.exists(os.path.dirname(filename)):
    os.makedirs(os.path.dirname(filename))
  return open(filename, 'w')

def collect_stocks_data(stocks, ipo_to_present_name, ipo_one_year_name):
  f_all_data = create_file("all_data/{}".format(ipo_to_present_name))
  f_yearly_data = create_file("year_only_data/{}".format(ipo_one_year_name))

  for stock in stocks:
    try:
      symbol = stock.get_symbol()
      name = stock.get_name()
      share = Share(symbol)
      price = share.get_price()
    
      historical_data = share.get_historical(start_date, end_date)

      if len(historical_data) > 1:
        oldest_entry_available = historical_data[-1]
        oldest_entry_closing_price = oldest_entry_available['Adj_Close']
        oldest_entry_date = datetime.strptime(oldest_entry_available['Date'], "%Y-%m-%d")

        # Only use companies that IPOed two weeks after the first of january in 2005.
        # This was done to account for some missing data.
        if (oldest_entry_date - min_ipo_date).total_seconds() > NUM_SECONDS_TWO_WEEKS:
          ipo_date = date_to_string(oldest_entry_date)

          current_price_rounded = "%.2f" % float(price)
          ipo_price_rounded = "%.2f" % float(oldest_entry_closing_price)

          data = str((symbol, ipo_date, ipo_price_rounded, current_price_rounded))

          write_and_flush(f_all_data, data)

          if(len(historical_data) > NUM_WORK_DAYS_ONE_YEAR):
            year_after_ipo_entry = historical_data[-NUM_WORK_DAYS_ONE_YEAR]
            year_after_ipo_date = datetime.strptime(year_after_ipo_entry['Date'], "%Y-%m-%d")

            year_after_ipo_date = date_to_string(year_after_ipo_date)
            year_after_ipo_price = "%.2f" % float(year_after_ipo_entry['Adj_Close'])

            data = str((symbol, ipo_date, ipo_price_rounded, year_after_ipo_date, year_after_ipo_price))

            write_and_flush(f_yearly_data, data)
      else:
        print "{} has no historical data".format(symbol)

      continue
    except NameError as e:
      print "NameError: ", e
    except IndexError as e:
      print "IndexError: ", e
    except KeyboardInterrupt:
      raise
    except:
      print "GeneralError:", sys.exc_info()[0]
      continue

  f_all_data.close()
  f_yearly_data.close()

def collect_stock_exchange_data(stock_exchange):
  stocks_split = list(chunks(stock_exchange.get_stocks(), NUM_STOCKS_PER_THREAD))

  for i in range(len(stocks_split)):
    ipo_to_present_name = "all_{}_{}".format(stock_exchange.get_exchange_name(), str(i))
    ipo_one_year_name = "year_only_{}_{}".format(stock_exchange.get_exchange_name(), str(i))

    p = Process(target=collect_stocks_data, args=(stocks_split[i], ipo_to_present_name, ipo_one_year_name, ))
    p.start()

for stock_exchange in stock_exchanges:
  p = Process(target=collect_stock_exchange_data, args=(stock_exchange, ))
  p.start()