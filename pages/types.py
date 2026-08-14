"""Types for page/components/modals."""

from enum import StrEnum
from typing import Literal, TypeAlias, TypeVar

# Selenium expects tuple[str, str] e.g. (By.XPATH, "//div")
Locator: TypeAlias = tuple[str, str]


class Weekday(StrEnum):
    """Enumeration for days of the week."""

    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


WorkDay: TypeAlias = Literal[
    Weekday.MONDAY,
    Weekday.TUESDAY,
    Weekday.WEDNESDAY,
    Weekday.THURSDAY,
    Weekday.FRIDAY,
]

Weekend: TypeAlias = Literal[
    Weekday.SATURDAY,
    Weekday.SUNDAY,
]

T = TypeVar("T")
DaySchedule: TypeAlias = dict[Weekday, list[T]]
