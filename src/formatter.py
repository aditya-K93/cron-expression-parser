from typing import List, Union


def format_field_name(column_name: str) -> str:
    """Format a field name padded to 14 characters
    """
    return '{:14}'.format(column_name)


def format_field_value(value: Union[str, List[int]]) -> str:
    """Format a field value for nice textual output
    """
    if isinstance(value, str):
        return value
    # set is unordered in python so sort value
    return " ".join([str(num) for num in sorted(value)])


class CronFormatter:
    def __init__(self,
                 minute: List[int],
                 hour: List[int],
                 day_of_month: List[int],
                 month: List[int],
                 day_of_week: List[int],
                 command: str):
        self.minute = minute
        self.hour = hour
        self.day_of_month = day_of_month
        self.month = month
        self.day_of_week = day_of_week
        self.command = command

    def __str__(self) -> str:
        fields = [
            ('minute', self.minute),
            ('hour', self.hour),
            ('day of month', self.day_of_month),
            ('month', self.month),
            ('day of week', self.day_of_week),
            ('command', self.command)
        ]

        formatted_fields = [(format_field_name(field_name), format_field_value(
            value)) for field_name, value in fields]
        rows = [f"{field_name}{value}" for field_name, value in formatted_fields]
        return "\n".join(rows)
