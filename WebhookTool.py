import requests
from colorama import init, Fore, Style
import time
import json
import os

init(autoreset=True)

ASCII_ART = f"""{Fore.RED}

                                                                                    ,----,                            
                                                                                  ,/   .`|                            
           .---.                      ,---,                              ,-.    ,`   .'  :                    ,--,    
          /. ./|            ,---,   ,--.' |                          ,--/ /|  ;    ;     /                  ,--.'|    
      .--'.  ' ;          ,---.'|   |  |  :       ,---.     ,---.  ,--. :/ |.'___,/    ,'  ,---.     ,---.  |  | :    
     /__./ \ : |          |   | :   :  :  :      '   ,'\   '   ,'\ :  : ' / |    :     |  '   ,'\   '   ,'\ :  : '    
 .--'.  '   \' .   ,---.  :   : :   :  |  |,--. /   /   | /   /   ||  '  /  ;    |.';  ; /   /   | /   /   ||  ' |    
/___/ \ |    ' '  /     \ :     |,-.|  :  '   |.   ; ,. :.   ; ,. :'  |  :  `----'  |  |.   ; ,. :.   ; ,. :'  | |    
;   \  \;      : /    /  ||   : '  ||  |   /' :'   | |: :'   | |: :|  |   \     '   :  ;'   | |: :'   | |: :|  | :    
 \   ;  `      |.    ' / ||   |  / :'  :  | | |'   | .; :'   | .; :'  : |. \    |   |  ''   | .; :'   | .; :'  : |__  
  .   \    .\  ;'   ;   /|'   : |: ||  |  ' | :|   :    ||   :    ||  | ' \ \   '   :  ||   :    ||   :    ||  | '.'| 
   \   \   ' \ |'   |  / ||   | '/ :|  :  :_:,' \   \  /  \   \  / '  : |--'    ;   |.'  \   \  /  \   \  / ;  :    ; 
    :   '  |--" |   :    ||   :    ||  | ,'      `----'    `----'  ;  |,'       '---'     `----'    `----'  |  ,   /  
     \   \ ;     \   \  / /    \  / `--''                          '--'                                      ---`-'   
      '---"       `----'  `-'----'                                                                                    
                                                                                                                      

                                                                    
"""

print(ASCII_ART + Fore.BLUE + "                    >>> Webhook Tool <<<\n")

# --- Helpers ---

def save_webhooks(webhooks):
    with open("webhooks.json", "w") as f:
        json.dump(webhooks, f, indent=4)

def load_webhooks():
    if not os.path.exists("webhooks.json"):
        return {}
    with open("webhooks.json", "r") as f:
        return json.load(f)

def print_header(title):
    print(Fore.MAGENTA + f"\n--- {title} ---\n" + Fore.RESET)

def get_color_from_hex(hex_color):
    try:
        return int(hex_color.lstrip("#"), 16)
    except:
        print(Fore.RED + "Invalid color code! Using default white (0xFFFFFF).")
        return 0xFFFFFF

def send_webhook(url, payload, files=None):
    try:
        response = requests.post(url, json=payload, files=files)
        if response.status_code == 204:
            print(Fore.GREEN + "Message sent successfully.")
        else:
            print(Fore.RED + f"Failed to send message! Status: {response.status_code} | {response.text}")
    except Exception as e:
        print(Fore.RED + f"Error sending webhook: {e}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Main ---

def main():
    clear_screen()
    print(ASCII_ART)
    webhooks = load_webhooks()

    print(Fore.YELLOW + "Your saved webhooks:")
    if not webhooks:
        print(Fore.RED + "No saved webhooks found.")
    else:
        for i, (name, url) in enumerate(webhooks.items(), 1):
            print(f"{i}. {name} : {url[:50]}{'...' if len(url) > 50 else ''}")

    print("\nOptions:")
    print("1. Use saved webhook")
    print("2. Add new webhook")
    print("3. Delete a saved webhook")
    print("4. Continue without saving")

    choice = input(Fore.CYAN + "Choose option (1-4): ").strip()

    webhook_url = None
    if choice == "1":
        if not webhooks:
            print(Fore.RED + "No webhooks saved. Please add a new one.")
            return
        idx = int(input("Enter webhook number: ")) - 1
        if idx < 0 or idx >= len(webhooks):
            print(Fore.RED + "Invalid selection.")
            return
        webhook_url = list(webhooks.values())[idx]

    elif choice == "2":
        name = input("Give this webhook a name (for saving): ").strip()
        url = input("Enter Discord Webhook URL: ").strip()
        if not url.startswith("https://discord.com/api/webhooks/"):
            print(Fore.RED + "Invalid webhook URL format.")
            return
        webhooks[name] = url
        save_webhooks(webhooks)
        webhook_url = url
        print(Fore.GREEN + f"Webhook '{name}' saved successfully.")

    elif choice == "3":
        if not webhooks:
            print(Fore.RED + "No webhooks saved.")
            return
        idx = int(input("Enter webhook number to delete: ")) - 1
        if idx < 0 or idx >= len(webhooks):
            print(Fore.RED + "Invalid selection.")
            return
        key_to_delete = list(webhooks.keys())[idx]
        del webhooks[key_to_delete]
        save_webhooks(webhooks)
        print(Fore.GREEN + f"Webhook '{key_to_delete}' deleted successfully.")
        return

    elif choice == "4":
        webhook_url = input("Enter Discord Webhook URL (no saving): ").strip()
        if not webhook_url.startswith("https://discord.com/api/webhooks/"):
            print(Fore.RED + "Invalid webhook URL format.")
            return
    else:
        print(Fore.RED + "Invalid choice.")
        return

    # Choose message type
    use_embed = input(Fore.CYAN + "Send an embed message? (y/n): ").strip().lower() == "y"

    payload = {}

    if use_embed:
        print_header("Embed Builder")
        title = input("Embed title: ").strip()
        description = input("Embed description: ").strip()
        color_hex = input("Embed color (hex, e.g. FF0000): ").strip()
        color = get_color_from_hex(color_hex)

        author_name = input("Author name (optional): ").strip()
        author_icon = input("Author icon URL (optional): ").strip()
        thumbnail_url = input("Thumbnail URL (optional): ").strip()
        footer_text = input("Footer text (optional): ").strip()
        footer_icon = input("Footer icon URL (optional): ").strip()

        embed = {
            "title": title,
            "description": description,
            "color": color,
        }

        if author_name:
            embed["author"] = {"name": author_name}
            if author_icon:
                embed["author"]["icon_url"] = author_icon

        if thumbnail_url:
            embed["thumbnail"] = {"url": thumbnail_url}

        if footer_text:
            embed["footer"] = {"text": footer_text}
            if footer_icon:
                embed["footer"]["icon_url"] = footer_icon

        payload["embeds"] = [embed]

    else:
        content = input("Enter message content: ").strip()
        payload["content"] = content

    # File upload support
    attach_file = input("Attach a file? (y/n): ").strip().lower() == "y"
    files = None
    if attach_file:
        file_path = input("Enter full path to file: ").strip()
        if not os.path.isfile(file_path):
            print(Fore.RED + "File not found.")
            return
        files = {
            "file": open(file_path, "rb")
        }

    # Spam mode
    spam_mode = input("Enable spam mode? (y/n): ").strip().lower() == "y"
    if spam_mode:
        try:
            count = int(input("How many messages to send?: "))
            delay = float(input("Delay between messages (seconds, can be 0): "))
        except ValueError:
            print(Fore.RED + "Invalid input for count or delay.")
            return

        print(Fore.YELLOW + f"Starting spam: sending {count} messages with {delay}s delay.")

        for i in range(count):
            try:
                if files:
                    files["file"].seek(0)  # reset file pointer for each upload
                response = requests.post(webhook_url, json=payload, files=files)
                if response.status_code == 204:
                    print(Fore.GREEN + f"[{i+1}/{count}] Message sent successfully.")
                else:
                    print(Fore.RED + f"[{i+1}/{count}] Failed! Status: {response.status_code} | {response.text}")
            except Exception as e:
                print(Fore.RED + f"[{i+1}/{count}] Exception: {e}")

            if i != count - 1:
                time.sleep(delay)

        if files:
            files["file"].close()
    else:
        send_webhook(webhook_url, payload, files)
        if files:
            files["file"].close()


if __name__ == "__main__":
    main()