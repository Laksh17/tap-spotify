# tap-spotify-bearer

`tap-spotify-bearer` is a Singer tap for Spotify.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.


## Configuration

Make sure you have `poetry` installed in addition to the other packages.

Steps to get the tap working:

1. Clone this repository 

2. Create a developer account using this link: `https://developer.spotify.com/dashboard`

3. To create an app on spotify, follow the steps as shown in the "Create an app" section on the official documentation for the spotify API whose link is: `https://developer.spotify.com/documentation/web-api/tutorials/getting-started`. 
NOTE: Use `https://localhost:8080` as the redirect-URI

4. Create a `.env` file within the main folder and enter your Client ID and Seceret as follows:
```bash
SPOTIFY_CLIENT_ID = "YOUR APP'S ID"
SPOTIFY_CLIENT_SECRET = "YOUR APP'S SECRET"
```

5. Run the following command to configure your tap:
```bash
pip install .\tap-spotify-bearer\ 
```

6. Run the following command to test the success of your tap:
```bash
poetry run tap-spotify-bearer --test --config ENV
```

7. Run the following command to get the output from the playlist whose ID is mentioned is mentioned in the `streams.py` file. 
NOTE: You can obtain the ID of your desired playlist by copying the last the string after the final `/` in the URL 

8. Refer the steps followed in the `target-gsheets` github repostiory whose link is `https://github.com/singer-io/target-gsheet` to connect this tap to Google Sheets.

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
