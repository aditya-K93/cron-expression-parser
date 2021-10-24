import unittest
from src.cron_expresion_parser import CronExpressionParser
from src.formatter import CronFormatter


class CronExpressionParserUnitTest(unittest.TestCase):

    def test_crontab_expression_parser(self):
        cron_exp1 = CronExpressionParser("*/15 0 1,15 * 1-5 /usr/bin/find")
        expected_min = {0, 15, 30, 45}
        expected_hour = {0}
        expected_dom = {1, 15}
        expected_month = set(range(1, 13))
        expected_dow = {1, 2, 3, 4, 5}
        expected_command = '/usr/bin/find'
        parsed_exp_range = cron_exp1.parsed_crontab_expression
        formatted_range = CronFormatter(parsed_exp_range[0], parsed_exp_range[1], parsed_exp_range[2],
                                        parsed_exp_range[3], parsed_exp_range[4], cron_exp1.command)

        self.assertEqual(set(formatted_range.minute), expected_min)
        self.assertEqual(set(formatted_range.hour), expected_hour)
        self.assertEqual(set(formatted_range.day_of_month), expected_dom)
        self.assertEqual(set(formatted_range.month), expected_month)
        self.assertEqual(set(formatted_range.day_of_week), expected_dow)
        self.assertEqual(formatted_range.command, expected_command)

    def test_parsed_crontab_expression(self):
        cron_exp1 = CronExpressionParser("*/15 0 1,15 * 1-5")
        cron_exp2 = CronExpressionParser("*/5 23-2 5 8 *")
        self.assertNotEqual(cron_exp1.split_expression, cron_exp2.split_expression)
        self.assertNotEqual(cron_exp1.parsed_crontab_expression, cron_exp2.parsed_crontab_expression)
        cron_exp1.split_expression = cron_exp2.split_expression
        cron_exp1._parse_crontab_expression()
        self.assertEqual(cron_exp1.split_expression, cron_exp2.split_expression)
        self.assertEqual(cron_exp1.parsed_crontab_expression, cron_exp2.parsed_crontab_expression)

    def test_crontab_expression_range_expander(self):
        input_expect = [
            (('1/4', (0, 23)), {1, 5, 9, 13, 17, 21}),
            (('*/15', (0, 59)), {0, 15, 30, 45}),
            (('10-5/2', (5, 13)), {10, 12, 5}),
            (('5-10/2', (1, 20)), {5, 7, 9}),
            (('10-5/3', (1, 11)), {10, 2, 5}),
            (('*', (0, 7)), set(range(0, 8))),
            (('2', (1, 7)), {2}),
            (('1-10', (1, 20)), set(range(1, 11))),
            (('9-5', (1, 12)), {9, 10, 11, 12, 1, 2, 3, 4, 5}),
            (('10/20', (0, 100)), {10, 30, 50, 70, 90}),
        ]

        for input_expression_with_bounds, expected_range in input_expect:
            self.assertEqual(expected_range,
                             CronExpressionParser.calculate_range_from_expression(
                                 *input_expression_with_bounds))

    def test_asterisk_cannot_be_combined(self):
        self.assertRaises(ValueError,
                          CronExpressionParser, "* *,1-9 * * *")

    def test_minutes_out_of_range(self):
        self.assertRaises(ValueError,
                          CronExpressionParser, "61 * * * *")

    def test_hours_out_of_range(self):
        self.assertRaises(ValueError,
                          CronExpressionParser, "* 25 * * *")

    def test_day_of_month_out_of_range(self):
        self.assertRaises(ValueError,
                          CronExpressionParser, "* * 32 * *")

    def test_month_out_of_range(self):
        self.assertRaises(ValueError,
                          CronExpressionParser, "* * * 13 *")

    def test_day_of_week_out_of_range(self):
        self.assertRaises(ValueError,
                          CronExpressionParser, "* * * * 8")

    def test_fail_missing_fields(self):
        items = ["*", "* *", "* * *", "* * * *"]
        for item in items:
            self.assertRaises(ValueError, CronExpressionParser, item)


if __name__ == "__main__":
    unittest.main()
