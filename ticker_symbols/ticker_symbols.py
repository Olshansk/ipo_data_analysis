import abc
import os.path
import urllib2
import pickle

class Base(object):
  __metaclass__ = abc.ABCMeta

  def __init__(self, force_remote_load = False):
    if force_remote_load or not os.path.isfile(self.get_file_name()):
      self.load_remote_data()
      self.write_stocks_to_file()
    else:
      self.read_stocks_from_file()

  @staticmethod
  def remove_quotations(string):
    return string.replace('"', '')

  def load_remote_data(self):
    req = urllib2.Request(self.get_url(), headers={'User-Agent' : "Magic Browser"}) 
    raw_data = urllib2.urlopen(req)
    data = raw_data.read().split('\n')
    legend = [Base.remove_quotations(sym) for sym in data[0].split(',')]
    ticker_data = data[1:]
    tickers = []
    for raw_ticker_data in ticker_data:
      ticker_data = [Base.remove_quotations(data) for data in raw_ticker_data.split(',')]
      tickers.append(Stock(legend, ticker_data))
    self.tickers = tickers

  def get_stocks(self):
    return self.tickers

  def write_stocks_to_file(self):
    pickle.dump(self.tickers, open(self.get_file_name(), "wb"))

  def read_stocks_from_file(self):
    self.tickers = pickle.load(open(self.get_file_name(), "rb"))

  @abc.abstractmethod
  def get_url(self):
    pass

  @abc.abstractmethod
  def get_file_name(self):
    pass

  @abc.abstractmethod
  def get_exchange_name(self):
    pass

class NASDAQ(Base):
  def __init__(self, force_remote_load = False):
    Base.__init__(self, force_remote_load)

  def get_url(self):
    return 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'

  def get_file_name(self):
    return 'NASDAQ_SYMBOLS.p'

  def get_exchange_name(self):
    return 'NASDAQ'

class NYSE(Base):
  def __init__(self, force_remote_load = False):
    Base.__init__(self, force_remote_load)

  def get_url(self):
    return 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download'

  def get_file_name(self):
    return 'NYSE_SYMBOLS.p'

  def get_exchange_name(self):
    return 'NYSE'

class AMEX(Base):
  def __init__(self, force_remote_load = False):
    Base.__init__(self, force_remote_load)

  def get_url(self):
    return 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download'

  def get_file_name(self):
    return 'AMEX_SYMBOLS.p'

  def get_exchange_name(self):
    return 'AMEX'

class Stock(object):

  def __init__(self, legend, data):
    self.data = dict(zip(legend, data))

  def get_symbol(self):
    return self.data['Symbol']

  def get_name(self):
    try:
      return self.data['Name']
    except:
      return None

  def get_last_sale(self):
    return self.data['LastSale']

  def get_market_cap(self):
    return self.data['MarketCap']

  def get_ipo_year(self):
    return self.data['IPOyear']

  def get_sector(self):
    return self.data['Sector']

  def get_industry(self):
    return self.data['industry']

  def get_summary_quote(self):
    return self.data['Summary Quote']