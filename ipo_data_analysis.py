from ast import literal_eval as make_tuple
from datetime import datetime, timedelta
import io
import math
from itertools import groupby

final_close_date = datetime.strptime('2015-10-27', "%Y-%m-%d")
MAX_GROWTH = 1000

def discount_value(value, start_date, end_date, inflation_rates):
    year_range = range(end_date.year, start_date.year - 1, -1)
    value = float(value)
    for y in year_range:
        if y == end_date.year == start_date.year:
            month_range = range(end_date.month, start_date.month - 1, -1)
        elif y == start_date.year:
            month_range = range(12, start_date.month - 1, -1)
        elif y == end_date.year:
            month_range = range(end_date.month, 0, -1)
        else:
            month_range = range(12, 0, -1)
        for m in month_range:
            factor = 1.0 + float(inflation_rates[y][m]) / 100.0
            exponent = - (1.0 / 12.0)
            value *= math.pow(factor, exponent)
    return value

def compute_data_company_lifetime(raw_tuples, max_growth, inflation_rates):
  for t in raw_tuples:
    date = datetime.strptime(t[1], "%Y-%m-%d")
    date_ipo_no_day_string = "{}-{}".format(date.year, date.month)
    ipo_price = float(t[2])
    current_price = float(t[3])
    current_price_discounted = discount_value(current_price, date, final_close_date, inflation_rates)
    delta = ((current_price_discounted - ipo_price) / ipo_price)
    percent_change = delta * 100.0
    percent_change_rounded = format(percent_change, '.2f')
    data = (date_ipo_no_day_string, percent_change_rounded)

    if (float(percent_change_rounded) < max_growth):
        yield data
    else:
        print "{}\t{}".format(t[0], percent_change_rounded)

# Too lazy to update data set and function to have one function that works for both use cases
def compute_data_company_first_year(raw_tuples, max_growth, inflation_rates):
  for t in raw_tuples:
    date_ipo = datetime.strptime(t[1], "%Y-%m-%d")
    price_ipo = float(t[2])
    date_ipo_no_day_string = "{}-{}".format(date_ipo.year, date_ipo.month)

    date_year_later = datetime.strptime(t[3], "%Y-%m-%d")
    price_year_later = float(t[4])

    price_year_later_discounted = discount_value(price_year_later, date_ipo, date_year_later, inflation_rates)
    delta = ((price_year_later_discounted - price_ipo) / price_ipo)
    percent_change = delta * 100.0
    percent_change_rounded = format(percent_change, '.2f')
    data = (date_ipo_no_day_string, percent_change_rounded)

    if (float(percent_change_rounded) < max_growth):
      yield data
    
def get_inflation_rates(file_name):
    all_inflation_rates = {}
    f = open(file_name, 'r')    
    lines = f.readlines()
    for line in lines[1:]:
        split = line.strip().split()
        monthly_inflation_rates = {}
        for i in range(1, 13):
            if len(split) > i:
                monthly_inflation_rates[i] = float(split[i])
            else:
                break
        all_inflation_rates[int(split[0])] = monthly_inflation_rates

    return all_inflation_rates

def average_data(tuple_lines):
  for key, group in groupby(sorted(tuple_lines), lambda x: x[0]):
    values = [float(thing[1]) for thing in group]
    average_change = sum(values) / float(len(values))
    yield (key, average_change)

def get_sorted_average_data(file_name, inflation_rates, compute_function):
    f = open(file_name, 'r')
    raw_lines = f.readlines()
    tuple_lines = [make_tuple(line.strip()) for line in raw_lines]
    computed_data = list(compute_function(tuple_lines, MAX_GROWTH, inflation_rates))
    averaged_data = list(average_data(computed_data))
    sorted_average_data = sorted(averaged_data, key=lambda t: (int(t[0].split("-")[0]), int(t[0].split("-")[1])))
    return sorted_average_data

def write_data_to_file(file_name, data):
    f = open(file_name, 'w')
    data_strings = ["{}\t{}".format(i[0], i[1]) for i in company_lifetime_sorted_average_data]
    output = '\n'.join(data_strings)
    f.write(output)
    f.close()

inflation_rates = get_inflation_rates('inflation_rates.txt')

company_lifetime_sorted_average_data = get_sorted_average_data('all_data.txt', inflation_rates, compute_data_company_lifetime)
write_data_to_file('ipo_data_output.txt', company_lifetime_sorted_average_data)

year_after_ipo_sorted_average_data = get_sorted_average_data('year_only_data.txt', inflation_rates, compute_data_company_first_year)
write_data_to_file('ipo_data_year_only_output.txt', year_after_ipo_sorted_average_data)
