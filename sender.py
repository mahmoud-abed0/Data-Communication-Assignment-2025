import socket
import config
from utils import generate_control_info

def start_sender():
    print(">>> Client 1 (Sender) Started.")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((config.HOST, config.PORT_SERVER))
            print(f">>> Connected to Server on port {config.PORT_SERVER}")
            
            while True:
                print("\n" + "-"*30)
                text = input("Enter text to send (or 'exit'): ")
                if text.lower() == 'exit': break

                print("\nSelect Detection Method:")
                print("1. Parity Bit")
                print("2. 2D Parity")
                print("3. CRC (Cyclic Redundancy Check)")
                print("4. Hamming Code")
                print("5. Internet Checksum")
                
                choice = input("Your Choice (1-5): ")
                
                method_map = {
                    "1": "Parity",
                    "2": "2D Parity",
                    "3": "CRC",
                    "4": "Hamming",
                    "5": "Checksum"
                }
                
                method = method_map.get(choice, "CRC") # الافتراضي هو CRC
                
                # توليد معلومات التحكم
                control_info = generate_control_info(text, method)
                print(f"Generated Control Info ({method}): {control_info}")
                
                # بناء وإرسال الحزمة
                packet = f"{text}|{method}|{control_info}"
                s.sendall(packet.encode(config.DEFAULT_ENCODING))
                print(">> Packet Sent Successfully.")

    except ConnectionRefusedError:
        print("[Error] Could not connect to Server. Ensure server_corruptor.py is running.")

if __name__ == "__main__":
    start_sender()