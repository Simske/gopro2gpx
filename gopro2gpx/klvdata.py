#
# 17/02/2019
# Juan M. Casillas <juanm.casillas@gmail.com>
# https://github.com/juanmcasillas/gopro2gpx.git
#
# Released under GNU GENERAL PUBLIC LICENSE v3. (Use at your own risk)
#

import struct

from . import fourCC


class KLVData:
    """
    format: Header: 32-bit, 8-bit, 8-bit, 16-bit
            Data: 32-bit aligned, padded with 0
    """

    # pylint: disable=too-many-instance-attributes

    binary_format = ">4sBBH"

    def __init__(self, data, offset):
        binary_struct = struct.Struct(KLVData.binary_format)  # unsigned bytes!
        (
            self.fourCC,  # pylint: disable=invalid-name
            self.type,
            self.size,
            self.repeat,
        ) = binary_struct.unpack_from(data, offset=offset)
        self.fourCC = self.fourCC.decode()

        self.type = int(self.type)
        self.length = self.size * self.repeat
        self.padded_length = self.pad(self.length)

        # read now the data, in raw format
        self.rawdata = self.read_raw_data(data, offset)
        # process the label, if found
        self.data = fourCC.manage(self)

    def __str__(self):

        stype = chr(self.type)
        if self.type == 0:
            stype = "null"

        if self.rawdata:
            rawdata = self.rawdata
            rawdata = " ".join(format(x, "02x") for x in rawdata)
            rawdatas = self.rawdata[0:10]
        else:
            rawdata = "null"
            rawdatas = "null"

        return "fourCC=%s type=%s size=%d repeat=%s data={%s} raws=|%s| raw=[%s]" % (
            self.fourCC,
            stype,
            self.size,
            self.repeat,
            self.data,
            rawdatas,
            rawdata,
        )

    @staticmethod
    def pad(n, base=4):  # pylint: disable=invalid-name
        "padd the number so is % base == 0"
        if n % base == 0:
            return n
        return n + base - n % base

    def skip(self):
        return self.fourCC in fourCC.skip_labels

    def read_raw_data(self, data, offset):
        "read the raw data, don't process anything, just get the bytes"
        if self.type == 0:
            return None

        num_bytes = self.pad(self.size * self.repeat)
        if num_bytes == 0:
            # empty package.
            return None

        fmt = ">" + str(num_bytes) + "s"
        (rawdata,) = struct.Struct(fmt).unpack_from(data, offset=offset + 8)
        return rawdata
