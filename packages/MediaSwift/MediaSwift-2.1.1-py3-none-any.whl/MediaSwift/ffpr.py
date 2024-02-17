# ffpr.py
# ---------

import os
import json
import subprocess
from functools import lru_cache
from typing import Optional


class FFProbeResult:
    """
    >>> REPRESENTS THE RESULT OF FFPROBE ANALYSIS ON A MULTIMEDIA FILE.

    ... ATTRIBUTES
    ----------
    >>> INFO : DICT
        >>> INFORMATION OBTAINED FROM FFPROBE.

    ... METHODS
    -------
    >>> DURATION() -> OPTIONAL[FLOAT]:
        >>> GET THE DURATION OF THE MULTIMEDIA FILE.
    >>> BIT_RATE() -> OPTIONAL[FLOAT]:
        >>> GET THE BIT RATE OF THE MULTIMEDIA FILE.
    >>> NB_STREAMS() -> OPTIONAL[INT]:
        >>> GET THE NUMBER OF STREAMS IN THE MULTIMEDIA FILE.
    STREAMS():
        >>> GET THE DETAILS OF INDIVIDUAL STREAMS IN THE MULTIMEDIA FILE.

        >>> EXAMPLE:


        ```python
        =================================================================
        >>> from MediaSWiftPy import ffpr

        >>> ffprobe = ffpr()
        >>> info = ffprobe.probe(r"PATH_TO_MEDIA_FILE")
        >>> ffprobe.pretty(info)
        =================================================================
        ```

    >>> USE "pretty()" MORE BEAUTIFY CONTENT SHOW.
    >>> RETURN NONE
    """

    def __init__(self, info):
        self.info = info

    @property
    def duration(self) -> Optional[float]:
        try:
            return float(self.info["format"]["duration"])
        except (KeyError, ValueError):
            return None

    @property
    def bit_rate(self) -> Optional[float]:
        try:
            return int(self.info["format"]["bit_rate"]) / 1000
        except (KeyError, ValueError):
            return None

    @property
    def nb_streams(self) -> Optional[int]:
        return self.info["format"].get("nb_streams")

    @property
    def streams(self):
        return self.info["streams"]


class ffpr:
    """
    >>> A CLASS FOR INTERFACING WITH FFPR TO ANALYZE MULTIMEDIA FILES.

    ... METHODS
    -------
    PROBE[INPUT_FILE] -> OPTIONAL:
    ---------------------------------------------
        >>> ANALYZE MULTIMEDIA FILE USING FFPR AND RETURN THE RESULT.
    PRETTY(INFO):
    ----------------------------
        >>> PRINT READABLE SUMMARY OF THE FFPR ANALYSIS RESULT, MAKE BEAUTIFY CONTENT.

        >>> EXAMPLE:


        ```python
        =================================================================
        >>> from MediaSWiftPy import ffpr

        >>> Details = ffpr()
        >>> info = Details.probe(r"PATH_TO_MEDIA_FILE")
        >>> Details.pretty(info)
        =================================================================
        ```

    >>> USE "pretty()" MORE BEAUTIFY CONTENT SHOW.
    >>> RETURN: NONE
    """

    def __init__(self):
        self._ffprobe_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "bin", "ffprobe.exe"
        )

    @property
    def ffprobe_path(self):
        return self._ffprobe_path

    @lru_cache(maxsize=None)
    def probe(self, input_file) -> Optional[FFProbeResult]:
        """
        >>> ANALYZE MULTIMEDIA FILE USING FFPR AND RETURN THE RESULT.

        ... PARAMETERS
        ----------
        INPUT_FILE : STR
        -----------------
            >>> PATH TO THE MULTIMEDIA FILE.

        OPTIONAL:
        ----------
            >>> RESULT OF THE FFPR ANALYSIS.
            >>> RETURN: NONE
        """
        try:
            command = [
                self.ffprobe_path,
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_format",
                "-show_streams",
                input_file,
            ]
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            return FFProbeResult(json.loads(result.stdout.decode("utf-8")))
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def pretty(self, info: FFProbeResult):
        """
        >>> PRINT READABLE SUMMARY OF THE FFPR ANALYSIS RESULT, MAKE BEAUTIFY CONTENT.

        ... PARAMETERS
        ----------
        INFO :
        -------
            >>> RESULT OF THE FFPR ANALYSIS.
            >>> RETURN: NONE
        """
        if not info:
            print("No information available.")
            return

        print("Video Info:\n")
        print(f"General:")
        print(f"  File: {info.info['format']['filename']}")

        try:
            duration_seconds = info.duration
            minutes, seconds = divmod(duration_seconds, 60)
            print(f"  Duration: {int(minutes)}:{int(seconds)} min")
        except (KeyError, ValueError):
            print("  Duration information not available.")

        try:
            bit_rate_kbps = info.bit_rate
            print(f"  Bit rate: {bit_rate_kbps} kbit/s")
        except (KeyError, ValueError):
            print("  Bit rate information not available.")

        print(f"  Number of streams: {info.nb_streams}")

        for i, stream in enumerate(info.streams):
            print(f"\nStream {i + 1} ({stream['codec_type']} stream):")
            print(f"  Codec: {stream.get('codec_name', 'N/A')}")
            print(f"  Profile: {stream.get('profile', 'N/A')}")
            print(f"  Level: {stream.get('level', 'N/A')}")
            try:
                bit_rate_kbps = (
                    int(stream.get("bit_rate", "N/A")) / 1000
                )  # Corrected here
                print(f"  Bit rate: {bit_rate_kbps} kbit/s")
            except (KeyError, ValueError):
                print("  Bit rate information not available.")
            print(f"  Type: {stream.get('codec_type', 'N/A')}")

            if "tags" in stream:
                print(f"  Language: {stream['tags'].get('language', 'N/A')}")

            if stream["codec_type"] == "video":
                print(
                    f"  Resolution: {stream.get('width', 'N/A')}x{stream.get('height', 'N/A')}"
                )
                print(
                    f"  Display aspect ratio: {stream.get('display_aspect_ratio', 'N/A')}"
                )
                print(f"  Frame rate: {stream.get('r_frame_rate', 'N/A')}")
            elif stream["codec_type"] == "audio":
                print(f"  Channels: {stream.get('channels', 'N/A')}")
                print(f"  Sample rate: {stream.get('sample_rate', 'N/A')}")
            elif stream["codec_type"] == "subtitle":
                print(f"  Language: {stream.get('tags', {}).get('language', 'N/A')}")
