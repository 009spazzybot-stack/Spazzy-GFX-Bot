# GFX Bot Setup Guide

Complete step-by-step guide to get your Discord bot running.

## Prerequisites

- Discord account
- Windows/Mac/Linux computer
- Python 3.8+ (or just use Replit/GitHub Codespaces)

---

## Option 1: Local Setup (Windows/Mac/Linux)

### Step 1: Install Python

**Windows/Mac:**
- Download from [python.org](https://www.python.org/downloads/)
- Install and check "Add Python to PATH"

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Step 2: Get Your Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **+ New Application**
3. Name it: `GFX Bot`
4. Click to **Bot** tab
5. Click **Add Bot**
6. Under TOKEN, click **Copy**
7. **KEEP THIS SECRET!** Never share it

### Step 3: Invite Bot to Server

1. In Developer Portal, go to **OAuth2** → **URL Generator**
2. Check these scopes:
   - ☑️ `bot`
   - ☑️ `applications.commands`
3. Check these permissions:
   - ☑️ Send Messages
   - ☑️ Attach Files
   - ☑️ Use Slash Commands
4. Copy the generated URL
5. Paste in browser and select your server

### Step 4: Download Bot Code

1. Download or clone the project
2. Extract to a folder (e.g., `C:\Users\YourName\GFX Bot\bot.py`)

### Step 5: Create .env File

In the bot folder, create a file named `.env` and paste:

```
TOKEN=paste_your_token_here
```

(Replace with your actual token from Step 2)

### Step 6: Install Dependencies

Open terminal/PowerShell in the bot folder and run:

```bash
pip install -r requirements.txt
```

### Step 7: Run the Bot

```bash
python main.py
```

You should see:
```
YourBotName has connected to Discord!
Synced X command(s)
```

### Step 8: Test in Discord

In your Discord server, type:
```
/help_gfx
```

Bot should respond with available commands!

---

## Option 2: GitHub Codespaces (Browser-Based)

### Step 1-2: Same as above (get bot token)

### Step 3: Create GitHub Repo

1. Go to [GitHub](https://github.com)
2. Click **+** → **New repository**
3. Name: `esports-discord-bot`
4. Click **Create repository**

### Step 4: Open Codespaces

1. Click green **Code** button
2. Click **Codespaces**
3. Click **Create codespace on main**
4. Wait for VS Code to load in browser

### Step 5-8: Same as Local Setup

Just run the commands in the Codespaces terminal!

---

## Option 3: Replit (Easiest for Beginners)

### Step 1: Go to Replit

1. Visit [replit.com](https://replit.com)
2. Sign in or create account

### Step 2: Create New Repl

1. Click **+ Create**
2. Search for **Python**
3. Name it `GFX Bot`
4. Click **Create**

### Step 3: Add Files

1. Click **Create file**
2. Create: `main.py`
3. Copy code from main.py in this project
4. Create: `requirements.txt`
5. Copy: 
   ```
   discord.py==2.4.0
   pillow==10.1.0
   python-dotenv==1.0.0
   ```

### Step 4: Set Environment Variable

1. Click **Secrets** (lock icon)
2. Add secret:
   - **Key:** `TOKEN`
   - **Value:** (your bot token)

### Step 5: Run

Click **Run** button!

---

## First Commands to Try

Once the bot is running, try these in your Discord server:

```
/help_gfx
/welcome player_name: YourName team_name: Your Team
/announcement player_name: TestPlayer title: WELCOME
/recruit game: Fortnite role: Player
/design prompt: Test banner
```

---

## Troubleshooting

### "Token not found"
- Check `.env` file exists
- Make sure `TOKEN=` line is there
- Restart the bot

### "Bot not responding"
- Verify bot is invited to server
- Check permissions in OAuth2 URL Generator
- Restart Discord app

### "Missing module discord"
- Run: `pip install -r requirements.txt`
- Make sure pip uses Python 3

### "No such file or directory: main.py"
- Make sure terminal is in the bot folder
- Run: `cd "C:\path\to\bot.py"`

---

## Next Steps

1. **Customize templates** - Add images to `templates/` folder
2. **Add custom fonts** - Add .ttf files to `fonts/` folder
3. **Deploy 24/7** - Host on Railway, Render, or Glitch
4. **Add more commands** - Edit main.py to add new graphics types

---

## Getting Help

- Check [discord.py docs](https://discordpy.readthedocs.io/)
- Check [Pillow docs](https://pillow.readthedocs.io/)
- Check bot terminal for error messages

Good luck! 🚀
