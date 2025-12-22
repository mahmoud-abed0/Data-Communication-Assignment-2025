# server.py
import socket
import config
from utils import inject_error

def start_server():
    print(">>> Server (Intermediate + Corruptor) Started")


    try:
        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiver_socket.connect((config.HOST, config.PORT_CLIENT2))
        print(">>> Connected to Receiver")
    except:
        print("❌ Receiver not running! Start receiver.py first.")
        return


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((config.HOST, config.PORT_SERVER))
        s.listen(1)
        print(f">>> Listening for Sender on port {config.PORT_SERVER}...")

        conn, addr = s.accept()
        with conn:
            print(f">>> Sender connected: {addr}")

            while True:
                packet = conn.recv(config.BUFFER_SIZE).decode(config.DEFAULT_ENCODING)
                if not packet:
                    break

                print("\n[NEW PACKET] Incoming:", packet)

                parts = packet.split("|")
                if len(parts) < 3:
                    continue

                data = "|".join(parts[:-2])
                method = parts[-2]
                control = parts[-1]


                print("""
0. None
1. Bit Flip
2. Char Substitution
3. Char Deletion
4. Char Insertion
5. Char Swapping
6. Multiple Bit Flips
7. Burst Error
""")
                error_type = input(">>> Select Error Type (0-7): ")

                corrupted_data = inject_error(data, error_type)

                new_packet = f"{corrupted_data}|{method}|{control}"
                receiver_socket.sendall(new_packet.encode(config.DEFAULT_ENCODING))

                print(f"[FORWARDED] {new_packet}")

    receiver_socket.close()

if __name__ == "__main__":
    start_server()
