import logging

from jsonschema import Draft202012Validator
from helpers.client import DynamicAPIClient
from schemas import (
    account_schema,
    calendar_schema,
    listing_ids_schema,
    listings_schema,
    reservation_list_schema,
    reservation_schema,
)
from helpers import exceptions as DynamicExceptions

from dateutil.relativedelta import relativedelta
import datetime

BASE_URL=""
API_KEY=""


def _log_report_for_20x(context: str, schema: dict, payload: dict):
    validator = Draft202012Validator(
        schema, format_checker=Draft202012Validator.FORMAT_CHECKER
    )

    errors = sorted(validator.iter_errors(payload), key=str)

    if not errors:
        print(f"[OK]{context}")
        return

    print(f"[ERROR !!] {context}")

    for error in errors:
        print(f"    - {error.json_path} - {error.message}")


def _validate_account_endpoint_returns_200(client: DynamicAPIClient):
    account_payload = client.get_account_information()

    _log_report_for_20x(
        context="GET /account status:200",
        schema=account_schema,
        payload=account_payload,
    )


def _validate_account_endpoint_returns_401(client: DynamicAPIClient):
    invalid_client = DynamicAPIClient(
        api_key="invalid-api-key", base_url=client.base_url
    )

    try:
        invalid_client.get_account_information()
    except DynamicExceptions.InvalidCredentials:
        print("[OK]GET /account status:401")
    except Exception as e:
        print(e)
        print("[ERROR !!] GET /account status:401")


def _validate_listing_ids_endpoint_returns_200(client: DynamicAPIClient):
    listing_ids_payload = client.get_listing_ids()

    _log_report_for_20x(
        context="GET /listings status:200",
        schema=listing_ids_schema,
        payload=listing_ids_payload,
    )


def _validate_listing_endpoint_returns_200(client: DynamicAPIClient):
    listing_ids_payload = client.get_listing_ids()
    listing_id = listing_ids_payload[0]
    listing_payload = client.get_listing_by_id(listing_id)
    _log_report_for_20x(
        context=f"GET /listings/{listing_id} status:200",
        schema=listings_schema,
        payload=listing_payload,
    )


def _validate_listing_endpoint_returns_404(client: DynamicAPIClient):
    try:
        client.get_listing_by_id("invalid-id")
    except DynamicExceptions.PropertyNotFound:
        print("[OK]GET /listings/invalid-id status:404")
    except Exception:
        print("[ERROR !!] GET /listings/invalid-id status:404")


def _validate_listing_calendar_endpoint_returns_200(client: DynamicAPIClient):
    listing_ids_payload = client.get_listing_ids()
    listing_id = listing_ids_payload[0]
    try:
        calendar_payload = client.get_calendar_by_listing_id(listing_id)
    except DynamicExceptions.StatusCodeException as e:
        print(
            f"[ERROR !!] GET /listings/{listing_id}/calendar returned a {e.status_code} status:200"
        )
        return
    _log_report_for_20x(
        context=f"GET /listings/{listing_id}/calendar status:200",
        schema=calendar_schema,
        payload=calendar_payload,
    )


def _validate_listing_calendar_endpoint_returns_404(client: DynamicAPIClient):
    try:
        client.get_calendar_by_listing_id("invalid-id")
    except DynamicExceptions.PropertyNotFound:
        print("[OK]GET /listings/invalid-id/calendar status:404")
    except Exception:
        print("[ERROR !!] GET /listings/invalid-id/calendar status:404")


def _validate_post_prices_endpoint_returns_201(client: DynamicAPIClient):
    listing_ids_payload = client.get_listing_ids()
    listing_id = listing_ids_payload[0]
    date = datetime.date.today()
    dummy_rates = [
        {
            "date": (date + relativedelta(days=1)).isoformat(),
            "dailyPrice": 296,
            "minNights": 3,
            "checkinDays": ["saturday"],
            "checkoutDays": ["saturday"],
        },
        {
            "date": (date + relativedelta(days=2)).isoformat(),
            "dailyPrice": 296,
            "minNights": 3,
            "checkinDays": ["saturday", "friday"],
            "checkoutDays": ["saturday"],
        },
        {
            "date": (date + relativedelta(days=3)).isoformat(),
            "dailyPrice": 433,
            "minNights": 2,
            "checkinDays": ["saturday"],
            "checkoutDays": ["saturday"],
            "extraGuests": 2,
            "extraGuestFee": 156,
        },
    ]
    calendar_payload = client.post_rates(listing_id, dummy_rates)
    _log_report_for_20x(
        context=f"POST /listing/{listing_id}/calendar status:201",
        schema=calendar_schema,
        payload=calendar_payload,
    )


def _validate_post_prices_endpoint_returns_404(client: DynamicAPIClient):
    dummy_rates = []

    try:
        client.post_rates("invalid-id", dummy_rates)
    except DynamicExceptions.PropertyNotFound:
        print("[OK]POST /listings/invalid-id/calendar status:404")
    except Exception:
        print("[ERROR !!] POST /listings/invalid-id/calendar status:404")


def _validate_listing_reservations_endpoint_returns_200(client: DynamicAPIClient):
    listing_ids_payload = client.get_listing_ids()
    try:
        listing_id = listing_ids_payload[0]
        reservation_list_payload = client.get_reservations_by_listing_id(listing_id)

        _log_report_for_20x(
            context=f"GET /listings/{listing_id}/reservations status:200",
            schema=reservation_list_schema,
            payload=reservation_list_payload,
        )
    except IndexError:
        print(f"[ERROR !!] GET /listings/{listing_id}/reservations does not return a list.")

    except DynamicExceptions.InvalidCredentials:
        print(
            f"[ERROR !!] GET /listings/{listing_id}/reservations - Our credentials are invalid"
        )


def _validate_listing_reservations_endpoint_returns_404(client: DynamicAPIClient):
    try:
        client.get_reservations_by_listing_id("invalid-id")
    except DynamicExceptions.PropertyNotFound:
        print("[OK]GET /listings/invalid-id/reservations status:404")
    except Exception:
        print("[ERROR !!] GET /listings/invalid-id/reservations status:404")


def _validate_reservation_endpoint_returns_200(client: DynamicAPIClient):
    listing_ids_payload = client.get_listing_ids()
    try:
        listing_id = listing_ids_payload[0]
        reservations = client.get_reservations_by_listing_id(listing_id)
        if len(reservations) == 0:
            print(
                "[ERROR !!] Couldn't Validate GET /reservations/{id} because listings/{listing_id}/reservations returned no reservations."
            )
            return

        reservation_id = reservations[0]["id"]
        reservation_payload = client.get_reservation(reservation_id)
        _log_report_for_20x(
            context=f"GET /reservations/{reservation_id} status:200",
            schema=reservation_schema,
            payload=reservation_payload,
        )
    except IndexError:
        print(f"[ERROR !!] GET /listings/{listing_id}/reservations does not return a list.")
    except DynamicExceptions.InvalidCredentials:
        print(f"[ERROR !!] GET /listings/{listing_id}/reservations Returns a 401.")


def _validate_reservation_endpoint_returns_404(client: DynamicAPIClient):
    try:
        client.get_reservation("invalid-id")
    except DynamicExceptions.ReservationNotFound:
        print("[OK]GET /reservations/invalid_id be status:404")
    except Exception:
        print("[ERROR !!] Couldn't Validate GET /reservations/invalid_id be status:404")


def _pre_work(disable_logging: bool = True):
    utilities_logger = logging.getLogger("lib.utilities")
    if disable_logging:
        utilities_logger.propagate = False
    else:
        utilities_logger.propagate = True


def run(base_url: str, api_key: str, disable_logging: bool = True):
    _pre_work(disable_logging=disable_logging)

    client = DynamicAPIClient(api_key, base_url)

    _validate_account_endpoint_returns_200(client)
    _validate_account_endpoint_returns_401(client)
    _validate_listing_ids_endpoint_returns_200(client)
    _validate_listing_endpoint_returns_200(client)
    _validate_listing_endpoint_returns_404(client)
    _validate_listing_calendar_endpoint_returns_200(client)
    _validate_listing_calendar_endpoint_returns_404(client)
    _validate_listing_reservations_endpoint_returns_200(client)
    _validate_listing_reservations_endpoint_returns_404(client)
    _validate_reservation_endpoint_returns_200(client)
    _validate_reservation_endpoint_returns_404(client)
    _validate_post_prices_endpoint_returns_201(client)
    _validate_post_prices_endpoint_returns_404(client)

if __name__ == "__main__":
    run(BASE_URL, API_KEY)

