import requests
import datetime
import time
from colorama import init, Fore, Style
import os
init(autoreset=True)


def print_welcome_message():
    print(r"""
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "Roketo Lunar Program BOT")
    print(Fore.GREEN + Style.BRIGHT +
          "Update Link: https://github.com/Honguan/Roketo-Lunar-Program")
    print(Fore.BLUE + Style.BRIGHT +
          "Buy me a coffee :) USDT\n TRON : TPxoRzYQvEQ63J2QoJuJaQ8g5xZoXiiHdG\n BNB : 0xd30c141148c343f84a1ae9d55e3e76d148f9c39e")
    print(Fore.RED + Style.BRIGHT +
          "There is no sale, all sales are scams\n\n")


def get_headers(token):
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {token}',
        'origin': 'https://miniapp.roke.to',
        'priority': 'u=1, i',
        'referer': 'https://miniapp.roke.to/',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def nickname(ini_token):
    url = 'https://lunar-api.roke.to/users/me/'
    try:
        response = requests.get(url, headers=get_headers(ini_token))
        data = response.json()
        if response.status_code == 200:
            name = data['first_name'] + ' ' + data['last_name']
            return name
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return False


def dock_balance(ini_token):
    url = 'https://lunar-api.roke.to/dock/'
    response = requests.get(url, headers=get_headers(ini_token))
    data = response.json()
    try:
        response.raise_for_status()
        last_claimed_time = data['last_claimed_time']
        last_yield_time = data['last_yield_time']
        lunar_loot_speed_lvl = data['lunar_loot_speed_lvl']
        dock_size_lvl = data['dock_size_lvl']
        yield_percentage_lvl = data['yield_percentage_lvl']

        # Convert to datetime objects
        last_claimed_datetime = datetime.datetime.fromtimestamp(
            last_claimed_time)
        last_yield_datetime = datetime.datetime.fromtimestamp(last_yield_time)

        # Convert to strings without microseconds
        last_claimed_str = last_claimed_datetime.strftime('%Y-%m-%d %H:%M:%S')
        last_yield_str = last_yield_datetime.strftime('%Y-%m-%d %H:%M:%S')
        balance = round(data['balance'] / 100000000, 2)
        print(Fore.YELLOW + Style.BRIGHT + f"Loot Balance: {balance}", end=" ")
        print(Fore.YELLOW + Style.BRIGHT +
              f"Last Claimed Time: {last_claimed_str}")
        print(Fore.YELLOW + Style.BRIGHT +
              f"Last Yield Time: {last_yield_str}")
        return lunar_loot_speed_lvl, dock_size_lvl, yield_percentage_lvl
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")


def claim_mining(ini_token):
    url = 'https://lunar-api.roke.to/dock/idle-mining/'
    response = requests.post(url, headers=get_headers(ini_token))
    data = response.json()
    try:
        response.raise_for_status()
        print(Fore.YELLOW + Style.BRIGHT + f"claim_mining: {data}")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            print(Fore.BLUE + Style.BRIGHT + "You can't press the button yet")


def animate_energy_recharge(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(
                f"\r recharge energy {frame} - remaining time {remaining_time} second", end="", flush=True)
            time.sleep(0.25)
    print("\r Break time.", flush=True)


# def claim_last_yield(ini_token):  //no longer available
#     url = 'https://lunar-api.roke.to/dock/idle-yield/'
#     response = requests.post(url, headers=get_headers(ini_token))
#     data = response.json()
#     try:
#         response.raise_for_status()
#         print(f"detail: {data['detail']}")
#     except requests.exceptions.HTTPError as e:
#         print(f"HTTP Error: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")


def auto_upgrade_yield_percentage(ini_token):
    url = 'https://lunar-api.roke.to/dock/upgrades/yield_percentage/'
    response = requests.post(url, headers=get_headers(ini_token))
    data = response.json()
    try:
        response.raise_for_status()
        print(Fore.GREEN + Style.BRIGHT + f"Yield_Upgrade_Level: {data}")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            print(Fore.BLUE + Style.BRIGHT +
                  "Not enough money to upgrade yield_percentage")


def auto_upgrade_lunar_loot_speed(ini_token):
    url = 'https://lunar-api.roke.to/dock/upgrades/lunar_loot_speed/'
    response = requests.post(url, headers=get_headers(ini_token))
    data = response.json()
    try:
        response.raise_for_status()
        print(Fore.GREEN + Style.BRIGHT + f"Loot_Speed_Upgrade_Level: {data}")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            print(Fore.BLUE + Style.BRIGHT +
                  "Not enough money to upgrade loot_speed")


def auto_upgrade_dock_size(ini_token):
    url = 'https://lunar-api.roke.to/dock/upgrades/dock_size/'
    response = requests.post(url, headers=get_headers(ini_token))
    data = response.json()
    try:
        response.raise_for_status()
        print(Fore.GREEN + Style.BRIGHT + f"Dock_Size_Upgrade_Level: {data}")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            print(Fore.BLUE + Style.BRIGHT +
                  "Not enough money to upgrade dock_size")


def read_tokens():
    with open('initdata.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]


def main():
    print_welcome_message()

    clear_console()
    user_lunar_loot_speed_upgrades = input(
        "Auto loot speed upgrades ? (y /default n) : ") or 'n'
    if user_lunar_loot_speed_upgrades == 'y':
        max_lunar_loot_speed = int(input("Max Upgrade Until Level? : "))

    user_dock_size_upgrades = input(
        "Auto dock size upgrades ? (y /default n) : ") or 'n'
    if user_dock_size_upgrades == 'y':
        max_dock_size = int(input("Max Upgrade Until Level? : "))

    user_yield_percentage_upgrades = input(
        "Auto yield percentage upgrades ? (y /default n) : ") or 'n'
    if user_yield_percentage_upgrades == 'y':
        max_yield_percentage = int(input("Max Upgrade Until Level? : "))

    while True:
        print_welcome_message()
        tokens = read_tokens()
        for index, token in enumerate(tokens):
            if nickname(token) == False:
                continue
            print(
                f"{Fore.BLUE + Style.BRIGHT}\n========[{Fore.WHITE + Style.BRIGHT} Akun {index + 1}  {Fore.BLUE + Style.BRIGHT}]========")
            lunar_loot_speed_lvl, dock_size_lvl, yield_percentage_lvl = dock_balance(
                token)

            claim_mining(token)

            if user_lunar_loot_speed_upgrades == 'y' and lunar_loot_speed_lvl < max_lunar_loot_speed:
                auto_upgrade_lunar_loot_speed(token)
            elif user_dock_size_upgrades == 'y' and dock_size_lvl < max_dock_size:
                auto_upgrade_dock_size(token)
            elif user_yield_percentage_upgrades == 'y' and yield_percentage_lvl < max_yield_percentage:
                auto_upgrade_yield_percentage(token)

            print(
                f"{Fore.BLUE + Style.BRIGHT}===========================================")
        animate_energy_recharge(300)


if __name__ == "__main__":
    main()
