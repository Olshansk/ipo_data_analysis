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

### Parallelization ###
Retrieving historical data that dates a decade back for a certain company make take a while, so multiple processes are kicked off to run in parallel and reduce the execution time. The limiting factor on the number of processes that can be run is the rate limiting enforced by YQL.

The three stock exchanges investigated are NASDAQ, NYSE and AMEX. Each process is pulls the data for 1000 companies (at most) from a specific exchange sequentially. The output from each process is written out to a file under all_data and year_only_data named EXCHANGE_NUM.

Parsing Data
============

Execution
---------

```
  $ cat all_data/* > all_data.txt
  $ cat year_only_data/* > year_only_data.txt
  $ python ipo_data_analysis.py
```

Output
------

### ipo_data_output.txt ###
  
Average % change in stock price between close on day of IPO and the date specified in the code (November 27th, 2015). Adjusted for inflation and splits.

### ipo_data_year_only_output.txt ###
  
Average % change in stock price between close on day of IPO and on the first trading day a year after the IPO. Adjusted for inflation and splits.
