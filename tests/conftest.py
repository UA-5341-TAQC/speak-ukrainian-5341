"""Root pytest configuration.

The shared fixtures live in the project-level ``fixtures`` package and are
re-exported here so they are visible to every test in the ``tests`` directory.
pytest auto-loads conftest.py files it finds, so the fixtures module must not
be registered twice via ``pytest_plugins`` - re-exporting the fixture
functions is enough.
"""

from fixtures.conftest import authenticated_driver, driver

__all__ = ["authenticated_driver", "driver"]