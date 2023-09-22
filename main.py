import os
try:
    import json
    import requests
    from colorama import Fore, init
except:
    os.system("pip install colorama")
    os.system("pip install requests")

init(autoreset=True)

def main(settings):
    os.system('cls' if os.name == 'nt' else 'clear')
    cookie = settings["cookie"]
    mass_unfavor = settings["mass_unfavor"]
    whitelist = set(settings.get("whitelist", []))
    try:
        id = requests.get("https://users.roblox.com/v1/users/authenticated", cookies={".ROBLOSECURITY": cookie}).json()["id"]
    except Exception as e:
        print(Fore.RED + "Please provide a valid cookie in settings.json")
        os.system("pause")
        return

    response = requests.get(f'https://games.roblox.com/v2/users/{id}/favorite/games?limit=50&sortOrder=Asc')
    if response.status_code != 200:
        print(Fore.RED + f"Failed to fetch favourited games. {response.status_code}")
        os.system("pause")
        return

    games = response.json().get('data', [])
    print(Fore.GREEN + f"You currently have {len(games)} favorited games.\n")

    if mass_unfavor:
        input(Fore.LIGHTRED_EX + "!!! Warning: Mass unfavor is enabled. This will unfavorite all you're favorited games except the games you've added in the whitelist! Press Enter to continue.")
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.GREEN + f"You currently have {len(games)} favorited games.\n")

    unfavorited = 0
    for game in games:
        game_name = game['name']
        game_id = game['id']
        game_place = int(game['rootPlace']['id'])

        if game_place not in whitelist:
            unfavor = 'y' if mass_unfavor else input(Fore.LIGHTWHITE_EX + f"Do you want to unfavor game {game_name} (ID: {game_place})? (y/n): ").strip().lower()

            if unfavor == 'y':
                response = requests.post('https://accountsettings.roblox.com/v1/email', cookies={".ROBLOSECURITY": cookie})
                csrf = response.headers['x-csrf-token']

                response = requests.post(f'https://games.roblox.com/v1/games/{game_id}/favorites', cookies={".ROBLOSECURITY": cookie}, headers={"x-csrf-token": csrf}, json={"isFavorited": False})
                if response.status_code == 200:
                    print(Fore.GREEN + f"Unfavorited game: {game_name} (ID: {game_place})")
                    unfavorited += 1
                else:
                    print(Fore.RED + f"Failed to unfavor game: {game_name} (ID: {game_place}) {response.status_code}")
        else:
            print(Fore.YELLOW + f"Skipping game: {game_name} (ID: {game_place})")

    print(Fore.MAGENTA + f"Unfavorited {unfavorited} games.")
    os.system("pause")

if __name__ == "__main__":
    with open("settings.json", 'r') as file:
        settings = json.load(file)
    main(settings)
