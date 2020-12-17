from datetime import date

from loyal.domain import (
    MatchingService,
    MatchingStatus,
    normalize_person_name,
)
from loyal.test_utils import PassportFactory, PersonFactory


class TestAccountService:

    async def test__match_passport_by_person___hit_with_correct_keys(
        self,
        account_service: AccountService,
    ) -> None:
        person = PersonFactory.build()
        passport = PassportFactory.build(consumer_id=person.consumer_id)

        await matching_service.persons.add(person)
        await matching_service.passports.add(passport)

        assert passport == await matching_service.match_passport_by_person(
            person.name,
            person.surname,
            person.patronymic,
            person.birthdate,
        )

    async def test__match_passport_by_person__hit_with_incorrect_keys(
        self,
        matching_service: MatchingService,
    ) -> None:
        surname, name, patronymic = "Цой Алексей Ёжикович".split()

        person = PersonFactory.build(
            name=normalize_person_name(name),
            surname=normalize_person_name(surname),
            patronymic=normalize_person_name(patronymic),
        )
        passport = PassportFactory.build(consumer_id=person.consumer_id)

        await matching_service.persons.add(person)
        await matching_service.passports.add(passport)

        assert passport == await matching_service.match_passport_by_person(
            name,
            surname,
            patronymic,
            person.birthdate,
        )

    async def test__match_passport_by_person__no_hit_consumer(
        self,
        matching_service: MatchingService,
    ) -> None:
        person = PersonFactory.build()

        passport = await matching_service.match_passport_by_person(
            person.name,
            person.surname,
            person.patronymic,
            person.birthdate,
        )
        assert passport is None

    async def test__match__no_hit_passport(
        self,
        matching_service: MatchingService,
    ) -> None:
        person = PersonFactory.build()
        await matching_service.persons.add(person)

        passport = await matching_service.match_passport_by_person(
            person.name,
            person.surname,
            person.patronymic,
            person.birthdate,
        )
        assert passport is None

    async def test__match_status_by_person_passport__full_hit(
        self,
        matching_service: MatchingService,
    ) -> None:
        person = PersonFactory.build()
        passport = PassportFactory.build(consumer_id=person.consumer_id)

        await matching_service.persons.add(person)
        await matching_service.passports.add(passport)

        status = await matching_service.match_status_by_person_passport(
            person.name,
            person.surname,
            person.patronymic,
            person.birthdate,
            passport.number,
            passport.issued_at,
        )
        assert status is MatchingStatus.FULL_HIT

    async def test__match_status_by_person_passport__person_and_passport_hit(
        self,
        matching_service: MatchingService,
    ) -> None:
        person = PersonFactory.build()
        passport = PassportFactory.build(consumer_id=person.consumer_id)

        await matching_service.persons.add(person)
        await matching_service.passports.add(passport)

        status = await matching_service.match_status_by_person_passport(
            person.name,
            person.surname,
            person.patronymic,
            person.birthdate,
            passport.number,
            date(1970, 1, 1),
        )
        assert status is MatchingStatus.PERSON_AND_PASSPORT_HIT

    async def test__match_status_by_person_passport__person_hit(
        self,
        matching_service: MatchingService,
    ) -> None:
        person = PersonFactory.build()
        passport = PassportFactory.build()

        await matching_service.persons.add(person)

        status = await matching_service.match_status_by_person_passport(
            person.name,
            person.surname,
            person.patronymic,
            person.birthdate,
            passport.number,
            passport.issued_at,
        )
        assert status is MatchingStatus.PERSON_HIT

    async def test__match_status_by_person_passport__no_hit(
        self,
        matching_service: MatchingService,
    ) -> None:
        person = PersonFactory.build()
        passport = PassportFactory.build()

        status = await matching_service.match_status_by_person_passport(
            person.name,
            person.surname,
            person.patronymic,
            person.birthdate,
            passport.number,
            passport.issued_at,
        )
        assert status is MatchingStatus.NO_HIT
