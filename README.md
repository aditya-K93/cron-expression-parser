# Cron Expression Parser

Zero dependency Cron Expression Parser python project to parse an input cron string and expands each field to show the
times at which it will run.

The standard cron format with five time fields (minute, hour, day of month, month, and day of week) plus a command is
considered. Special time strings are excluded such as "@yearly".

```
Field	          Allowed values      Allowed special characters	
Minutes     	  0–59	              * , -
Hours	          0–23	              * , -
Day of month	  1–31	              * , - ?
Month	          1–12 or JAN–DEC     * , -
Day of week       0–6 or SUN–SAT      * , - ? 
```

https://en.wikipedia.org/wiki/Cron#CRON_expression

## Usage

- Requirements: Python3 (`python3`) >=3.7
- Run the following command from within the project root directory

  $ `make run crontab="*/15 0 1,15 * 1-5 /usr/bin/find"`
- **Note**: This will create a new virtual env (.venv) in local directory and run project against the environment
- Or use python3 natively to run using

  $ `python3 cron_expression_parser_cli.py "*/15 0 1,15 * 1-5 /usr/bin/find"`

## Expected run output

    .venv/bin/python3 cron_expression_parser_cli.py "*/15 0 1,15 * 1-5 /usr/bin/find"
    minute        0 15 30 45
    hour          0
    day_of_month  1 15
    month         1 2 3 4 5 6 7 8 9 10 11 12
    day_of_week   1 2 3 4 5
    command       /user/bin/find

## Testing

- Tests are located in the test directory
- Run the following command from within the project root directory to run all tests

  $ `make test`

- Or use python3 natively to run using

  $ `python3 -m unittest  discover`

## Expected test output

  ```
    venv/bin/python3 -m unittest discover
    ..........
    ----------------------------------------------------------------------
    Ran 10 tests in 0.001s
    
    OK
```

## Help

- To get help on cron_expression_parser cli and its usage
- Run the following command from within the project root directory to get help

  $ `make help`
- Or use python3 natively to run using

  $ `python3 cron_expression_parser_cli.py -h`

## Expected help output

```
.venv/bin/python3 cron_expression_parser_cli.py -h
usage: cron_expression_parser_cli.py [-h] crontab_expression

positional arguments:
  crontab_expression  A crontab string expression, e.g. "*/15 0 1,15 * 1-5
                      /usr/bin/find"

optional arguments:
  -h, --help          show this help message and exit

make run crontab="*/15 0 1,15 * 1-5 /usr/bin/find"

```

## Makefile commands summarised

- `make clean`: remove the virtual env (.venv) and delete cache files
- `make test`:  runs the test suite
- `make run crontab="*/15 0 1,15 * 1-5 /usr/bin/find"` : runs the cron expression parser
- `make help`:  shows help on using cron_expression_parser

