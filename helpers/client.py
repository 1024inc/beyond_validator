from typing import Dict, List
from requests import request
from .exceptions import (
    BadRequest,
    InternalServerError,
    InvalidCredentials,
    PropertyNotFound,
    PostingRatesError,
    ReservationNotFound,
    StatusCodeException
)


class DynamicAPIClient():
    ROUTES = {
        "PATH_ACCOUNT": "/account",
        "PATH_LISTINGS": "/listings",
        "PATH_LISTING": "/listings/{listing_id}",
        "PATH_CALENDAR": "/listings/{listing_id}/calendar",
        "PATH_LISTING_RESERVATION": "/listings/{listing_id}/reservations",
        "PATH_RESERVATION": "/reservations/{reservation_id}",
    }
    ALLOWED_STATUS_CODES = (200, 400, 500, 201, 404, 401)

    def __init__(self, api_key, base_url) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.allowed_status_codes = self.ALLOWED_STATUS_CODES

    def _request(self, *args, headers=None, **kwargs):
        new_headers = {
            "x-api-key": self.api_key,
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
        }
        if headers:
            headers.update(new_headers)
        else:
            headers = new_headers
        url = self.base_url + kwargs.pop("path")
        response = request(headers=headers, url=url, *args, timeout=300, **kwargs)
        if (
            response.status_code not in self.allowed_status_codes
        ):
            raise StatusCodeException(
                message=f"{self._integration_name}: Response status code was "
                f"{response.status_code}, `allowed_status_codes` are:"
                f" {self.allowed_status_codes}",
                status_code=response.status_code,
                response=response,
            )
        if response.status_code == 500:
            raise InternalServerError(f"Request failed with error: {response.text}")

        if response.status_code == 400:
            raise BadRequest(f"Request failed with error: {response.text}")

        if response.status_code == 401:
            raise InvalidCredentials(
                f"Authentication failed with error: {response.text}"
            )

        if response.status_code == 403:
            raise InvalidCredentials(f"Access forbidden with error: {response.text}")

        return response

    def _get(self, **kwargs):
        return self._request("GET", **kwargs)

    def _post(self, data, **kwargs):
        return self._request("POST", data=data, **kwargs)

    def get_account_information(self):
        """Fetch account information."""
        response = self._get(path=self.ROUTES["PATH_ACCOUNT"])
        data = response.json()
        return data

    def get_listing_ids(self):
        """Fetch all Listings."""
        response = self._get(path=self.ROUTES["PATH_LISTINGS"])
        data = response.json()
        return data

    def get_listing_by_id(self, listing_id):
        """Fetch a listing by Listing ID"""
        path = self.ROUTES["PATH_LISTING"].format(listing_id=listing_id)
        response = self._get(path=path)
        if response.status_code == 404:
            raise PropertyNotFound(
                f"Failed to get listing with id: {listing_id} with error response: {response.text}"
            )
        data = response.json()
        return data

    def get_calendar_by_listing_id(self, listing_id):
        """Fetch calendar by Listing ID."""
        path = self.ROUTES["PATH_CALENDAR"].format(listing_id=listing_id)
        response = self._get(path=path)
        if response.status_code == 404:
            raise PropertyNotFound(
                f"Failed to get listing with id: {listing_id} with error response: {response.text}"
            )

        data = response.json()
        return data

    def post_rates(self, listing_id, rates: List[Dict]):
        """Post rates information by Listing ID."""
        path = self.ROUTES["PATH_CALENDAR"].format(listing_id=listing_id)
        response = self._post(path=path, data={}, json=rates)
        if response.status_code == 404:
            raise PropertyNotFound(
                f"Failed to get listing with id: {listing_id} with error response: {response.text}"
            )
        if response.status_code == 400:
            raise PostingRatesError(
                "Failed to post rates with the error: {response.text}"
            )
        return []

    def get_reservations_by_listing_id(self, listing_id, checkin_start_date=None):
        """Fetch reservations by Listing ID"""
        path = self.ROUTES["PATH_LISTING_RESERVATION"].format(listing_id=listing_id)
        params = dict()
        if checkin_start_date:
            params.update({"checkinStartDate": checkin_start_date.strftime("%Y-%m-%d")})
        response = self._get(path=path, params=params)

        if response.status_code == 404:
            raise PropertyNotFound(
                f"Failed to get listing with id: {listing_id} with error response: {response.text}"
            )
        data = response.json()
        return data

    def get_reservation(self, reservation_id):
        """Fetch a reservation by Reservation ID."""
        path = self.ROUTES["PATH_RESERVATION"].format(reservation_id=reservation_id)
        response = self._get(path=path)
        if response.status_code == 404:
            raise ReservationNotFound(
                f"Failed to get reservation with id: {reservation_id} with error response: {response.text}"
            )
        data = response.json()
        return data
