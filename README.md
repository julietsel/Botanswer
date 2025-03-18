# 📸 Screenshot-to-GPT-Telegram Notifier

This project monitors your screenshots on macOS, sends them to OpenAI GPT-4o for analysis, and delivers the AI-generated answers directly to your Telegram app (and Apple Watch notifications if configured!).

---

## 🚀 Features

- Automatically detects new screenshots saved on your Desktop.
- Sends screenshots to OpenAI's GPT-4o model for analysis.
- Receives and forwards GPT answers to your Telegram bot.
- Easy to run on macOS with minimal configuration.

---

## 🛠️ Setup Guide

### 1. **Requirements**

- Python 3.12+
- macOS
- Telegram app (iPhone/Apple Watch recommended)
- OpenAI API access (GPT-4o model)

---

## 🔑 How to get your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/).
2. Sign in to your account.
3. Navigate to **API Keys** in your account menu.
4. Click **Create new secret key**.
5. Copy and paste the key into the script:

```python
client = OpenAI(api_key="sk-...")
```

> ⚠️ **Do not share your API key.**


---

## 🤖 How to Create Your Telegram Bot

### Step 1: Create the Bot

1. Open Telegram and search for **@BotFather**.
2. Start a conversation and send `/newbot`.
3. Follow the prompts to:
   - Give your bot a name (e.g., `ScreenshotAnswerBot`)
   - Assign a username (must end in `bot`, e.g., `screenshot_answer_bot`)
4. Once created, BotFather will provide you a **Bot Token**:

```
Example token:
8014853991:AAF...dfc
```

Paste this token into the script here:

```python
BOT_TOKEN = 'your_bot_token_here'
```


### Step 2: Get Your Chat ID

1. Start a chat with your bot in Telegram.
2. Send any message (e.g., `/start`).
3. Visit this URL in your browser (replace YOUR_BOT_TOKEN):

```
https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
```

4. Find your **chat ID** in the JSON response. It will look like this:

```
"chat":{"id":XXXXXXXXXX,...}
```

5. Paste the chat ID into the script:

```python
CHAT_ID = 'your_chat_id_here'
```

---

## ⚙️ Configuration

Make sure you configure these variables in your Python script:

```python
client = OpenAI(api_key="your_openai_api_key")
BOT_TOKEN = 'your_telegram_bot_token'
CHAT_ID = 'your_chat_id'
```

The default screenshot folder is:

```python
CAPTURE_FOLDER = os.path.expanduser("~/Desktop/capture")
```

You can change it if necessary!

---

## ▶️ Running the Script

### Manual launch:
```bash
python3 Scriptquiz.py
```

### Recommended: Start/Stop shortcuts (via Karabiner-Elements)
- Start the script with `CTRL + SHIFT + F`
- Stop the script with `CTRL + SHIFT + D`

More info on Karabiner setup can be found [here](https://karabiner-elements.pqrs.org/).

---

## 📦 Dependencies

Install these Python libraries:

```bash
pip install openai requests watchdog
```

---

## 🛑 Notes

- This script is **for educational purposes only**.
- Do **not** share or publish your OpenAI keys.
- Always comply with OpenAI and Telegram's terms of use.



