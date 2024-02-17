import os
import gc
import subprocess
from threading import Thread
import logging
from typing import Optional, List
from functools import lru_cache


class ffpe:
    """
    >>> FFPE - SIMPLE WRAPPER FOR FFMPEG.

    >>> THIS CLASS PROVIDES A CONVENIENT INTERFACE FOR USING FFMPEG TO CONVERT MULTIMEDIA FILES.

    ... ATTRIBUTES
    ----------
    FFMPEG_PATH : STR
    -----------------
        >>> PATH TO THE FFMPEG EXECUTABLE.

    LOGGER : LOGGING.LOGGER
    -----------------------
        >>> LOGGER INSTANCE FOR LOGGING MESSAGES.

    ... METHODS
    ----------
    >>> CONVERT(INPUT_FILES, OUTPUT_DIR, CV=NONE, CA=NONE, S=NONE, HWACCEL=NONE,
    >>>         AR=NONE, AC=NONE, BA=NONE, R=NONE, F=NONE, PRESET=NONE, BV=NONE)
    >>>     CONVERT MULTIMEDIA FILES USING FFMPEG.

    CONVERT()
    ----------
        >>> USE "convert()" TO CONVERT FILES

        >>> EXAMPLE


         ```python
        =================================================================
         # INSTANTIATE THE FFPE CLASS

         from <library name> import *
         ffpe_instance = ffpe()

         # Define input files and output directory
        ... input_files = ['input1.mp4', 'input2.mp4'] # input_files [MULTIPLE CONVERT]
        ... input_file = ['input1.mp4']               # input_file [SINGLE CONVERT]

         output_dir = 'output_folder'

         # PERFORM MULTIMEDIA FILE CONVERSION USING FFMPEG
         ffpe_instance.convert(
             input_files=input_files,
             output_dir=output_dir,
             cv='h264',        # VIDEO CODEC
             ca='aac',         # AUDIO CODEC
             s='1920x1080',    # VIDEO RESOLUTION
             hwaccel='cuda',   # HARDWARE ACCELERATION
             ar=44100,         # AUDIO SAMPLE RATE
             ac=2,             # AUDIO CHANNELS
             ba=192000,        # AUDIO BITRATE
             r=30,             # VIDEO FRAME RATE
             f='mp4',          # OUTPUT FORMAT
             preset='fast',    # PRESET FOR ENCODING
             bv=2000           # VIDEO BITRATE
         )
        - NOTE - ALWAYS SET INPUT FILE PATH IN SQUARE BRACKETS:
        - EXAMPLE-1 - input_files=[r"PATH_TO_INPUT_FILE"] # SINGLE CONVERTION
        - EXAMPLE-2 - input_files=[
        r"PATH_TO_INPUT_FILE_1",
        r"PATH_TO_INPUT_FILE_2"
    ] # MULTIPLE CONVERTION


    -

         ```

    CODECS()
    ----------
        >>> GET INFORMATION ABOUT AVAILABLE CODECS USING FFMPEG.

    FORMATS()
    ---------
       >>> GET INFORMATION ABOUT AVAILABLE FORMATS USING FFMPEG.


    """

    def __init__(self):
        """
        INITIALIZE THE FFPE INSTANCE.

        SETS THE DEFAULT PATH TO THE FFMPEG EXECUTABLE AND INITIALIZES THE LOGGER.
        """
        self.ffmpeg_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "bin", "ffmpeg.exe"
        )
        self.logger = self._initialize_logger()

    def _initialize_logger(self) -> logging.Logger:
        """
        >>> INITIALIZE THE LOGGER FOR LOGGING MESSAGES.

        RETURNS
        -------
        LOGGING.LOGGER
            LOGGER INSTANCE.
        """
        logger = logging.getLogger("ffpe_logger")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger

    def convert(
        self,
        input_files: Optional[List[str]] = None,
        input_file: Optional[str] = None,
        output_dir: Optional[str] = None,
        cv: Optional[str] = None,
        ca: Optional[str] = None,
        s: Optional[str] = None,
        hwaccel: Optional[str] = None,
        ar: Optional[int] = None,
        ac: Optional[int] = None,
        ba: Optional[int] = None,
        r: Optional[int] = None,
        f: Optional[str] = None,
        preset: Optional[str] = None,
        bv: Optional[int] = None,
    ) -> None:
        """

            >>> EXAMPLE

             ```python
            =================================================================
             # INSTANTIATE THE FFPE CLASS

             from <library name> import *
             ffpe_instance = ffpe()

             # Define input files and output directory
            ... input_files = ['input1.mp4', 'input2.mp4'] # input_files [MULTIPLE CONVERT]
            ... input_file = ['input1.mp4']               # input_file [SINGLE CONVERT]

             output_dir = 'output_folder'

             # PERFORM MULTIMEDIA FILE CONVERSION USING FFMPEG
             ffpe_instance.convert(
                 input_files=input_files,
                 output_dir=output_dir,
                 cv='h264',        # VIDEO CODEC
                 ca='aac',         # AUDIO CODEC
                 s='1920x1080',    # VIDEO RESOLUTION
                 hwaccel='cuda',   # HARDWARE ACCELERATION
                 ar=44100,         # AUDIO SAMPLE RATE
                 ac=2,             # AUDIO CHANNELS
                 ba=192000,        # AUDIO BITRATE
                 r=30,             # VIDEO FRAME RATE
                 f='mp4',          # OUTPUT FORMAT
                 preset='fast',    # PRESET FOR ENCODING
                 bv=2000           # VIDEO BITRATE
             )
            - NOTE - ALWAYS SET INPUT FILE PATH IN SQUARE BRACKETS:
            - EXAMPLE-1 - input_files=[r"PATH_TO_INPUT_FILE"] # SINGLE CONVERTION
            - EXAMPLE-2 - input_files=[
            r"PATH_TO_INPUT_FILE_1",
            r"PATH_TO_INPUT_FILE_2"
        ] # MULTIPLE CONVERTION


        -

             ```
        """
        if not input_files and not input_file:
            self.logger.error("No input files provided.")
            return

        # HANDLE SINGLE FILE CONVERSION WITHOUT SQUARE BRACKETS
        if input_file:
            input_files = [input_file]

        threads = []
        for input_file in input_files:
            # EXTRACT THE FILENAME FROM THE INPUT PATH
            filename = os.path.basename(input_file)

            # CREATE THE OUTPUT FILE PATH BY JOINING THE OUTPUT_DIR AND FILENAME
            output_file = os.path.join(output_dir, filename)

            # CREATE A THREAD FOR EACH CONVERSION
            t = Thread(
                target=self._convert_single,
                args=(
                    input_file,
                    output_file,
                    cv,
                    ca,
                    s,
                    hwaccel,
                    ar,
                    ac,
                    ba,
                    r,
                    f,
                    preset,
                    bv,
                ),
            )
            threads.append(t)
            t.start()

        # WAIT FOR ALL THREADS TO FINISH
        for thread in threads:
            thread.join()

    @lru_cache(maxsize=None)
    def _convert_single(
        self,
        input_file: str,
        output_file: str,
        cv: Optional[str] = None,
        ca: Optional[str] = None,
        s: Optional[str] = None,
        hwaccel: Optional[str] = None,
        ar: Optional[int] = None,
        ac: Optional[int] = None,
        ba: Optional[int] = None,
        r: Optional[int] = None,
        f: Optional[str] = None,
        preset: Optional[str] = None,
        bv: Optional[int] = None,
    ) -> None:
        """

            >>> EXAMPLE


             ```python
            =================================================================
             # INSTANTIATE THE FFPE CLASS

             from <library name> import *
             ffpe_instance = ffpe()

             # DEFINE INPUT FILES AND OUTPUT DIRECTORY
            ... input_files = ['input1.mp4', 'input2.mp4'] # input_files [MULTIPLE CONVERT]
            ... input_file = ['input1.mp4']               # input_file [SINGLE CONVERT]

             output_dir = 'output_folder'

             # PERFORM MULTIMEDIA FILE CONVERSION USING FFMPEG
             ffpe_instance.convert(
                 input_files=input_files,
                 output_dir=output_dir,
                 cv='h264',        # VIDEO CODEC
                 ca='aac',         # AUDIO CODEC
                 s='1920x1080',    # VIDEO RESOLUTION
                 hwaccel='cuda',   # HARDWARE ACCELERATION
                 ar=44100,         # AUDIO SAMPLE RATE
                 ac=2,             # AUDIO CHANNELS
                 ba=192000,        # AUDIO BITRATE
                 r=30,             # VIDEO FRAME RATE
                 f='mp4',          # OUTPUT FORMAT
                 preset='fast',    # PRESET FOR ENCODING
                 bv=2000           # VIDEO BITRATE
             )
            - NOTE - ALWAYS SET INPUT FILE PATH IN SQUARE BRACKETS:
            - EXAMPLE-1 - input_files=[r"PATH_TO_INPUT_FILE"] # SINGLE CONVERTION
            - EXAMPLE-2 - input_files=[
            r"PATH_TO_INPUT_FILE_1",
            r"PATH_TO_INPUT_FILE_2"
        ] # MULTIPLE CONVERTION


        -

             ```
        """
        # BUILD THE FFMPEG COMMAND BASED ON THE PROVIDED PARAMETERS
        command = [self.ffmpeg_path, "-hide_banner"]

        if hwaccel:
            command += ["-hwaccel", hwaccel]

        command += ["-i", input_file]

        if cv:
            command += ["-c:v", cv]
        if ca:
            command += ["-c:a", ca]
        if s:
            command += ["-s", s]
        if ar:
            command += ["-ar", str(ar)]
        if ac:
            command += ["-ac", str(ac)]
        if ba:
            command += ["-b:a", str(ba)]
        if r:
            command += ["-r", str(r)]
        if f:
            command += ["-f", f]
        if preset:
            command += ["-preset", preset]
        if bv:
            command += ["-b:v", str(bv)]

        if output_file:
            command += ["-y", output_file]

        try:
            # EXECUTE THE FFMPEG COMMAND
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg command failed with error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Call the garbage collector to free up resources
        gc.collect()

    def codecs(self) -> None:
        """
            >>> GET INFORMATION ABOUT AVAILABLE CODECS USING FFMPEG.

        >>> EXAMPLE


         ```python
        =================================================================
            >>> from FFMPEG import *
            >>> ffmpe = ffpe()
            >>> ffmpe.codecs()
            ```

            ... RETURNS
            -------
            NONE
        """
        command = [self.ffmpeg_path, "-codecs"]
        try:
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            output = result.stdout.decode("utf-8")
            lines = output.split("\n")
            print("Available Codecs:\n")
            print("{:<20} {:<25} {:<60}".format("Codec", "Type", "Description"))
            print("{:<20} {:<25} {:<60}".format("-----", "----", "-----------"))
            for line in lines[11:]:  # Skip the header lines
                if line:  # Skip empty lines
                    fields = line.split()
                    if len(fields) >= 4:  # Ensure there are enough fields
                        codec_name = fields[1]
                        codec_type = fields[2].strip("()")
                        codec_description = " ".join(fields[3:])
                        print(
                            "{:<20} {:<25} {:<60}".format(
                                codec_name, codec_type, codec_description
                            )
                        )
                        print("-" * 150)  # Print a line
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg command failed with error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        gc.collect()

    def formats(self) -> None:  # CALL THE GARBAGE COLLECTOR TO FREE UP RESOURCES
        """
            >>> GET INFORMATION ABOUT AVAILABLE FORMATS USING FFMPEG.

        >>> EXAMPLE


         ```python
        =================================================================
            >>> from FFMPEG import *
            >>> ffmpe = ffpe()
            >>> ffmpe.formats()
            ```

            ... RETURNS
            -------
            NONE
        """
        command = [self.ffmpeg_path, "-formats"]
        try:
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            output = result.stdout.decode("utf-8")
            lines = output.split("\n")
            print("Available formats:\n")
            print("{:<30} {:<80}".format("Format", "Description"))
            print("{:<30} {:<80}".format("------", "-----------"))
            for line in lines[5:]:  # SKIP THE HEADER LINES
                if line:  # SKIP EMPTY LINES
                    fields = line.split()
                    if len(fields) >= 2:  # ENSURE THERE ARE ENOUGH FIELDS
                        format_name = fields[1]
                        format_description = " ".join(fields[2:])
                        print("{:<30} {:<80}".format(format_name, format_description))
                        print("-" * 100)  # PRINT A LINE
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg command failed with error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        gc.collect()


# CALL THE GARBAGE COLLECTOR TO FREE UP RESOURCES
