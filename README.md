Collecting data
==============

Execution
---------

``$ python ipo_data.py``

Output
------

The output is composed of two directories: *all\_data* and *year_only_data*

### all_data ###

Contains the data required to determine the percent change between the adjusted closing price on the day of the company's ipo and the adjusted closing price of the date being compared against; which would most likely be set to today.

Data for each company is written out in the following format:

``(stock symbol, ipo date, price on day of ipo, price on final date)``

e.g.

``('TFSC', '2014-8-8', '9.45', '9.79')``


### year_only_data ###
Contains the data required to determine the percent change between the adjusted closing price on the day of the company's ipo and the adjusted closing price of the first trading day a year later.

Data for each company is written out in the following format:

``(stock symbol, ipo date, price on day of ipo, date of trading day a year after ipo, closing price of first trading day a year after ipo)``

e.g.

``('TFSC', '2014-8-8', '9.45', '2015-8-10', '9.70')``

**Note: All the prices used are adjusted for present day stock splits.**

### Parallelization ###
Retrieving historical data that dates a decade back for a certain company make take a while, so multiple processes are kicked off to run in parallel and reduce the execution time. The limiting factor on the number of processes that can be run is the rate limiting enforced by YQL.

The three stock exchanges investigated are NASDAQ, NYSE and AMEX. Each process is responsible for 1000 companies (at most) from a specific exchange, and is named EXCHANGE_NUM.

There are definitely many more ways to optimize this, this is just the only method I implemented.

Parsing Data
============

Execution
---------

After following the execution steps above, run the commands below.

```
  $ cat all_data/* > all_data.txt
  $ cat year_only_data/* > year_only_data.txt
  $ python ipo_data_analysis.py
```

Output
------

