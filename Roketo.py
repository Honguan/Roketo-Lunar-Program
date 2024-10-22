import json
import requests
import datetime
import time
from colorama import init, Fore, Style
import os
init(autoreset=True)


def print_welcome_message():  # 印出歡迎訊息
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


def get_headers(token):  # 取得標頭
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


def get_token_headers():  # 取得token標頭
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
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


def clear_console():  # 清空控制台
    os.system('cls' if os.name == 'nt' else 'clear')


def get_token(query_id):  # 取得token
    url = 'https://lunar-api.roke.to/token/'
    data = json.dumps({"init_data": query_id})
    try:
        response = requests.get(url, headers=get_token_headers(), data=data)
        data = response.json()
        if response.status_code == 200:
            access_token = data['access_token']
            return access_token
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return False
    except (KeyError, ValueError) as e:
        print(f"Invalid JSON response: {e}")
        return False


def nickname(ini_token):  # 取得暱稱
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
    except (KeyError, ValueError) as e:
        print(f"Invalid JSON response: {e}")
        return False


def dock_balance(ini_token):  # 取得礦石資訊
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

        last_claimed_datetime = datetime.datetime.fromtimestamp(
            last_claimed_time)
        last_yield_datetime = datetime.datetime.fromtimestamp(last_yield_time)

        last_claimed_str = last_claimed_datetime.strftime('%Y-%m-%d %H:%M:%S')
        last_yield_str = last_yield_datetime.strftime('%Y-%m-%d %H:%M:%S')
        balance = round(data['balance'] / 100000000, 2)
        print(Fore.YELLOW + Style.BRIGHT + f"Loot Balance: {balance}")
        print(Fore.YELLOW + Style.BRIGHT +
              f"Last Claimed Time: {last_claimed_str}")
        print(Fore.YELLOW + Style.BRIGHT +
              f"Last Yield Time: {last_yield_str}")
        return last_claimed_time, lunar_loot_speed_lvl, dock_size_lvl, yield_percentage_lvl
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Invalid JSON response: {e}")


def claim_ad(ini_token):  # 領取廣告礦石
    url = 'https://lunar-api.roke.to/ad-logs/'
    response = requests.post(url, headers=get_headers(ini_token))
    ad_logs_count, ad_logs_count_limit = 0, 0
    try:
        response.raise_for_status()
        data = response.json()
        ad_logs_count = data['ad_logs_count']
        ad_logs_count_limit = data['ad_logs_count_limit']
        if response.status_code == 200:
            print(Fore.YELLOW + Style.BRIGHT + f"claim ad success")
            return ad_logs_count, ad_logs_count_limit
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            print(Fore.BLUE + Style.BRIGHT + "You can't claim ad")
            return ad_logs_count, ad_logs_count_limit
    except (KeyError, ValueError) as e:
        print(f"Invalid JSON response: {e}")
        return ad_logs_count, ad_logs_count_limit


def claim_mining(ini_token):  # 領取礦石
    url = 'https://lunar-api.roke.to/dock/idle-mining/'
    response = requests.post(url, headers=get_headers(ini_token))
    try:
        response.raise_for_status()
        if response.status_code == 200:
            print(Fore.YELLOW + Style.BRIGHT + f"claim mining success")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            print(Fore.BLUE + Style.BRIGHT + "You can't press claim_mining")
    except (KeyError, ValueError) as e:
        print(f"Invalid JSON response: {e}")


def claim_last_yield(ini_token):  # 領取存款礦石
    url = 'https://lunar-api.roke.to/dock/yield-claim/'
    response = requests.post(url, headers=get_headers(ini_token))
    try:
        response.raise_for_status()
        if response.status_code == 200:
            print(Fore.YELLOW + Style.BRIGHT + f"claim last yield success")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            print(Fore.BLUE + Style.BRIGHT + "You can't press last_yield")
    except (KeyError, ValueError) as e:
        print(f"Invalid JSON response: {e}")


def auto_upgrade_yield_percentage(ini_token):  # 自動升級礦石產量
    url = 'https://lunar-api.roke.to/dock/upgrades/yield_percentage/'
    response = requests.post(url, headers=get_headers(ini_token))
    data = response.json()
    try:
        response.raise_for_status()
        if response.status_code == 200:
            # Define the variable
            lunar_loot_speed_lvl = data['lunar_loot_speed_lvl']
            print(Fore.GREEN + Style.BRIGHT +
                  f"Yield_Upgrade_Level: {lunar_loot_speed_lvl}")  # Use the variable
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            print(Fore.BLUE + Style.BRIGHT +
                  "Not enough money to upgrade yield_percentage")
    except (KeyError, ValueError) as e:
        print(f"Invalid JSON response: {e}")


def auto_upgrade_lunar_loot_speed(ini_token):  # 自動升級礦石速度
    url = 'https://lunar-api.roke.to/dock/upgrades/lunar_loot_speed/'
    response = requests.post(url, headers=get_headers(ini_token))
    data = response.json()
    try:
        response.raise_for_status()
        if response.status_code == 200:
            lunar_loot_speed_lvl = data['lunar_loot_speed_lvl']
            print(Fore.GREEN + Style.BRIGHT +
                  f"Lunar_Loot_Speed_Upgrade_Level: {lunar_loot_speed_lvl}")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            print(Fore.BLUE + Style.BRIGHT +
                  "Not enough money to upgrade loot_speed")
    except (KeyError, ValueError) as e:
        print(f"Invalid JSON response: {e}")


def auto_upgrade_dock_size(ini_token):  # 自動升級倉庫大小
    url = 'https://lunar-api.roke.to/dock/upgrades/dock_size/'
    response = requests.post(url, headers=get_headers(ini_token))
    data = response.json()
    try:
        response.raise_for_status()
        if response.status_code == 200:
            dock_size_lvl = data['dock_size_lvl']
            print(Fore.GREEN + Style.BRIGHT +
                  f"Dock_Size_Upgrade_Level: {dock_size_lvl}")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            print(Fore.BLUE + Style.BRIGHT +
                  "Not enough money to upgrade dock_size")
    except (KeyError, ValueError) as e:
        print(f"Invalid JSON response: {e}")


def read_tokens():  # 讀取密鑰
    with open('initdata.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]


def read_query_ids():  # 讀取query_id
    with open('query_id.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]


def write_tokens(tokens):  # 寫入密鑰
    with open('initdata.txt', 'w') as file:
        for token in tokens:
            file.write(f"{token}\n")


def animate_energy_recharge(duration):  # 休息動畫
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(
                f"\r recharge energy {frame} - remaining time {remaining_time} second", end="", flush=True)
            time.sleep(0.25)
    print("\r Break time.", flush=True)


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
        # last_claimed_time = 0
        for index, token in enumerate(tokens):
            if nickname(token) == False:
                print(
                    f"{Fore.RED + Style.BRIGHT}Invalid Token, Please Check Your Token")
                query_ids = read_query_ids()
                tokens = []
                for query_id in query_ids:
                    token = get_token(query_id)
                    if token:
                        tokens.append(token)
                write_tokens(tokens)
                continue
            print(
                f"{Fore.BLUE + Style.BRIGHT}\n========[{Fore.WHITE + Style.BRIGHT} Akun {index + 1} |  {nickname(token)} {Fore.BLUE + Style.BRIGHT}]========")
            current_last_claimed_time, lunar_loot_speed_lvl, dock_size_lvl, yield_percentage_lvl = dock_balance(
                token)

            claim_mining(token)
            claim_last_yield(token)
            # current_last_claimed_time = int(datetime.datetime.fromtimestamp(
            #     current_last_claimed_time).timestamp()) + 7500
            # print(current_last_claimed_time)

            ad_logs_count, ad_logs_count_limit = claim_ad(token)

            while ad_logs_count < ad_logs_count_limit:
                ad_logs_count, ad_logs_count_limit = claim_ad(token)
                time.sleep(1)
                if ad_logs_count == ad_logs_count_limit:
                    break

            if user_lunar_loot_speed_upgrades == 'y' and lunar_loot_speed_lvl < max_lunar_loot_speed:
                auto_upgrade_lunar_loot_speed(token)
            elif user_dock_size_upgrades == 'y' and dock_size_lvl < max_dock_size:
                auto_upgrade_dock_size(token)
            elif user_yield_percentage_upgrades == 'y' and yield_percentage_lvl < max_yield_percentage:
                auto_upgrade_yield_percentage(token)

            print(
                f"{Fore.BLUE + Style.BRIGHT}===========================================")
        animate_energy_recharge(1000)


if __name__ == "__main__":
    main()
