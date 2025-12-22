import socket
import config
from utils import generate_control_info, correct_hamming

def start_receiver():
    print(f">>>> Client 2 (Receiver) Started on port {config.PORT_CLIENT2}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((config.HOST, config.PORT_CLIENT2))
        s.listen()

        conn, addr = s.accept()
        with conn:
            print(f"Connected by Server: {addr}")

            while True:
                try:
                    packet = conn.recv(config.BUFFER_SIZE).decode(config.DEFAULT_ENCODING)
                    if not packet:
                        break

                    parts = packet.split('|')
                    if len(parts) < 3:
                        continue

                    rec_data = "|".join(parts[:-2])
                    method = parts[-2]
                    sent_control = parts[-1]

                    final_data = rec_data
                    recovered = False

                    # ======================
                    # Hamming Logic
                    # ======================
                    if method == "Hamming":
                        fixed_text, was_fixed = correct_hamming(rec_data, sent_control)

                        if was_fixed:
                            recomputed = generate_control_info(fixed_text, method)
                            if recomputed == sent_control:
                                final_data = fixed_text
                                recovered = True

                        calc_control = generate_control_info(final_data, method)

                    # ======================
                    # Other Methods
                    # ======================
                    else:
                        calc_control = generate_control_info(rec_data, method)

                    # ======================
                    # Output
                    # ======================
                    print("\n" + "=" * 60)
                    print(f"Received Data       : {rec_data}")

                    if recovered:
                        print(f"Corrected Data      : {final_data}")

                    print(f"Method              : {method}")
                    print(f"Sent Check Bits     : {sent_control}")
                    print(f"Computed Check Bits : {calc_control}")

                    if sent_control == calc_control and not recovered:
                        print("Status              : DATA CORRECT ✅")
                    elif recovered:
                        print("Status              : DATA RECOVERED by Hamming 🛠️")
                    else:
                        print("Status              : DATA CORRUPTED ⚠️")

                    print("=" * 60)

                except Exception as e:
                    print(f"Error processing packet: {e}")

if __name__ == "__main__":
    start_receiver()
