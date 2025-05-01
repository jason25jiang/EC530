import requests
import time

SERVER = "http://localhost:8000"
USERNAME = input("Enter your username: ")

requests.post(f"{SERVER}/subscribe", json={"username": USERNAME})

while True:
    action = input("[S]end, [R]eceive, [Q]uit: ").lower()

    if action == "s":
        recipient = input("Send to: ")
        message = input("Message: ")
        resp = requests.post(f"{SERVER}/send", json={
            "sender": USERNAME,
            "recipient": recipient,
            "message": message
        })
        print(resp.json())

    elif action == "r":
        resp = requests.get(f"{SERVER}/messages/{USERNAME}")
        msgs = resp.json()
        if msgs:
            for m in msgs:
                print(f"[{m['time']}] {m['from']}: {m['message']}")
        else:
            print("No new messages.")

    elif action == "q":
        print("Goodbye!")
        break

# def send_message():
#     msg = input("> ")
#     requests.post(f"{SERVER}/send", json={"user": USERNAME, "message": msg})

# def fetch_messages():
#     resp = requests.get(f"{SERVER}/messages")
#     for m in resp.json():
#         print(f"[{m['timestamp']}] {m['user']}: {m['message']}")

# if __name__ == "__main__":
#     print("Click Enter to send message. Ctrl+C to exit.")
#     try:
#         while True:
#             send_message()
#             fetch_messages()
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("\nGoodbye!")
