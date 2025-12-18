import socket
import config
from utils import generate_control_info, text_to_bin 

def start_receiver():
    print(f">>> Client 2 (Receiver) Started on port {config.PORT_CLIENT2}...")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((config.HOST, config.PORT_CLIENT2))
        s.listen()
        
        conn, addr = s.accept()
        with conn:
            print(f"Connected by Server: {addr}")
            while True:
                data = conn.recv(config.BUFFER_SIZE).decode(config.DEFAULT_ENCODING)
                if not data: break
                
                try:
                    parts = data.split('|')
                    if len(parts) < 3: continue

                    rec_data = "|".join(parts[:-2]) 
                    method = parts[-2]
                    rec_control = parts[-1]

                    
                    calc_control = generate_control_info(rec_data, method)
                    status_msg = ""
                    corrected_data = rec_data

                    if method == "Hamming" and rec_control != calc_control:
                        
                        sent_bin = bin(int(rec_control, 16))[2:]
                        calc_bin = bin(int(calc_control, 16))[2:]
                        
                       
                        if len(sent_bin) == len(calc_bin):
                            syndrome = int(rec_control, 16) ^ int(calc_control, 16)
                            status_msg = f" (Single Bit Error Detected! Syndrome: {hex(syndrome)})"

                        else:
                            status_msg = " (Major Error: Structure Changed)"



                    print("\n" + "="*50)
                    print(f"Received Data       : {rec_data}")
                    print(f"Method              : {method}")
                    print(f"Sent Check Bits     : {rec_control}")
                    print(f"Computed Check Bits : {calc_control}")
                    
                    if rec_control == calc_control:
                        print("Status              : DATA CORRECT (Hatasız)")
                    else:
                        print(f"Status              : DATA CORRUPTED (Hatalı){status_msg}")
                    print("="*50)

                except Exception as e:
                    print(f"Error processing packet: {e}")

if __name__ == "__main__":
    start_receiver()