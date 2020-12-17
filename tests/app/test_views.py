from datetime import date
from http import HTTPStatus

import aiohttp
from aiohttp.test_utils import TestClient

from loyal.domain import (
    MatchingStatus,
    PassportRepositoryInterface,
    PersonRepositoryInterface,
)
from loyal.test_utils import PassportFactory, PersonFactory


async def assert_ok(
    response: aiohttp.ClientResponse,
    *,
    data: dict = None,
    message: str = None,
) -> None:
    http_status = HTTPStatus.OK
    assert response.status == http_status

    assert await response.json() == {
        "data": data or {},
        "message": message or "OK",
    }


async def assert_bad_request(
    response: aiohttp.ClientResponse,
    *,
    message: str,
) -> None:
    http_status = HTTPStatus.BAD_REQUEST
    assert response.status == http_status

    assert await response.json() == {
        "message": message,
    }


async def assert_validation_error(
    response: aiohttp.ClientResponse,
    *,
    errors: dict,
) -> None:
    http_status = HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.status == http_status

    assert await response.json() == {
        "errors": errors,
        "message": "Input payload validation failed",
    }


async def assert_graphql_response(
    response: aiohttp.ClientResponse,
    *,
    data: dict = None,
    errors: list = None,
) -> None:
    http_status = HTTPStatus.OK
    assert response.status == http_status

    assert await response.json() == {
        "data": data,
        "errors": errors,
    }


class TestPingView:
    url = "/ping"

    async def test_that_service_is_alive(self, client: TestClient) -> None:
        response = await client.get(self.url)

        await assert_ok(response, message="pong")


class TestHealthView:
    url = "/health"

    async def test_that_service_is_alive(self, client: TestClient) -> None:
        response = await client.get(self.url)

        await assert_ok(response)


class TestGraphQLSchemas:
    url = "/graphql"

    async def test_payload_parsing_error(
        self,
        client: TestClient,
    ) -> None:
        data = "{ not_a_json }"
        response = await client.post(self.url, data=data)

        message = "Couldn't parse request body"
        await assert_bad_request(response, message=message)

    async def test_invalid_json_schema(
        self,
        client: TestClient,
    ) -> None:
        json = {
            "not_query": "query",
        }
        response = await client.post(self.url, json=json)

        errors = {
            "query": ["Missing data for required field."],
        }
        await assert_validation_error(response, errors=errors)

    async def test_validation_error(
        self,
        client: TestClient,
    ) -> None:
        query = """
            {
                passportByPerson(
                    name: "Steve"
                    surname: "Paul",
                    patronymic: "Jobs",
                    birthdate: "19701010",
                ) {
                    number
                }
            }
        """

        json = {
            "query": query,
        }
        response = await client.post(self.url, json=json)

        data = {
            "passportByPerson": None,
        }
        errors = [
            (
                "Input payload validation failed: "
                "birthdate (not a valid date), "
                "name (doesn't match expected pattern), "
                "patronymic (doesn't match expected pattern), "
                "surname (doesn't match expected pattern)"
            ),
        ]
        await assert_graphql_response(response, data=data, errors=errors)


class TestGraphQLHealthView:
    url = "/graphql"

    async def test_successful_health_query(self, client: TestClient) -> None:
        json = {
            "query": "{ health }",
        }
        response = await client.post(self.url, json=json)

        data = {
            "health": True,
        }
        await assert_graphql_response(response, data=data)

    async def test_failed_health_query(self, client: TestClient) -> None:
        json = {
            "query": "{ health { status } }",
        }
        response = await client.post(self.url, json=json)

        errors = [
            'Field "health" of type "Boolean" must not have a sub selection.',
        ]
        await assert_graphql_response(response, errors=errors)


class TestGraphQLPassportByPersonView:
    url = "/graphql"

    async def test_successful_passport_query_hit(
        self,
        client: TestClient,
        asyncpg_person_repository: PersonRepositoryInterface,
        asyncpg_passport_repository: PassportRepositoryInterface,
    ) -> None:
        person = PersonFactory.build(
            name="АВДЕИМЛ",
            surname="ЕЖИКОВ",
            patronymic="АКСЕНОВИЧЦОИ",
            birthdate=date(1970, 1, 1),
        )
        passport = PassportFactory.build(
            consumer_id=person.consumer_id,
            number="4545000888",
        )

        await asyncpg_person_repository.add(person)
        await asyncpg_passport_repository.add(passport)

        query = """
            {
                passportByPerson(
                    name: "  Авдей Мл "
                    surname: " Ёжиков",
                    patronymic: "Аксёнович-Цой",
                    birthdate: "1970-01-01",
                ) {
                    consumerId
                    number
                    updatedAt
                }
            }
        """

        json = {
            "query": query,
        }
        response = await client.post(self.url, json=json)

        data = {
            "passportByPerson": {
                "consumerId": passport.consumer_id,
                "number": passport.number,
                "updatedAt": passport.updated_at.strftime("%Y-%m-%d"),
            },
        }
        await assert_graphql_response(response, data=data)

    async def test_successful_passport_query_no_hit(
        self,
        client: TestClient,
        asyncpg_person_repository: PersonRepositoryInterface,
    ) -> None:
        person = PersonFactory.build(
            name="АВДЕИМЛ",
            surname="ЕЖИКОВ",
            patronymic="АКСЕНОВИЧЦОИ",
            birthdate=date(1970, 1, 1),
        )
        await asyncpg_person_repository.add(person)

        query = """
            {
                passportByPerson(
                    name: "Авдей Мл"
                    surname: "Ёжиков",
                    patronymic: "Аксёнович-Цой",
                    birthdate: "1970-01-01",
                ) {
                    consumerId
                    number
                    updatedAt
                }
            }
        """

        json = {
            "query": query,
        }
        response = await client.post(self.url, json=json)

        data = {
            "passportByPerson": None,
        }
        await assert_graphql_response(response, data=data)

    async def test_successful_passport_query_no_hit_2(
        self,
        client: TestClient,
    ) -> None:
        query = """
            {
                passportByPerson(
                    name: "Авдей Мл"
                    surname: "Ёжиков",
                    patronymic: "Аксёнович-Цой",
                    birthdate: "1970-01-01",
                ) {
                    number
                }
            }
        """

        json = {
            "query": query,
        }
        response = await client.post(self.url, json=json)

        data = {
            "passportByPerson": None,
        }
        await assert_graphql_response(response, data=data)

    async def test_failed_syntax_passport_query(
        self,
        client: TestClient,
    ) -> None:
        query = """
            {
                passportByPerson(
                    patronymic: "Иванович",
                    birthdate: "1970-01-01",
                ) {
                    number
                }
            }
        """

        json = {
            "query": query,
        }
        response = await client.post(self.url, json=json)

        errors = [
            (
                'Field "passportByPerson" argument "name" of '
                'type "String!" is required but not provided.'
            ),
            (
                'Field "passportByPerson" argument "surname" of '
                'type "String!" is required but not provided.'
            ),
        ]
        await assert_graphql_response(response, errors=errors)


class TestGraphQLPersonStatusView:
    url = "/graphql"

    async def test_no_hit_status(self, client: TestClient) -> None:
        query = """
            {
                checkPersonPassport(
                    name: "Авдей Мл",
                    surname: "Ёжиков",
                    patronymic: "Аксёнович-Цой",
                    birthdate: "1970-01-01",
                    passportNumber: "8989765345",
                    passportIssuedAt: "2015-12-02",
                )
            }
        """

        json = {
            "query": query,
        }
        response = await client.post(self.url, json=json)

        data = {
            "checkPersonPassport": MatchingStatus.NO_HIT,
        }
        await assert_graphql_response(response, data=data)

    async def test_person_hit_status(
        self,
        client: TestClient,
        asyncpg_person_repository: PersonRepositoryInterface,
        asyncpg_passport_repository: PassportRepositoryInterface,
    ) -> None:
        person = PersonFactory.build(
            name="АВДЕИМЛ",
            surname="ЕЖИКОВ",
            patronymic="АКСЕНОВИЧЦОИ",
            birthdate=date(1970, 1, 1),
        )
        passport = PassportFactory.build(
            consumer_id=person.consumer_id,
        )

        await asyncpg_person_repository.add(person)
        await asyncpg_passport_repository.add(passport)

        query = """
            {
                checkPersonPassport(
                    name: "Авдей Мл",
                    surname: "Ёжиков",
                    patronymic: "Аксёнович-Цой",
                    birthdate: "1970-01-01",
                    passportNumber: "8989765345",
                    passportIssuedAt: "2015-12-02",
                )
            }
        """

        json = {
            "query": query,
        }
        response = await client.post(self.url, json=json)

        data = {
            "checkPersonPassport": MatchingStatus.PERSON_HIT,
        }
        await assert_graphql_response(response, data=data)

    async def test_person_and_passport_hit_status(
        self,
        client: TestClient,
        asyncpg_person_repository: PersonRepositoryInterface,
        asyncpg_passport_repository: PassportRepositoryInterface,
    ) -> None:
        person = PersonFactory.build(
            name="АВДЕИМЛ",
            surname="ЕЖИКОВ",
            patronymic="АКСЕНОВИЧЦОИ",
            birthdate=date(1970, 1, 1),
        )
        passports = (
            PassportFactory.build(
                consumer_id=person.consumer_id,
                number="4545000888",
                issued_at=date(2012, 7, 15),
            ),
            PassportFactory.build(
                consumer_id=person.consumer_id,
                number="8989765345",
                issued_at=date(2015, 12, 2),
            ),
        )

        for passport in passports:
            await asyncpg_passport_repository.add(passport)
        await asyncpg_person_repository.add(person)

        query = """
            {
                checkPersonPassport(
                    name: "Авдей Мл",
                    surname: "Ёжиков",
                    patronymic: "Аксёнович-Цой",
                    birthdate: "1970-01-01",
                    passportNumber: "8989765345",
                    passportIssuedAt: "1970-12-02",
                )
            }
        """

        json = {
            "query": query,
        }
        response = await client.post(self.url, json=json)

        data = {
            "checkPersonPassport": MatchingStatus.PERSON_AND_PASSPORT_HIT,
        }
        await assert_graphql_response(response, data=data)

    async def test_full_hit_status(
        self,
        client: TestClient,
        asyncpg_person_repository: PersonRepositoryInterface,
        asyncpg_passport_repository: PassportRepositoryInterface,
    ) -> None:
        person = PersonFactory.build(
            name="АВДЕИМЛ",
            surname="ЕЖИКОВ",
            patronymic="АКСЕНОВИЧЦОИ",
            birthdate=date(1970, 1, 1),
        )
        passports = (
            PassportFactory.build(
                consumer_id=person.consumer_id,
                number="4545000888",
                issued_at=date(2012, 7, 15),
            ),
            PassportFactory.build(
                consumer_id=person.consumer_id,
                number="8989765345",
                issued_at=date(2015, 12, 2),
            ),
        )

        for passport in passports:
            await asyncpg_passport_repository.add(passport)
        await asyncpg_person_repository.add(person)

        query = """
            {
                checkPersonPassport(
                    name: "Авдей Мл",
                    surname: "Ёжиков",
                    patronymic: "Аксёнович-Цой",
                    passportNumber: "8989765345",
                    passportIssuedAt: "2015-12-02",
                )
            }
        """

        json = {
            "query": query,
        }
        response = await client.post(self.url, json=json)

        data = {
            "checkPersonPassport": MatchingStatus.FULL_HIT,
        }
        await assert_graphql_response(response, data=data)
