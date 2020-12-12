#
# 17/02/2019
# Juan M. Casillas <juanm.casillas@gmail.com>
# https://github.com/juanmcasillas/gopro2gpx.git
#
# Released under GNU GENERAL PUBLIC LICENSE v3. (Use at your own risk)
#

import configparser
import os
import platform


class Config:
    # pylint: disable=too-few-public-methods
    def __init__(self, ffmpeg, ffprobe):
        self.ffmpeg_cmd = ffmpeg
        self.ffprobe_cmd = ffprobe

        self.verbose = False
        self.inputfile = None
        self.outputfile = None

    def set_cli_options(self, verbose, inputfile, outputfile):
        self.verbose = verbose
        self.inputfile = inputfile
        self.outputfile = outputfile


def setup_environment(args):
    """
    Setup ffmpeg environment and commandline arguments.
    First check for config file, if it doesn't exist ffmpeg is assumed to be installed
    somewhere in PATH
    """
    windows = platform.system() == "Windows"
    # find config path depending on OS
    if windows:
        config_path = os.path.expandvars(r"%APPDATA%\gopro2gpx\gopro2gpx.conf")
    else:
        if os.environ.get("XDG_CONFIG_HOME", False):
            config_path = os.path.expandvars("$XDG_CONFIG_HOME/gopro2gpx.conf")
        else:
            config_path = os.path.expandvars("$HOME/.config/gopro2gpx.conf")

    # read config if it exists
    if os.path.exists(config_path):
        conf = configparser.ConfigParser()
        conf.read(config_path)
        ffmpeg, ffprobe = conf["ffmpeg"]["ffmpeg"], conf["ffmpeg"]["ffprobe"]
    else:
        # otherwise assume ffmpeg and ffprobe are in path
        if windows:
            ffmpeg, ffprobe = "ffmpeg.exe", "ffprobe.exe"
        else:
            ffmpeg, ffprobe = "ffmpeg", "ffprobe"

    config = Config(ffmpeg, ffprobe)

    # configure CLI arguments
    config.set_cli_options(args.verbose, args.file, args.outputfile)

    return config
