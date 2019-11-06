# etl_for_btc
ETL operations for BTC data, and a web service, which is calling an external interface

## Introduction
This repository contains 2 projects in 2 different subfolders. The first one - "btc_etl" makes 1:1 what was described in the task: 
various ETL operations on bitcoin (BTC) data from a CSV file, and visualization of data in a line graph. For the realization of the solution `pandas` and `matplotlib` packages of Python were used. Projects consists of just 1 script.

This script makes amongst other operations a currency conversion. A default rate was given with the task. But I decided to develop a separate service, which is a `Flask` web application, calling an external API for the actual rate. The first program can call this web application, and in case of connection error or timeout it uses the given default rate.

## Documentation of code 
The code is well-documented, with use of various docstring. NumPy/SciPy style was chosen. Modules, public methods and functions, their arguments in both projects have docstring, which could be then collected with `pydoc`. 

## Execution / deployment
There are 3 possibilities to execute the script, which executes ETL operations on BTC data: 

1. Clone repository and execute the `etl_for_btc\btc_etl\app\btc.py` directly. In this case the Flask app (`api_caller\app\api_caller.py`) will not be deployed, and the `btc` script will use the default value. No arguments are needed to run the script from the console. The scripts saves 2 output files (transformed data in `"etl_for_btc\btc_etl\output\btc-last-year.csv"` and graph in `"prices_of_BTC_past_year.png"`).
2. 
3. Deploy both apps with docker-compose. Then you can see, how the `btc` app sends request to the `api_caller` app and gets the exchange rate. In this case you will find the output files in the volume. You will have to stop the `api_caller` app manually, while `btc` app finishes automatically.

If you just want to see the output files without executing any code, please take a look at the `"etl_for_btc\btc_etl\output"` folder.

## Testing
For both apps unit tests were written, using the `unittest` package from Python's standard library. Respective modules with unit tests can be called directly. Tests and all relevant files (dummy data, certificates for HTTP connection) lie in the "test" folders in both project subfolders. 

## To be improved 
It is clear, that since it is just a demonstration app for a very small task, and made in short term, there are some things that could be done better. These are just some things that could be done better: 
- division of logic into class may be probably better.
- `btc` app can not just call the `api_caller` service, but give arguments: URL and pattern for extraxting the required value.
- Unit tests lack proper documentation, although names of the tests should prodvide you with understanding of what they are testing.
- Unit tests are not being executed automatically, e.g. with a Travis CI script.
- In ideal case 2 projects should have each own repository. 
