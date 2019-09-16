from struct import unpack
from enum import Enum

# This script collects zip file's metadata into easily accessable classes
# Author: Otteri
#
# Data structure references (accessed 17.9.2019):
# Zip file:
# 1. https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
# 2. https://users.cs.jmu.edu/buchhofp/forensics/formats/pkzip.html
# Dos date time:
# https://docs.microsoft.com/en-us/windows/desktop/api/Winbase/nf-winbase-dosdatetimetofiletime

class Compression(Enum):
    STORE               = 0
    SHRUNK              = 1
    REDUCED_1           = 2
    REDUCED_2           = 3
    REDUCED_3           = 4
    REDUCED_4           = 5
    IMPLODED            = 6
    DEFLATE             = 8
    ENHANCED_DEFLATED   = 9
    PKWARE_DCL_IMPLODED = 10
    RESERVED            = 11
    BZIP2               = 12
    LZMA                = 14
    IBM_CMPSC           = 16
    IBM_TERSE           = 18
    IBM_LZ77_Z          = 19
    JPEG_VARIANT        = 96
    WAWPACK             = 97
    PPMD_VERSION_I      = 98

# Version block is two bytes long and holds information about two things:
# High byte tells a version type
# Low byte tells the zip specification version
class Version():
    class Versions(Enum):
        MS_DOS        = 0
        AMIGA         = 1
        OPENVMS       = 2
        UNIX          = 3
        VM_CMS        = 4
        ATARI_ST      = 5
        OS2_HPFS      = 6
        MACINTOSH     = 7
        Z_SYSTEM      = 8
        CP_M          = 9
        WINDOWS_NTFS  = 10
        MVS           = 11
        VSE           = 12
        ACRON_RISC    = 13
        VFAT          = 14
        ALTERNATE_MVS = 15
        BE_OS         = 16
        TANDEM        = 17
        OS_400        = 18
        OS_X          = 19
        UNUSED        = 20

    def __init__(self, new_value):
        b1, b2 = new_value.to_bytes(2, byteorder='big')
        self.value = new_value
        self.high_byte = b1
        self.low_byte = b2
        self.version_type = self.Versions(self.high_byte).name

    def __str__(self):
        return(str(self.value))

# Structure overview of a Zip file:
#    ___________________
#   |      Header 1     |
#   |    File data 1    |
#   | Data descriptor 1 |
#   |       ...         |
#   |     Header n      |
#   |   File data n     |
#   | Data descriptor n |
#   | Central directory |
#   |___________________|
# Header files contain useful metadata. 
# Find the headers and store the metadata.
class ZipInfo:
    def __init__(self, filename):
        self.local_file_headers = []
        self.central_directory_header = None

        with open(filename, 'rb') as data:
            for four_bytes in self.read_bytes_to_buffer(data, 4):
                bytelist = list(four_bytes)
                if (bytelist == ['0x50','0x4b','0x3','0x4']):
                    data.seek(data.tell() - 4) # go back to signature start
                    header = LocalFileHeader()
                    header.collect_header(data)
                    self.local_file_headers.append(header)
                elif (bytelist == ['0x50','0x4b','0x5','0x6']):
                    pass # End of central directory record
                         # TODO: collect this data
                elif (bytelist == ['0x50','0x4b','0x1','0x2']):
                    data.seek(data.tell() - 4)
                    central = CentralDirectoryHeader()
                    central.collect_central_directory_file_header(data)
                    self.central_directory_header = central


    # The zip files can be large, so we don't want to read the whole file into memory at once
    # While seeking certain byte pattern from the file's binary data, use a generator instead.
    # This sovles the possible memory consuption problems, because only small chunks of data
    # are read at time. Function yields twice because it returns multiple bytes at once. 
    # (single yield returns only one value).
    def read_bytes_to_buffer(self, file_object, bytes_n):
        chunksize = bytes_n
        def generator():
            n = 0
            for nbytes in chunk[n:n+bytes_n]:
                n += bytes_n
                yield hex(nbytes)      
        while True:
            chunk = file_object.read(chunksize)
            if not chunk:
                break
            yield generator()

    # date: two bytes that represent date in MS-DOS format
    # return: date as a string (format: MM/dd/yyyy).
    def dos_date_to_str(self, date):
        year_mask  = 0b1111111000000000
        month_mask = 0b0000000111100000
        day_mask   = 0b0000000000011111
        year  = ((date & year_mask) >> 9) + 1980
        month = (date & month_mask) >> 5
        day   = (date & day_mask)
        return("{:02d}/{:02d}/{:04d}".format(month, day, year))

    # time: two bytes that represent time in MS-DOS format
    # return: time as a string (format: HH:mm:ss)
    def dos_time_to_str(self, time):
        hour_mask   = 0b1111100000000000
        minute_mask = 0b0000011111100000
        second_mask = 0b0000000000011111
        hours   = ((time & hour_mask) >> 11) - 1
        minutes = (time & minute_mask) >> 5
        seconds = (time & second_mask) * 2
        return("{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds))

    # Returns signature as a string in following four bytes format: \x50\x4b\x03\x04
    # Note: all zip file signatures are 4 bytes long
    def get_signature_str(self, b):
        b1, b2, b3, b4 = b.to_bytes(4, byteorder='little')
        signature = [hex(b1), hex(b2), hex(b3), hex(b4)]
        return(''.join(str('\\' + e) for e in signature))

    # Python uses b' to indicate that object is a byte object.
    # This method removes the precending b' from printed string.
    def remove_b(self, byte_object):
        return str(byte_object).split("'")[1]

    # Creates an 'bit'-array that represents two bytes of data
    # E.g. 'General purpose flags' and 'Internal attributes'
    # use this kind of datastructure
    def read_16_bit_flags(self, general_flag):
        bits = [0] * 16
        for i in range(0, 15):
            if(general_flag & (1 << i)):
                bits[i] = 1
        return bits

class LocalFileHeader(ZipInfo):
    def __init__(self):
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

    # Fixed size stuff is read to fields with binary unpack and then
    # the varying length contents are then filled by using array tricks
    def collect_header(self, data):
        # read the fixed data bytes
        header_data = data.read(30)
        fields = unpack('<LHHHHHLLLHH', header_data[0:30])
        self.header_signature = self.get_signature_str(fields[0])
        self.minimum_version = fields[1]
        self.general_flag = fields[2]
        self.compression_method = Compression(fields[3]).name
        self.last_modification_time = self.dos_time_to_str(fields[4])
        self.last_modification_date = self.dos_date_to_str(fields[5])
        self.crc_32 = hex(fields[6])
        self.compressed_size = fields[7]
        self.uncompressed_size = fields[8]
        self.file_name_length = fields[9]
        self.extra_field_length = fields[10]

        # read the remaining variable amount of header bytes
        header_data = data.read(self.file_name_length + self.extra_field_length)
        self.file_name = self.remove_b(header_data[0:self.file_name_length])
        if(self.extra_field_length > 0):
            self.extra_field = header_data[self.file_name_length:
            self.file_name_length+self.extra_field_length]
        else:
            self.extra_field = '-'

    # Print all the classes attribute and value pairs
    def __str__(self):
        header_string = ""
        for attr, value in self.__dict__.items():
            header_string += attr + ': ' + str(value) + '\n'

        return(header_string)

class CentralDirectoryHeader(ZipInfo):
    def __init__(self):
        self.header_signature       = None
        self.version                = None
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
        self.file_comment_length    = None
        self.disk_number            = None
        self.internal_attributes    = None
        self.external_attributes    = None
        self.local_header_offset    = None      
        self.file_name              = None
        self.extra_field            = None
        self.file_comment           = None

    def collect_central_directory_file_header(self, data):       
        header_data = data.read(46) # read fixed data fields
        fields = unpack('<LHHHHHHLLLHHHHHLL', header_data[0:46])
        self.header_signature       = self.get_signature_str(fields[0])
        self.version                = Version(fields[1])
        self.minimum_version        = fields[2]
        self.general_flag           = fields[3]
        self.compression_method     = Compression(fields[4]).name
        self.last_modification_time = self.dos_time_to_str(fields[5])
        self.last_modification_date = self.dos_date_to_str(fields[6])
        self.crc_32                 = hex(fields[7])
        self.compressed_size        = fields[8]
        self.uncompressed_size      = fields[9]
        self.file_name_length       = fields[10]
        self.extra_field_length     = fields[11]
        self.file_comment_length    = fields[12]
        self.disk_number            = fields[13]
        self.internal_attributes    = fields[14]
        self.external_attributes    = fields[15]
        self.local_header_offset    = fields[16]     

        # read the remaining variable amount of header bytes
        header_data = data.read(self.file_name_length + self.extra_field_length + self.file_comment_length)
        self.file_name = self.remove_b(header_data[0:self.file_name_length])
        if (self.extra_field_length > 0):
            self.extra_field = header_data[self.file_name_length:
            self.file_name_length+self.extra_field_length]
        else:
            self.extra_field = '-'    
        if (self.file_comment_length > 0):
            self.file_comment = header_data[self.file_name_length + self.extra_field_length:
            self.file_name_length + self.extra_field_length + self.file_comment_length]
        else:
            self.file_comment = '-'             
        
    def __str__(self):
        header_string = ""
        for attr, value in self.__dict__.items():
            header_string += attr + ': ' + str(value) + '\n'
        return(header_string)



if __name__ == "__main__":
    file = input("Give path to Zip\n")
    zip_metadata = ZipInfo(file)
    
    # Print collected data fields:
    for local_header in zip_metadata.local_file_headers:
        print("[Local header]\n{}".format(local_header))
    print("[Central header]\n{}".format(zip_metadata.central_directory_header))