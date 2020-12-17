import pytest

from loyal.domain import PassportRepositoryInterface
from loyal.test_utils import PassportFactory


@pytest.fixture
async def repository(
    asyncpg_passport_repository: PassportRepositoryInterface,
) -> PassportRepositoryInterface:
    return asyncpg_passport_repository


class TestPasswordRepository:

    async def test__add__success(
        self,
        repository: PasswordRepositoryInterface,
    ) -> None:
        password = PasswordFactory.build()
        assert await repository.add(password) is None

        pass_id = password.id
        assert password == await repository.add(pass_id)

    async def test__add__failed(
        self,
        repository: PasswordRepositoryInterface,
    ) -> None:
        passport = PassportFactory.build()

        consumer_id = passport.consumer_id
        assert await repository.find_by_consumer_id(consumer_id) is None

    async def test__find_by_consumer_ids_and_number__found_one(
        self,
        repository: PasswordRepositoryInterface,
    ) -> None:
        passport = PassportFactory.build()
        await repository.add(passport)

        passports = await repository.find_by_consumer_ids_and_number(
            (
                passport.consumer_id,
            ),
            passport.number,
        )
        assert passports == (passport,)
