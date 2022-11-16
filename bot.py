import requests
import random
import time
import os

TOKEN_PATH = "./token.txt"
TOKEN = None

def get_token():
    if not os.path.exists(TOKEN_PATH):
        while True:
            token = input("Token: ").strip()

            try:
                token_valid = validate_token(token)
            except Exception:
                print("Error: Unable to validate token. Try again.")
                continue

            if not token_valid:
                print("Error: Invalid token. Try again.")
                continue

            break

        with open(TOKEN_PATH, "w") as file:
            file.write(token)
            file.close()

        return token
    
    with open(TOKEN_PATH, "r") as file:
        token = file.read().strip()
        file.close()
    
    try:
        token_valid = validate_token(token)
    except Exception:
        print("Error: Unable to validate saved token. Retrying...")
        return get_token()
    

    if not token_valid:
        print("Error: Saved token is invalid. Please set a new token.")
        os.remove(TOKEN_PATH)
        return get_token()

    return token

def validate_token(token):
    user = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}).json()

    if not "id" in user:
        return False
    
    return True

def validate_channel(channel_id):
    channel = requests.get(f"https://discord.com/api/v9/channels/{channel_id}", headers={"Authorization": TOKEN}).json()
    
    if not "id" in channel:
        return False
    
    return True

def send_message(channel_id, message):
    http = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers={"Authorization": TOKEN}, json={"content": message})

def get_textlist():
    if not os.path.exists("textlistpath.txt"):
        while True:
            path = input("Path: ").strip()
            if not os.path.exists(path):
                print("Error: Path does not exist.")
                continue
            break

        with open("textlistpath.txt", "w") as file:
            file.write(path)
            file.close()
        
    with open("textlistpath.txt", "r") as file:
        path = file.read().strip()
        file.close()
    
    print(f"Select text list file.\n")

    for file in os.listdir(path):
        file_path = f"{path}/{file}"
        if os.path.isfile(file_path):
            print(file)
    
    print()

    while True:
        while True:
            filename = input("Filename: ").strip()
            file_path = f"{path}/{filename}"
            if not os.path.isfile(file_path):
                print(f"Erorr: Invalid file. Try again.")
                continue
            break
        
        with open(file_path, "rb") as file:
            textlist = [i.decode() for i in file.read().strip().splitlines()]
            file.close()
        
        if len(textlist) <= 0:
            print("Error: Text List is empty. Try another file.")
            continue

        break
    
    return textlist

def get_shuffle_mode():
    print("\nSelect shuffle mode.\n\n1 - Shuffle\n2 - No Shuffle\n")
    shuffle_modes = [1, 2]

    while True:
        try:
            shuffle_mode = int(input("Shuffle Mode: "))
            if not shuffle_mode in shuffle_modes:
                raise Exception
        except Exception:
            print("Error: Invalid shuffle mode.")
            continue
        break

    return shuffle_mode

def main():
    global TOKEN

    try:
        textlist = get_textlist()
    except KeyboardInterrupt:
        return

    try:
        shuffle_mode = get_shuffle_mode()
    except KeyboardInterrupt:
        return

    try:
        token = get_token()
    except KeyboardInterrupt:
        return

    TOKEN = token
        
    try:
        while True:
            channel_id = input("Channel ID: ").strip()

            try:
                channel_valid = validate_channel(channel_id)
            except Exception:
                print("Error: Unable to validate channel. Try again.")
                continue

            if not channel_valid:
                print("Error: Invalid channel ID. Try again.")
                continue

            break
    except KeyboardInterrupt:
        return
    
    try:
        while True:
            try:
                sleep_time = int(input("Sleep Time (Seconds): "))
            except Exception:
                print("Error: Invalid sleep time. Must be integer.")
                continue
            break
    except KeyboardInterrupt:
        return
    
    try:
        while True:
            if shuffle_mode == 1:
                random.shuffle(textlist)
            
            for text in textlist:
                try:
                    send_message(channel_id, text)
                except Exception:
                    print("Error: Unable to send message. Sleeping in 5 seconds...")
                    time.sleep(5)
                    continue
                print(f"Sent -> {text}")
                time.sleep(sleep_time)
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
