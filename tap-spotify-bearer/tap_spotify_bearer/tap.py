"""Spotify tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_spotify_bearer import streams


class TapSpotify(Tap):
    """Spotify tap class."""

    name = "tap-spotify-bearer"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        # th.Property(
        #     "auth_token",
        #     th.StringType,
        #     required=True,
        #     secret=True,  # Flag config as protected.
        #     description="The token to authenticate against the API service",
        # ),
        # th.Property(
        #     "project_ids",
        #     th.ArrayType(th.StringType),
        #     required=True,
        #     description="Project IDs to replicate",
        # ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.spotify.com/v1/playlists",
            description="The url for the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.SpotifyStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.ArtistsStream(self),
        ]


if __name__ == "__main__":
    TapSpotify.cli()
