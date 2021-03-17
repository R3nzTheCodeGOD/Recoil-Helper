# -*- coding: utf-8 -*-
__author__: str = "Erdem Yılmaz"
__version__: str = "1.0.0"

import pyautogui
import time
import win32api
import random
import keyboard
import configparser
import winsound
import os
import colorama

colorama.init()

class Color:
    "ColorText Console"
    @staticmethod
    def red(text: str) -> str:
        "Return red text"
        return colorama.Fore.RED + str(text) + colorama.Style.RESET_ALL

    @staticmethod
    def blue(text: str) -> str:
        "Return blue text"
        return colorama.Fore.BLUE + str(text) + colorama.Style.RESET_ALL

    @staticmethod
    def bright(text: str) -> str:
        "Return bright text"
        return colorama.Style.BRIGHT + str(text) + colorama.Style.RESET_ALL

    @staticmethod
    def yellow(text: str) -> str:
        "Return yellow text"
        return colorama.Fore.YELLOW + str(text) + colorama.Style.RESET_ALL

    @staticmethod
    def green(text: str) -> str:
        "Return green text"
        return colorama.Fore.GREEN + str(text) + colorama.Style.RESET_ALL

class Recoil:
    "Base Recoil Class"
    def __init__(self, *args: list, **kwargs: dict) -> None:
        super().__init__()
        self.kwargs: dict = kwargs
        self.min_horizontal: float = self.kwargs.get("min_horizontal", -1.0)
        self.max_horizontal: float = self.kwargs.get("max_horizontal", 1.0)
        self.min_vertical: float = self.kwargs.get("min_vertical", 2.0)
        self.max_vertical: float = self.kwargs.get("max_vertical", 3.0)
        self.min_firerate: float = self.kwargs.get("min_firerate", 0.03)
        self.max_firerate: float = self.kwargs.get("max_firerate", 0.04)
        self.toggle_key: str = self.kwargs.get("toggle_key", "F6")
        self.log_state: bool = self.kwargs.get("log", False)
        self.run_state: bool = False
        self.last_state: bool = False
        self.const_offset: int = 1000
        self.color = Color()
    
    def activate(self) -> None:
        "Active Script"
        self.run_state = not self.run_state
        if self.run_state:
            winsound.Beep(400, 400)
        else:
            winsound.Beep(500, 400)

    @staticmethod
    def is_mouse_press() -> bool:
        "Get Mouse Press State"
        lmb_state = win32api.GetKeyState(0x01)
        return lmb_state < 0

    def get_horizontal(self) -> int:
        "Get Horizontal Pattern"
        if self.min_horizontal == 0 and self.max_horizontal == 0:
            return 0
        else:
            return int(random.randrange(self.min_horizontal * self.const_offset, self.max_horizontal * self.const_offset, 1) / self.const_offset)
    
    def get_vertical(self) -> int:
        "Get Vertical Pattern"
        if self.min_vertical == self.max_vertical:
            return int(self.min_vertical)
        else:
            return int(random.randrange(self.min_vertical * self.const_offset, self.max_vertical * self.const_offset, 1) / self.const_offset)
    
    def get_firerate(self) -> float:
        "Get Random Time"
        if self.min_firerate == self.max_firerate:
            return float(self.min_firerate)
        else:
            return float(random.randrange(self.min_firerate * self.const_offset, self.max_firerate * self.const_offset, 1) / self.const_offset)

    def mouse_move(self, horizontal_offset, vertical_offset) -> None:
        "Mouse Move Func"
        win32api.mouse_event(0x0001, horizontal_offset, vertical_offset)
        if self.log_state is True:
            print(self.color.green(f"Vertical: {vertical_offset} | Horizontal: {horizontal_offset}"))

    def start(self) -> None:
        "Run Recoil System"
        while True:
            key_down: bool = keyboard.is_pressed(self.toggle_key)
            if key_down != self.last_state:
                self.last_state = key_down
                if self.last_state:
                    self.activate()

            if self.is_mouse_press() and self.run_state:
                self.mouse_move(self.get_horizontal(), self.get_vertical())
                time.sleep(self.get_firerate())
            
            time.sleep(0.001)

def main() -> None:
    "Main Func"
    cfg = configparser.ConfigParser()
    clr = Color()
    
    try:
        cfg.read("config.ini")
    except configparser.NoSectionError:
        print(clr.red("English: File named 'config.ini' not found starting at default settings.\nTürkçe: 'Config.ini' adlı dosya bulunamadı varsayılan ayarlarda başlatılıyor."))
        time.sleep(3.5)
        os.system("cls")
        r3nz = Recoil()
        print(clr.bright(clr.blue("[R3nzTheCodeGOD] Recoil Helper")))
        print(clr.yellow(f"On/Off Button: {r3nz.toggle_key}"))
        r3nz.start()
    
    else:
        os.system("cls")
        r3nz = Recoil(
            min_horizontal=float(cfg.get("config", "min_horizontal")),
            max_horizontal=float(cfg.get("config", "max_horizontal")),
            min_vertical=float(cfg.get("config", "min_vertical")),
            max_vertical=float(cfg.get("config", "max_vertical")),
            min_firerate=float(cfg.get("config", "min_firerate")),
            max_firerate=float(cfg.get("config", "max_firerate")),
            toggle_key=str(cfg.get("config", "toggle_key")),
            log=True if cfg.get("config", "log") == "True" else False)
        lang: str = str(cfg.get("lang", "lang"))
        if lang == "tr_TR":
            print(clr.bright(clr.blue("[R3nzTheCodeGOD] Spray Yardımcı")))
            print(f"Minimum Dikey Çekme: {clr.green(r3nz.min_vertical)}")
            print(f"Maximum Dikey Çekme: {clr.green(r3nz.max_vertical)}")
            print(f"Minimum Yatay Çekme: {clr.green(r3nz.min_horizontal)}")
            print(f"Maximum Yatay Çekme: {clr.green(r3nz.max_vertical)}")
            print(f"Minimum Ateş Sıklığı: {clr.green(r3nz.min_firerate)}")
            print(f"Maximum Ateş Sıklığı: {clr.green(r3nz.max_firerate)}")
            print(f"Aç/Kapat Tuşu: {clr.green(r3nz.toggle_key)}")
            print(f"Konsol Loglama: {clr.green('Açık') if r3nz.log_state else clr.red('Kapalı')}")
            print(clr.yellow("Coded By Erdem"))
        else:
            print(clr.bright(clr.blue("[R3nzTheCodeGOD] Recoil Helper")))
            print(f"Minimum Vertical Traction: {clr.green(r3nz.min_vertical)}")
            print(f"Maximum Vertical Traction: {clr.green(r3nz.max_vertical)}")
            print(f"Minimum Horizontal Traction: {clr.green(r3nz.min_horizontal)}")
            print(f"Maximum Horizontal Traction: {clr.green(r3nz.max_vertical)}")
            print(f"Minimum Firerate: {clr.green(r3nz.min_firerate)}")
            print(f"Maximum Firerate: {clr.green(r3nz.max_firerate)}")
            print(f"On/Off key: {clr.green(r3nz.toggle_key)}")
            print(f"Console Log: {clr.green('Open') if r3nz.log_state else clr.red('Close')}")
            print(clr.yellow("Coded By Erdem"))
        r3nz.start()

if __name__ == "__main__":
    main()