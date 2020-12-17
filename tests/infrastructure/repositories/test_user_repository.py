from datetime import date

import pytest

from loyal.domain import Person, PersonRepositoryInterface
from loyal.test_utils import PersonFactory


@pytest.fixture
async def repository(
    asyncpg_person_repository: PersonRepositoryInterface,
) -> PersonRepositoryInterface:
    return asyncpg_person_repository


class TestPersonRepository:

    async def test__find_consumer_id__found(
        self,
        repository: PersonRepositoryInterface,
    ) -> None:
        name, patronymic, surname = "ГАЛИНА ПЕТРОВНА ВАСИЛЬКОВА".split()
        birthdate = date(1970, 1, 1)

        persons: list = PersonFactory.create_batch(
            3,
            name=name,
            surname=surname,
            patronymic=patronymic,
            birthdate=birthdate,
        )

        for person in persons:
            await repository.add(person)

        def sort_key(p: Person) -> tuple:
            return (
                p.last_credit_opened_at,
                p.last_date_credit_updated_at,
                p.score_gen_5,
            )

        persons = sorted(persons, key=sort_key, reverse=True)

        consumer_id = await repository.find_consumer_id(
            name,
            surname,
            patronymic,
            birthdate,
        )
        assert consumer_id == persons[0].consumer_id

    async def test__find_consumer_id__not_found(
        self,
        repository: PersonRepositoryInterface,
    ) -> None:
        person = PersonFactory.build()

        consumer_id = await repository.find_consumer_id(
            person.name,
            person.surname,
            person.patronymic,
            person.birthdate,
        )
        assert consumer_id is None

    async def test__find_consumer_ids__found(
        self,
        repository: PersonRepositoryInterface,
    ) -> None:
        name, patronymic, surname = "ГАЛИНА ПЕТРОВНА ВАСИЛЬКОВА".split()
        birthdate = date(1970, 1, 1)

        persons: list = PersonFactory.create_batch(
            3,
            name=name,
            surname=surname,
            patronymic=patronymic,
            birthdate=birthdate,
        )

        for person in persons:
            await repository.add(person)

        consumer_ids = await repository.find_consumer_ids(
            name,
            surname,
            patronymic,
        )
        assert consumer_ids == tuple(person.consumer_id for person in persons)

    async def test__find_consumer_ids__not_found(
        self,
        repository: PersonRepositoryInterface,
    ) -> None:
        person = PersonFactory.build()

        consumer_ids = await repository.find_consumer_ids(
            person.name,
            person.surname,
            person.patronymic,
            person.birthdate,
        )
        assert consumer_ids == tuple()
