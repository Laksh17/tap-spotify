"""Stream type classes for tap-spotify-bearer."""

from __future__ import annotations

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_spotify_bearer.client import SpotifyStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class ArtistsStream(SpotifyStream):
    """Define custom stream."""
    
    name = "Trending Songs in India"
    path = "/37i9dQZF1DXbVhgADFy3im"
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    schema = th.PropertiesList(
        th.Property("track", th.ObjectType(
            th.Property("album_name",th.StringType),
            th.Property("song_link",th.StringType),
            th.Property("id",th.StringType),
            th.Property("song_name",th.StringType),
            th.Property("popularity",th.IntegerType)
        ))
        ).to_dict()
    
    # name = "Top 50 - Global"
    # path = "/37i9dQZEVXbMDoHDwVN2tF"
    # replication_key = None
    # # Optionally, you may also use `schema_filepath` in place of `schema`:
    # # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    # schema = th.PropertiesList(
    #     th.Property("track", th.ObjectType(
    #         th.Property("album_name",th.StringType),
    #         th.Property("song_link",th.StringType),
    #         th.Property("id",th.StringType),
    #         th.Property("song_name",th.StringType),
    #         th.Property("popularity",th.IntegerType)
    #     ))
    #     ).to_dict()
