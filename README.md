Collecting data
###############

Execution
---------

$ python ipo.data

Output
------

The output is composed of two directories: all_data and yearly_data.

all_data contains data of this form:
  
  (stock symbol, ipo date, price on day of ipo, price on specified date)

e.g.

  ('TFSC', '2014-8-8', '9.45', '9.79')

yearly_data contains data of this form:

  (stock symbol, ipo date, price on day of ipo, date of trading day a year after ipo, closing price of trading day a year after uoi)

e.g.

  ('TFSC', '2014-8-8', '9.45', '2015-8-10', '9.70')

Note:
  All the prices used are adjusted for stock splits.

Since retrieving data historical data a decade into the past takes a while, multiple processes are executed in parallel to partition
the data being collected. The NUM_STOCKS_PER_THREAD variable controls how many stocks need to iterated over, sequantilly, per process.
The limit factor on the number of processes that can be run is the rate limiting enforced by YQL.

Collection
----------

Once the script finishes executing, the partitioned files can be merged into one shared file very simply:

$ cat all_data/* > all_data.txt
$ cat yearly_data/* > yearly_data.txt