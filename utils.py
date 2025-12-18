import zlib


def text_to_bin(text):
    return ''.join(format(ord(i), '08b') for i in text)


def get_parity(data, mode='even'):
    binary_data = text_to_bin(data)
    count = binary_data.count('1')
    if mode == 'even':

        return '1' if count % 2 != 0 else '0'
    else:

        return '1' if count % 2 == 0 else '0'


def get_2d_parity(data):

    rows = [format(ord(c), '08b') for c in data]
    

    row_parities = []
    for r in rows:
        row_parities.append('1' if r.count('1') % 2 != 0 else '0')
    

    col_parities = []
    for i in range(8): 
        col_bits = [r[i] for r in rows]
        col_parities.append('1' if col_bits.count('1') % 2 != 0 else '0')
    

    return "".join(row_parities) + "-" + "".join(col_parities)


def get_crc(data):

    crc_val = zlib.crc32(data.encode()) & 0xffffffff
    return hex(crc_val)[2:].upper()


def get_hamming(data):
    
    bin_data = text_to_bin(data)
    m = len(bin_data)
    
    
    r = 0
    while (2**r) < (m + r + 1):
        r += 1
        

    res = []
    j = 0
    k = 0
    for i in range(1, m + r + 1):
        if i == 2**j:
            res.append(0)
            j += 1
        else:
            res.append(int(bin_data[k]))
            k += 1
            

    for i in range(r):
        pos = 2**i
        parity = 0
        for j in range(1, len(res) + 1):
            if j & pos: 
                parity ^= res[j-1]
        res[pos-1] = parity
        

    hamming_str = "".join(map(str, res))
    return hex(int(hamming_str, 2))[2:].upper()


def get_checksum(data):

    total = sum(ord(c) for c in data)
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return hex(~total & 0xFFFF)[2:].upper()

def generate_control_info(data, method):
    if method == "Parity": return get_parity(data, 'even')
    elif method == "2D Parity": return get_2d_parity(data)
    elif method == "CRC": return get_crc(data)
    elif method == "Hamming": return get_hamming(data)
    elif method == "Checksum": return get_checksum(data)
    return "0"