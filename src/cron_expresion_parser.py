from typing import Set, Tuple, List

__all__ = ["CronExpressionParser"]


class CronExpressionParser:
    MAX_FIELDS_SUPPORTED = 5
    MINUTES = (0, 59)
    HOURS = (0, 23)
    DAYS_OF_MONTH = (1, 31)
    MONTHS = (1, 12)
    DAYS_OF_WEEK = (0, 6)
    RANGE_LIMITS = (MINUTES, HOURS, DAYS_OF_MONTH, MONTHS, DAYS_OF_WEEK)
    DAY_NAMES = list(zip(('SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'), range(7)))
    MONTH_NAMES = list(zip(('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                       'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'), range(1, 13)))

    def __init__(self, expression: str):
        """
        Parse valid crontab expression with 5 fields (minute,hour,day_of_month,month,day_of_week) and command)
        """

        crontab_fields_with_command = expression.split(None, self.MAX_FIELDS_SUPPORTED)
        self.split_expression = self._normalize_expression(crontab_fields_with_command)
        self._parse_crontab_expression()

    def _normalize_expression(self, crontab_fields_with_command: List) -> List:
        """
        normalize crontab expressions
        """
        # if command is missing make command as empty
        if len(crontab_fields_with_command) == self.MAX_FIELDS_SUPPORTED:
            crontab_fields_with_command.append('')

        minutes, hours, day_of_month, months, day_of_week, self.command = crontab_fields_with_command

        # `*` and `?` are synonymous for day_of_week and day_of_month. day 7 and day 0 refer to same day
        day_of_week = day_of_week.replace('7', '0').replace('?', '*')
        day_of_month = day_of_month.replace('?', '*')

        # replace month name and day names if present like jan, feb and sun, mon
        for month_str, month_num in self.MONTH_NAMES:
            months = months.upper().replace(month_str, str(month_num))

        for dow_str, dow_num in self.DAY_NAMES:
            day_of_week = day_of_week.upper().replace(dow_str, str(dow_num))

        return [minutes, hours, day_of_month, months, day_of_week]

    def _parse_crontab_expression(self) -> None:
        """
        Parse crontab string expression and set valid range in parsed_crontab_expression
        """
        self.parsed_crontab_expression = []
        for expression, min_max_range in zip(self.split_expression, self.RANGE_LIMITS):

            # expression like '1,3,5' is a range expression in itself hence doesn't need expansion
            # such expression can't have `*` since * implies match all valid range for the given field
            exp_with_comma = expression.split(',')
            if len(exp_with_comma) > 1 and "*" in exp_with_comma:
                raise ValueError("\"*\" must be alone in a field")

            # for other valid expression expand into corresponding range
            parsed_expression_set = set()
            for sub_expression in exp_with_comma:
                parsed_expression_set.update(self.calculate_range_from_expression(sub_expression, min_max_range))

            self.parsed_crontab_expression.append(parsed_expression_set)

        # Support for specifying both a day-of-week AND a day-of-month parameter is ambiguous,
        # it's a famous problem that when a crontab line contains both day of week and day of month ,
        # cron uses OR for figuring out a day to fire the command
        if self.split_expression[2] == "*" and self.split_expression[4] != "*":
            self.parsed_crontab_expression[2] = set()
        elif self.split_expression[4] == "*" and self.split_expression[2] != "*":
            self.parsed_crontab_expression[4] = set()

    @staticmethod
    def calculate_range_from_expression(range_expression_str: str, min_max_range: Tuple[int, int]) -> Set[int]:
        """
        return a set containing valid values for a given crontab range
        'min_max_range' is a two element range iterable containing the
        both-inclusive upper and lower limits of the crontab expression.
        """
        element = range_expression_str.strip()
        # default offset assume to be in steps of 1 update later for cases like 5-10/2 where offset is 2
        offset = 1
        if element == '*':
            return set(range(min_max_range[0], min_max_range[1] + 1))
        elif element.isdigit():
            # check for bounds and return digit as set (handles cases where range is specified as (1,3))
            value = int(element)
            if min_max_range[0] <= value <= min_max_range[1]:
                return {value}
            else:
                raise ValueError(f"{element} is not within valid range")
        elif '-' in element or '/' in element:
            divide = element.split('/')
            subrange = divide[0]
            if len(divide) == 2:
                # given: 1-10/5 or */1 offset should be 5 and 1 respectively
                offset = int(divide[1])

            if '-' in subrange:
                # given: 1-5
                prefix, suffix = [int(n) for n in subrange.split('-')]
                if prefix < min_max_range[0] or suffix > min_max_range[1]:
                    raise ValueError(f"{element} is not within valid range.")
            elif subrange.isdigit():
                # Handle offset increments e.g. 5/15 to run at :05, :20, :35, and :50
                return set(range(int(subrange), min_max_range[1] + 1, offset))
            elif subrange == '*':
                # Include all values with the given range
                prefix, suffix = min_max_range
            else:
                raise ValueError(f"Unrecognized symbol {subrange}")

            if prefix < suffix:
                # given: 5-7
                return set(range(prefix, suffix + 1, offset))
            else:
                # case where suffix > prefix meaning circular range. i.e [(prefix,max), (min,suffix)]
                # given: 11-5/3 and min_max_range=(1,14) = {11,14,3}
                prefix_to_max = list(range(prefix, min_max_range[1] + 1))
                min_to_suffix = list(range(min_max_range[0], suffix + 1))
                round_trip = prefix_to_max + min_to_suffix
                return set(round_trip[::offset])
        else:
            raise ValueError(f"Element {element} not in a recognized format.")

    def format_to_human_readable_std_out(self, formatter):
        return formatter(self.parsed_crontab_expression[0], self.parsed_crontab_expression[1],
                         self.parsed_crontab_expression[2], self.parsed_crontab_expression[3],
                         self.parsed_crontab_expression[4], self.command)
