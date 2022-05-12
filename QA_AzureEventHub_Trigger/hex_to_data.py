"""
functions responsible for decoding the hexidecimal data into a python
dictionary that contains the meaningful environment data.
"""


def decoder(hexdata):
    '''
    Decodes the encoded uplink data into a dictionary containing the
    temperature and humidity data.  This is the decode functions for the
    Milesight EM300-TH-868M temperature and humidity sensor.  It is likely
    that this will need updating for a different sensor.
    '''
    data = hex_to_decimal_array(hexdata)
    decoded = {}
    j = 0
    while j < len(data):
        channel_id = data[j]
        channel_type = data[j+1]
        j += 2
        # Battery
        if (int(channel_id) == 0x01 and int(channel_type) == 0x75):
            decoded["battery"] = data[j]
            j += 1
        # Temperature
        elif (int(channel_id) == 0x03 and int(channel_type) == 0x67):
            required_slice = slice(j, j+2)
            decoded["temperature"] = read_int_16le(data[required_slice]) / 10
            j += 2
        # Humidity
        elif (int(channel_id) == 0x04 and int(channel_type) == 0x68):
            decoded["humidity"] = data[j] / 2
            j += 1
        else:
            break

    return decoded


def read_uint_16le(value):
    '''
    Required function when determining the temperature value
    '''
    uint_value = (value[1] << 8) + value[0]
    return uint_value & 0xffff


def read_int_16le(value):
    '''
    Required function when determining the temperature value
    '''
    int_value = read_uint_16le(value)
    return int_value - 0x10000 if int_value > 0x7fff else int_value


def hex_to_decimal_array(hexdata):
    '''
    Converts hex data to decimal array for the decode function.
    '''
    if len(hexdata) % 2 != 0:
        print("Error: There must be an even number of hex digits to convert to decimals")
    else:
        decimal_array = []
        i = 0
        while i < len(hexdata):
            hex_value = hexdata[i:i+2]
            decimal_array.append(int(hex_value, 16))
            i += 2

        return decimal_array
