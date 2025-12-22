import zlib
import random

# ===============================
# 1. Basic Conversions
# ===============================

def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bin_to_text(bin_str):
    result = ""
    for i in range(0, len(bin_str), 8):
        byte = bin_str[i:i+8]
        if len(byte) == 8:
            val = int(byte, 2)
            if 32 <= val <= 126:
                result += chr(val)
            else:
                result += '?'
    return result

# ===============================
# 2. Error Detection Algorithms
# ===============================

def get_parity(data, mode='even'):
    bits = text_to_bin(data)
    ones = bits.count('1')

    if mode == 'even':
        return '0' if ones % 2 == 0 else '1'
    else:
        return '1' if ones % 2 == 0 else '0'

def get_2d_parity(data):
    if not data:
        return "0|0"

    rows = [format(ord(c), '08b') for c in data]
    row_parity = ''.join('1' if r.count('1') % 2 else '0' for r in rows)

    col_parity = ""
    for i in range(8):
        col = [row[i] for row in rows]
        col_parity += '1' if col.count('1') % 2 else '0'

    return f"{row_parity}|{col_parity}"

def get_crc(data):
    crc_val = zlib.crc32(data.encode()) & 0xffffffff
    return format(crc_val, '08X')

def get_checksum(data):
    data_bytes = data.encode()
    if len(data_bytes) % 2 != 0:
        data_bytes += b'\x00'

    total = 0
    for i in range(0, len(data_bytes), 2):
        word = (data_bytes[i] << 8) + data_bytes[i+1]
        total += word
        total = (total & 0xFFFF) + (total >> 16)

    return format(~total & 0xFFFF, '04X')

# ===============================
# 3. Hamming (7,4)
# ===============================

def get_hamming(data):
    bits = text_to_bin(data)
    encoded = ""

    for i in range(0, len(bits), 4):
        block = bits[i:i+4].ljust(4, '0')
        d1, d2, d3, d4 = map(int, block)

        p1 = (d1 + d2 + d4) % 2
        p2 = (d1 + d3 + d4) % 2
        p3 = (d2 + d3 + d4) % 2

        encoded += f"{p1}{p2}{d1}{p3}{d2}{d3}{d4}"

    return encoded

def correct_hamming(received_data, sent_control):
    corrected = False
    fixed_bits = ""

    for i in range(0, len(sent_control), 7):
        block = sent_control[i:i+7]
        if len(block) < 7:
            continue

        b = list(map(int, block))
        p1, p2, d1, p3, d2, d3, d4 = b

        c1 = (p1 + d1 + d2 + d4) % 2
        c2 = (p2 + d1 + d3 + d4) % 2
        c3 = (p3 + d2 + d3 + d4) % 2

        error_pos = c3 * 4 + c2 * 2 + c1

        if error_pos != 0:
            b[error_pos - 1] ^= 1
            corrected = True

        fixed_bits += f"{b[2]}{b[4]}{b[5]}{b[6]}"

    return bin_to_text(fixed_bits), corrected

# ===============================
# 4. Dispatcher
# ===============================

def generate_control_info(data, method):
    if method == "Parity":
        return get_parity(data)
    elif method == "2D Parity":
        return get_2d_parity(data)
    elif method == "CRC":
        return get_crc(data)
    elif method == "Hamming":
        return get_hamming(data)
    elif method == "Checksum":
        return get_checksum(data)
    return "0"

# ===============================
# 5. Error Injection (Server)
# ===============================

def inject_error(data, error_type):
    if not data:
        return data

    data_list = list(data)

    if error_type == '1':  # Bit Flip
        idx = random.randint(0, len(data_list) - 1)
        bit = random.randint(0, 7)
        new_val = ord(data_list[idx]) ^ (1 << bit)
        data_list[idx] = chr(new_val if 32 <= new_val <= 126 else ord(data_list[idx]))

    elif error_type == '2':  # Char Substitution
        i = random.randint(0, len(data_list) - 1)
        data_list[i] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    elif error_type == '3':  # Char Deletion
        if len(data_list) > 1:
            data_list.pop(random.randint(0, len(data_list) - 1))

    elif error_type == '4':  # Char Insertion
        data_list.insert(random.randint(0, len(data_list)), random.choice("XYZ"))

    elif error_type == '5':  # Char Swapping
        if len(data_list) >= 2:
            i = random.randint(0, len(data_list) - 2)
            data_list[i], data_list[i+1] = data_list[i+1], data_list[i]

    elif error_type == '6':  # Multiple Bit Flips
        for _ in range(2):
            data = inject_error("".join(data_list), '1')
            data_list = list(data)

    elif error_type == '7':  # Burst Error (Characters)
        length = random.randint(3, min(8, len(data_list)))
        start = random.randint(0, len(data_list) - length)
        for i in range(start, start + length):
            data_list[i] = random.choice("!@#$%^&*")

    return "".join(data_list)
