import argparse
from src.cron_expresion_parser import CronExpressionParser
from src.formatter import CronFormatter
import logging


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)
    logger = logging.getLogger("cron_expression_parser")

    parser = argparse.ArgumentParser()
    parser.add_argument("crontab_expression", type=str,
                        help="A crontab string expression, e.g. \"*/15 0 1,15 * 1-5 /usr/bin/find\"")
    args = parser.parse_args()

    try:
        print(CronExpressionParser(args.crontab_expression).format_to_human_readable_std_out(formatter=CronFormatter))
    except Exception as e:
        logger.exception(f"Failed to parse the input str{e}")


if __name__ == '__main__':
    main()
