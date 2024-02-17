"""Auth module for pod point, handled access token lifecycle."""

import logging
from datetime import datetime, timedelta

import aiohttp

from ..errors import APIError, AuthError, SessionError
from .session import Session
from ..endpoints import GOOGLE_BASE_URL, PASSWORD_VERIFY
from .functions import HEADERS
from .api_wrapper import APIWrapper

_LOGGER: logging.Logger = logging.getLogger(__package__)

class Auth():
    """Manages authentication lifecycle for a user"""
    def __init__(
        self,
        email: str,
        password: str,
        session: aiohttp.ClientSession,
        http_debug: bool = None
    ):
        self.email: str = email
        self.password: str = password
        self.access_token: str = None
        self.refresh_token: str = None
        self.access_token_expiry: datetime = None
        self.session: Session = None
        self._session: aiohttp.ClientSession = session
        self._api_wrapper: APIWrapper = APIWrapper(session=self._session)
        self._http_debug: bool = http_debug if http_debug is not None else False

    @property
    def user_id(self):
        """Return the user_id for a given session"""
        if self.session:
            return self.session.user_id
        return None

    def check_access_token(self) -> bool:
        """Does the current access token need refreshing?"""
        access_token_not_expired: bool = self.access_token_expired() is False

        return bool(self.access_token_set() and access_token_not_expired)

    def access_token_set(self) -> bool:
        return (
                self.access_token is not None and self.access_token_expiry is not None
        )

    def access_token_expired(self) -> bool:
        """Is the current access token expired"""
        return self.access_token_set() and datetime.now() > self.access_token_expiry

    async def async_update_access_token(self) -> bool:
        """Update access token, if needed."""
        if self.check_access_token():
            return True

        try:
            _LOGGER.debug('Updating access token')
            access_token_updated: bool = await self.__update_access_token()

            _LOGGER.debug(
                "Updated access token. New expiration: %s",
                self.access_token_expiry
            )

            self.session = Session(
                email=self.email,
                password=self.password,
                access_token=self.access_token,
                session=self._session,
                http_debug=self._http_debug
            )
            session_created = await self.session.create()

            if session_created is False:
                _LOGGER.error("Error creating session")

            return access_token_updated and session_created
        except AuthError as exception:
            _LOGGER.error("Error updating access token. %s", exception)
            raise exception
        except SessionError as exception:
            _LOGGER.error("Error creating session. %s", exception)
            raise exception

    async def __update_access_token(self, refresh: bool = False) -> bool:
        return_value = False

        try:
            wrapper = APIWrapper(session=self._session)
            response = await wrapper.post(
                url=f"{GOOGLE_BASE_URL}{PASSWORD_VERIFY}",
                body={"email": self.email, "returnSecureToken": True, "password": self.password},
                headers=HEADERS,
                exception_class=AuthError)

            if response.status != 200:
                await self.__handle_response_error(response, AuthError)

            json = await response.json()
            self.access_token = json["idToken"]
            self.refresh_token = json["refreshToken"]
            self.access_token_expiry = datetime.now() + timedelta(
                seconds=int(json["expiresIn"]) - 10
            )
            return_value = True

            if self._http_debug:
                _LOGGER.debug(json)
        except AuthError as exception:
            raise exception
        except KeyError as exception:
            raise AuthError(
                response.status,
                f"Error processing access token response. {exception} not found in json."
            ) from exception
        except (TypeError, ValueError) as exception:
            raise AuthError(
                response.status,
                f"Error processing access token response. \
When calculating expiry date, got: {exception}."
            ) from exception
        except APIError as exception:
            raise exception

        return return_value

    async def __handle_response_error(self, response, error_class):
        status = response.status
        response = await response.text()

        raise error_class(status, response)
