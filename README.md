# GFX Bot - Esports Graphics Generator

A Discord bot that creates professional esports graphics, banners, and posters on-demand using customizable text overlays.

## Features

- ✨ **Welcome Posters** - Create player welcome graphics
- 📢 **Announcement Posters** - Announce new players or team updates
- 💼 **Recruitment Posters** - Post recruitment graphics for your team
- 🎨 **Custom Designs** - Create custom graphics from any text prompt

## Commands

### `/welcome`
Create a professional welcome poster for a player.
```
/welcome player_name: Joshua team_name: Blaze Esports color: red
```

### `/announcement`
Create a player announcement poster.
```
/announcement player_name: MASE title: PLAYER ANNOUNCEMENT team_name: Blaze Esports
```

### `/recruit`
Create a recruitment poster.
```
/recruit game: Fortnite role: Pro Player team_name: Blaze Esports
```

### `/design`
Create a custom graphic from a text description.
```
/design prompt: Twitter banner for Blaze Esports with player Spookz
```

### `/help_gfx`
Show all available commands.

## Setup Instructions

### Step 1: Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application**
3. Name it (e.g., "GFX Bot")
4. Go to the **Bot** section
5. Click **Add Bot**
6. Copy the **Token** (keep it secret!)

### Step 2: Get OAuth2 URL

1. In Developer Portal, go to **OAuth2** → **URL Generator**
2. Select scopes:
   - `bot`
   - `applications.commands`
3. Select permissions:
   - Send Messages
   - Attach Files
   - Use Slash Commands
4. Copy the generated URL and open it in your browser to invite the bot to your server

### Step 3: Set Up the Bot Locally

1. Clone or download this project
2. Create a `.env` file in the project root:
   ```
   TOKEN=your_discord_bot_token_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 4: Run the Bot

```bash
python main.py
```

You should see: `YourBotName has connected to Discord!`

## Project Structure

```
bot.py/
├── main.py              # Main bot code
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── .env.example         # Example .env file
├── templates/           # Custom template images (add your own)
├── fonts/               # Custom fonts (optional)
└── renders/             # Output folder (auto-created)
```

## Customization

### Add Custom Templates

1. Create your esports templates in Canva or Photoshop
2. Export as PNG
3. Add to the `templates/` folder
4. Modify the bot code to use your templates

### Add Custom Fonts

1. Add .ttf font files to the `fonts/` folder
2. Modify the `add_text_to_image()` function to use them

### Customize Colors & Styling

Edit the `create_default_template()` function to change:
- Background colors (currently dark red gradient)
- Default font sizes
- Text positioning

## Requirements

- Python 3.8+
- discord.py 2.4.0+
- Pillow (PIL) for image manipulation
- python-dotenv for environment variables

## Hosting (Optional)

To keep the bot online 24/7, deploy to:
- **Railway** (recommended for Discord bots)
- **Heroku** (free tier ended, but check for alternatives)
- **Render**
- **Replit** with Always On (paid)

### Deploy to Railway

1. Push your code to GitHub
2. Connect your GitHub repo to Railway
3. Add `TOKEN` as an environment variable
4. Deploy!

## Support

For issues or questions, check the Discord bot documentation:
- [discord.py Documentation](https://discordpy.readthedocs.io/)
- [Pillow Documentation](https://pillow.readthedocs.io/)

## License

This project is open source and available for personal and commercial use.

---

Made with 🔴 for esports creators
