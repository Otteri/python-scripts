from struct import unpack
from enum import Enum

# References [18.07.2018]:
# https://docs.microsoft.com/en-us/windows/desktop/api/Winbase/nf-winbase-dosdatetimetofiletime
# https://en.wikipedia.org/wiki/Zip_(file_format)
# https://users.cs.jmu.edu/buchhofp/forensics/formats/pkzip.html

class Compression(Enum):
    STORE = 0
    SHRUNK = 1
    IMPLODED = 6
    DEFLATE = 8
    ENHANCED_DEFLATED = 9
    PKWARE_DCL_IMPLODED = 10
    BZIP2 = 12
    LZMA = 14
    IBM_TERSE = 18
    IBM_LZ77_Z = 19
    PPMD_VERSION_I = 98

class ZipInfo(object):
    def __init__(self, filename):
        data = open(filename, 'rb')
        header = self.create_local_file_header()
        header.collect_header(data)

    def create_local_file_header(self):
        return ZipInfo.LocalFileHeader(self)

    def dos_date_to_str(self, date):
        year_mask  = 0b1111111000000000
        month_mask = 0b0000000111100000
        day_mask   = 0b0000000000011111
        year  = ((date & year_mask) >> 9) + 1980
        month = (date & month_mask) >> 5
        day   = (date & day_mask)
        print("date: {}.{}.{}".format(day, month, year))
        return("{:02d}/{:02d}/{:04d}".format(day, month, year))

    # @time: two bytes that represent time in MS-DOS format
    # @return: time as a string
    def dos_time_to_str(self, time):
        hour_mask   = 0b1111100000000000
        minute_mask = 0b0000011111100000
        second_mask = 0b0000000000011111
        hours   = (time & hour_mask) >> 11
        minutes = (time & minute_mask) >> 5
        seconds = (time & second_mask) * 2
        print("time: {}.{}.{}".format(hours, minutes, seconds))
        return("{:02d}.{:02d}.{:02d}".format(hours, minutes, seconds))

    # Python uses b' to indicate that object is a byte object.
    # This method removes the precending b' from a string.
    def remove_b(self, byte_object):
        return str(byte_object).split("'")[1]

    # Creates an array that represents the two bytes
    def read_general_purpose_flag_bits(self, general_flag):
        bits = [0] * 16
        for i in range(0, 15):
            if(general_flag & (1 << i)):
                bits[i] = 1
        return bits

    class LocalFileHeader(object):
        def __init__(self, outer):
            self.header_signature       = None
            self.minimum_version        = None
            self.general_flag           = None
            self.compression_method     = None
            self.last_modification_time = None
            self.last_modification_date = None
            self.crc_32                 = None
            self.compressed_size        = None
            self.uncompressed_size      = None
            self.file_name_length       = None
            self.extra_field_length     = None
            self.file_name              = None
            self.extra_field            = None
            self.outer                  = outer

        def collect_header(self, data):
            header_data = data.read(30) # read the fixed data bytes
            fields = unpack('<LHHHHHLLLHH', header_data[0:30])
            self.header_signature = self.outer.remove_b(header_data[0:4])
            self.minimum_version = fields[1]
            self.general_flag = fields[2]
            self.compression_method = Compression(fields[3]).name
            self.last_modification_time = self.outer.dos_time_to_str(fields[4])
            self.last_modification_date = self.outer.dos_date_to_str(fields[5])
            self.crc_32 = hex(fields[6])
            self.compressed_size = fields[7]
            self.uncompressed_size = fields[8]
            self.file_name_length = fields[9]
            self.extra_field_length = fields[10]
            # read the remaining variable amount of the header bytes
            header_data = data.read(self.file_name_length + self.extra_field_length)
            self.file_name = self.outer.remove_b(header_data[0:self.file_name_length])
            if(self.extra_field_length > 0):
                self.extra_field = header_data[self.file_name_length:
                self.file_name_length+self.extra_field_length]
            else:
                self.extra_field = '-'

            flag_array = self.outer.read_general_purpose_flag_bits(self.general_flag)
            print("general_flag: ", self.outer.read_general_purpose_flag_bits(self.general_flag))
            if(flag_array[2] == 1):
                self.read_data_descriptor(data)
            print(self)

        def read_data_descriptor(self, data):
            print("Implement me!")    

        def __str__(self):
            header_string = ""
            for attr, value in self.__dict__.items():
                if(attr != "outer"):
                    header_string += attr + ': ' + str(value) + '\n'
            return(header_string)

if __name__ == "__main__":
    file = input("Give path to Zip\n")
    Zip = ZipInfo(file)
