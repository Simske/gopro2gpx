#
# 17/02/2019
# Juan M. Casillas <juanm.casillas@gmail.com>
# https://github.com/juanmcasillas/gopro2gpx.git
#
# Released under GNU GENERAL PUBLIC LICENSE v3. (Use at your own risk)
#

import re
import subprocess


class FFMpegTools:
    def __init__(self, config):
        self.config = config

    @staticmethod
    def run_cmd(cmd, args):
        result = subprocess.run(
            [cmd] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )
        return result.stderr.decode("utf-8")

    @staticmethod
    def run_cmd_raw(cmd, args):
        result = subprocess.run(
            [cmd] + args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True
        )
        return result.stdout

    def get_metadata_track(self, fname):
        """
        % ffprobe GH010039.MP4 2>&1

        The channel marked as
            gpmd (Stream #0:3(eng): Data: none (gpmd / 0x646D7067), 29 kb/s (default))
        In this case, the stream #0:3 is the required one (get the 3)

        Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'GH010039.MP4':
            Stream #0:1(eng): Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz,
                                                stereo, fltp, 189 kb/s (default)
            Stream #0:2(eng): Data: none (tmcd / 0x64636D74), 0 kb/s (default)
            Stream #0:3(eng): Data: none (gpmd / 0x646D7067), 29 kb/s (default)
            Stream #0:4(eng): Data: none (fdsc / 0x63736466), 12 kb/s (default)
        """
        output = self.run_cmd(self.config.ffprobe_cmd, [fname])
        # Stream #0:3(eng): Data: bin_data (gpmd / 0x646D7067), 29 kb/s (default)
        # Stream #0:2(eng): Data: none (gpmd / 0x646D7067), 29 kb/s (default)
        reg = re.compile(r"Stream #\d:(\d)\(.+\): Data: \w+ \(gpmd", flags=re.I | re.M)
        match = reg.search(output)

        if not match:
            return None
        return (int(match.group(1)), match.group(0))

    def get_metadata(self, track, fname):

        output_file = "-"
        args = [
            "-y",
            "-i",
            fname,
            "-codec",
            "copy",
            "-map",
            "0:%d" % track,
            "-f",
            "rawvideo",
            output_file,
        ]
        output = self.run_cmd_raw(self.config.ffmpeg_cmd, args)
        return output
