import socket
import random
import config
import time


def char_to_bits(data):
    return ''.join(format(ord(c), '08b') for c in data)

def bits_to_char(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)


def bit_flip(data):
    bits = char_to_bits(data)
    if not bits: return data
    pos = random.randint(0, len(bits)-1)
    bit_list = list(bits)
    bit_list[pos] = '1' if bit_list[pos] == '0' else '0'
    return bits_to_char(''.join(bit_list))

def multi_flip(data):
    bits = list(char_to_bits(data))
    if not bits: return data
    for _ in range(random.randint(2, 4)):
        i = random.randint(0, len(bits)-1)
        bits[i] = '1' if bits[i] == '0' else '0'
    return bits_to_char(''.join(bits))

def burst_error(data):
    bits = list(char_to_bits(data))
    if len(bits) < 5: return data
    length = random.randint(3, 8)
    start = random.randint(0, max(0, len(bits)-length))
    for i in range(start, min(start+length, len(bits))):
        bits[i] = '1' if bits[i] == '0' else '0'
    return bits_to_char(''.join(bits))


def inject_error_manual(data):
    error_types = [
        ("None", lambda x: x),
        ("Bit Flip (Binary)", bit_flip),
        ("Char Substitution", lambda d: d[:(i:=random.randint(0,len(d)-1))] + chr(random.randint(32,126)) + d[i+1:]),
        ("Char Deletion", lambda d: d[:(i:=random.randint(0,len(d)-1))] + d[i+1:] if len(d)>1 else d),
        ("Char Insertion", lambda d: d[:(i:=random.randint(0,len(d)))] + chr(random.randint(32,126)) + d[i:]),
        ("Char Swapping", lambda d: (l:=list(d), (i:=random.randint(0,max(0,len(d)-2))), (l.__setitem__(i, l[i+1]), l.__setitem__(i+1, l[i])), "".join(l))[3] if len(d)>1 else d),
        ("Multiple Bit Flips", multi_flip),
        ("Burst Error (Binary)", burst_error)
    ]
    
  
    print("\n" + "!"*5 + " WAITING FOR YOUR INPUT " + "!"*5)
    print("SELECT ERROR TYPE TO INJECT:")
    for i, (name, _) in enumerate(error_types):
        print(f"{i}. {name}")
    
    while True:
        try:
            choice_str = input(">>> Enter your choice (0-7): ").strip()
            if choice_str == "": continue 
            choice_idx = int(choice_str)
            if 0 <= choice_idx <= 7:
                name, func = error_types[choice_idx]
                break
            else:
                print("Invalid range! Please enter a number between 0 and 7.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    corrupted = func(data)
    print(f"    [Action] Applied: {name}")
    print(f"    [Result] '{data}' -> '{corrupted}'")
    return corrupted

def start_server():
    print(">>> MANUAL HYBRID SERVER Started.")
    
    
    try:
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_socket.connect((config.HOST, config.PORT_CLIENT2))
        print(f"    [Status] Connected to Receiver.")
    except:
        print("    [Error] Receiver not found! Run receiver.py first.")
        return


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((config.HOST, config.PORT_SERVER))
        s.listen(1)
        print(f"    [Status] Listening for Sender on {config.PORT_SERVER}...")
        
        conn, addr = s.accept()
        with conn:
            print(f"    [Status] Sender {addr} is connected.")
            while True:

                packet = conn.recv(4096).decode(config.DEFAULT_ENCODING)
                if not packet: break
                
                print(f"\n[NEW PACKET] Incoming: {packet}")
                
                parts = packet.split('|')
                if len(parts) >= 3:
                    data = "|".join(parts[:-2])
                    method = parts[-2]
                    control = parts[-1]


                    corrupted_data = inject_error_manual(data)


                    new_packet = f"{corrupted_data}|{method}|{control}"
                    sender_socket.sendall(new_packet.encode(config.DEFAULT_ENCODING))
                    print(f"    [Status] Packet forwarded to Receiver.")

    sender_socket.close()

if __name__ == "__main__":
    start_server()