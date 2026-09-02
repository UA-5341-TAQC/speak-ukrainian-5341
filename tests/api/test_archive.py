import allure
from jsonschema import validate

from api.archive_client import ArchiveClient
from api.schemas.archive_schema import ARCHIVE_SCHEMA


@allure.feature("API")
@allure.story("Archive")
@allure.title("Successful retrieval of all archives")
def test_get_archives(archive_client: ArchiveClient):
    """Verify successful retrieval of all archives."""
    with allure.step("Get all archives"):
        response = archive_client.get_archives()

    with allure.step("Verify successful response"):
        assert response.status_code == 200

    with allure.step("Verify response schema"):
        validate(
            instance=response.json(),
            schema=ARCHIVE_SCHEMA,
        )


@allure.feature("API")
@allure.story("Archive")
@allure.title("Successful retrieval of archives by class name")
def test_get_archives_by_class_name(
    archive_client: ArchiveClient,
):
    """Verify successful retrieval of archives by class name."""
    with allure.step("Get all archives"):
        response = archive_client.get_archives()

    assert response.status_code == 200

    archives = response.json()
    assert archives, "Archive list is empty."

    class_name = archives[0]["className"]

    with allure.step(
        f"Get archives by class name: {class_name}",
    ):
        response = archive_client.get_archives_by_class_name(
            class_name,
        )

    with allure.step("Verify successful response"):
        assert response.status_code == 200

    with allure.step("Verify response schema"):
        archives_by_class_name = response.json()

        validate(
            instance=archives_by_class_name,
            schema=ARCHIVE_SCHEMA,
        )

    with allure.step("Verify returned archives belong to requested class"):
        for archive in archives_by_class_name:
            assert archive["className"] == class_name