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

def main():
    global TOKEN

    if not os.path.exists("textlist.txt"):
        print("Error: textlist.txt file not found")
        return
    
    with open("textlist.txt", "rb") as file:
        textlist = [i.decode() for i in file.read().strip().splitlines()]
        file.close()

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
