"""REST client handling, including SpotifyStream base class."""

from __future__ import annotations
import requests
from pathlib import Path
from typing import Any, Callable, Iterable
import json
import requests
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream
from dotenv import load_dotenv
import os

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class SpotifyStream(RESTStream):
    """Spotify stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        # TODO: hardcode a value here, or retrieve it from self.config
        return self.config.get("api_url", "https://api.spotify.com/v1/playlists")

    records_jsonpath = "$.[*]"  # Or override `parse_response`.

    # Set this value or override `get_new_paginator`.
    next_page_token_jsonpath = "$.next_page"  # noqa: S105

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        load_dotenv()
        my_id = os.getenv("SPOTIFY_CLIENT_ID")
        my_secret_key = os.getenv("SPOTIFY_CLIENT_SECRET")
               
        data = {
            "grant_type": 'client_credentials',
            "client_id": {my_id},
            "client_secret": {my_secret_key}
        }
        
        response = requests.post("https://accounts.spotify.com/api/token",
                                 headers={"Content-Type": "application/x-www-form-urlencoded"},
                                 params=data)

        response.raise_for_status()
        jsonResponse = response.json()
           
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=jsonResponse["access_token"],
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")  # noqa: ERA001
        return headers

    # def get_new_paginator(self) -> BaseAPIPaginator:
    #     """Create a new pagination helper instance.

    #     If the source API can make use of the `next_page_token_jsonpath`
    #     attribute, or it contains a `X-Next-Page` header in the response
    #     then you can remove this method.

    #     If you need custom pagination that uses page numbers, "next" links, or
    #     other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

    #     Returns:
    #         A pagination helper instance.
    #     """
    #     pass

    # def get_url_params(
    #     self,
    #     context: dict | None,  # noqa: ARG002
    #     next_page_token: Any | None,
    # ) -> dict[str, Any]:
    #     """Return a dictionary of values to be used in URL parameterization.

    #     Args:
    #         context: The stream context.
    #         next_page_token: The next page index or value.

    #     Returns:
    #         A dictionary of URL query parameters.
    #     """
    #     pass
        # params: dict = {}
        # if next_page_token:
        #     params["page"] = next_page_token
        # if self.replication_key:
        #     params["sort"] = "asc"
        #     params["order_by"] = self.replication_key
        

    # def prepare_request_payload(
    #     self,
    #     context: dict | None,  # noqa: ARG002
    #     next_page_token: Any | None,  # noqa: ARG002
    # ) -> dict | None:
    #     """Prepare the data payload for the REST API request.

    #     By default, no payload will be sent (return None).

    #     Args:
    #         context: The stream context.
    #         next_page_token: The next page index or value.

    #     Returns:
    #         A dictionary with the JSON body for a POST requests.
    #     """
    #     # TODO: Delete this method if no payload is required. (Most REST APIs.)
    #     return None

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        
        for j in extract_jsonpath(self.records_jsonpath, input=response.json()):   
            for i in j["tracks"]["items"]:
                new_data = {"type": "RECORD", "stream": "Top 50 - Global", "record": {"id": "37i9dQZEVXbMDoHDwVN2tF", "name": "Top 50 - Global"}}
                new_data["track"] = {}
                new_data["track"]["album_name"] = i["track"]["album"]["name"]
                new_data["track"]["song_link"] = i["track"]["external_urls"]["spotify"]
                new_data["track"]["id"] = i["track"]["id"]
                new_data["track"]["song_name"] = i["track"]["name"]
                new_data["track"]["popularity"] = i["track"]["popularity"]

                yield new_data

    def post_process(
        self,
        row: dict,
        context: dict | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
            
       
        return row

