<h1>Synced Lyric on TouchBar</h1>

Show synced lyric in the touch-bar with BetterTouchTool and NetEase APIs. Based on the idea of [Kashi](https://community.folivora.ai/t/kashi-show-current-song-lyrics-on-touch-bar-spotify-itunes-youtube/6301).

## Features

-   **Synced lyrics** from NetEase Music APIs;
-   Support **Spotify** (Recommended) & **Music** (Only songs in your playlists);
-   Support for **English/Spanish/Chinese(Simplified/Traditional)/Japanese** and more;

## Instruction

**If you are not familiar with command line, python ecosystem or having problems understanding this tutorial, find a friend to help you. Issues/DMs are not actively monitored for this project.**

### 1. Installation

```shell
pip3 install -e .
```

### 2. Configuration in BetterTouchTool

Same as Kashi:

1.  Copy&paste the content in `lyric.json` in _Meun Bar > Touch Bar_;
2.  Change the python path `$PYTHONPATH` to your own python path in the script area;

```shell
$PYTHONPATH -m macos_lyric --app Music
```

or use Spotify(default)

```shell
$PYTHONPATH -m macos_lyric --app Spotify
```

**Be careful with typing double hyphens in BTT. It automatically change it to an em slash. Use copy & paste instead!**

## Acknowledgement

1. Inspired by [Kashi](https://community.folivora.ai/t/kashi-show-current-song-lyrics-on-touch-bar-spotify-itunes-youtube/6301) by [Jim Ho](https://github.com/jimu-gh).
2. Supported by wonderful projects like [qq-music-api](https://github.com/Rain120/qq-music-api) by [Rain120](https://github.com/Rain120) and [spotifylyrics](https://github.com/SimonIT/spotifylyrics) by [SimonIT](https://github.com/SimonIT).

## Disclaimer

This project is not affiliated with Apple, Spotify, QQ Music, NetEase Music, BetterTouchTool or any other third party. This project is not intended to violate any terms of service of the aforementioned parties. This project is for educational purposes only.
