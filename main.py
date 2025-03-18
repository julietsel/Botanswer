import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import base64
import requests
from openai import OpenAI

# ✅ Folder where screenshots will be saved
CAPTURE_FOLDER = os.path.expanduser("~/Desktop/capture")
os.makedirs(CAPTURE_FOLDER, exist_ok=True)

# ✅ OpenAI client setup (replace with your OpenAI API Key)
OPENAI_API_KEY = "your_openai_api_key_here"
client = OpenAI(api_key=OPENAI_API_KEY)

# ✅ Telegram bot configuration (replace with your bot token and chat ID)
BOT_TOKEN = 'your_telegram_bot_token_here'
CHAT_ID = 'your_telegram_chat_id_here'

# ✅ Update macOS screenshot location
subprocess.run(["defaults", "write", "com.apple.screencapture", "location", CAPTURE_FOLDER])
subprocess.run(["killall", "SystemUIServer"])
print(f"🖼️ Screenshots will be saved in {CAPTURE_FOLDER}")

# ✅ Send message to Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"📲 Telegram message sent: {text}")
        else:
            print(f"❌ Telegram error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception when sending Telegram message: {e}")

# ✅ Store processed files to avoid duplicates
processed_files = set()

# ✅ Wait until the file is fully written
def wait_for_file_complete(filepath, timeout=5):
    start_time = time.time()
    last_size = -1

    while time.time() - start_time < timeout:
        try:
            current_size = os.path.getsize(filepath)
        except FileNotFoundError:
            time.sleep(0.1)
            continue

        if current_size == last_size:
            return True
        last_size = current_size
        time.sleep(0.5)

    print(f"⚠️ Timeout waiting for file: {filepath}")
    return False

# ✅ Send screenshot to OpenAI GPT-4o
def send_screenshot_to_chatgpt(image_path):
    print(f"🚀 Sending {image_path} to OpenAI GPT...")

    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    image_data_uri = f"data:image/png;base64,{img_base64}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "You need to give the correct(s) answers to the question. Just give the number of the answer."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_data_uri
                            }
                        }
                    ]
                }
            ],
            max_tokens=50
        )

        answer = response.choices[0].message.content
        print(f"✅ OpenAI GPT Answer: {answer}")

        # ✅ Send the answer via Telegram
        send_telegram_message(f"Answer: {answer}")

    except Exception as e:
        print(f"❌ Error sending to OpenAI GPT: {e}")

# ✅ Monitor screenshot folder
class ScreenshotHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        filename = os.path.basename(event.src_path)

        if filename.startswith("."):
            print(f"⏭️ Ignored hidden file: {filename}")
            return

        if filename in processed_files:
            print(f"⏭️ Already processed: {filename}")
            return

        if filename.endswith((".png", ".jpg", ".jpeg")):
            print(f"🖼️ New screenshot detected: {filename}")

            if wait_for_file_complete(event.src_path):
                send_screenshot_to_chatgpt(event.src_path)
                processed_files.add(filename)
                print(f"✅ Marked as processed: {filename}")
            else:
                print(f"⚠️ Could not process: {filename}")

# ✅ Start observer
observer = Observer()
observer.schedule(ScreenshotHandler(), path=CAPTURE_FOLDER, recursive=False)
observer.start()

print("👀 Monitoring screenshots... Press Ctrl+C to quit.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
