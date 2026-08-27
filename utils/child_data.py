"""Utilities for generating test data."""

from dataclasses import dataclass
import random
import uuid


FIRST_NAMES = ["Alex", "Emma", "Daniel", "Sofia", "Max", "Olivia"]
LAST_NAMES = ["Johnson", "Smith", "Brown", "Taylor", "Wilson"]


@dataclass
class ChildData:
    """Test data for a child."""

    first_name: str
    last_name: str
    age: int

    @property
    def full_name(self) -> str:
        """Return child's full name."""

        return f"{self.first_name} {self.last_name}"

    @property
    def displayed_info(self) -> str:
        """Return child information as displayed in the UI."""

        return f"{self.full_name}, {self.age}"


def generate_child() -> ChildData:
    """Generate unique test data for a child."""

    return ChildData(
        first_name=f"{random.choice(FIRST_NAMES)}{uuid.uuid4().hex[:4]}",
        last_name=f"{random.choice(LAST_NAMES)}{uuid.uuid4().hex[:4]}",
        age=random.randint(5, 16),
    )