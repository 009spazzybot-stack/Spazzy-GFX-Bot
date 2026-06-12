# GFX Bot Quick Reference

## File Structure
```
bot.py/
├── main.py              ← Main bot code (run this!)
├── utils.py             ← Helper functions for templates
├── config.json          ← Bot configuration
├── requirements.txt     ← Python dependencies
├── .env.example         ← Example environment file
├── .env                 ← Your bot token (create this)
├── README.md            ← Full documentation
├── SETUP.md             ← Detailed setup guide
├── QUICKSTART.md        ← This file
├── templates/           ← Add custom images here
├── fonts/               ← Add custom fonts here (.ttf)
└── renders/             ← Generated graphics (auto-created)
```

## Quick Start (5 Minutes)

### 1. Get Bot Token
- Go to [Discord Developer Portal](https://discord.com/developers/applications)
- Create New Application → Add Bot → Copy Token

### 2. Create .env File
```
TOKEN=your_token_here
```

### 3. Install & Run
```bash
pip install -r requirements.txt
python main.py
```

### 4. Invite Bot
- OAuth2 → URL Generator
- Select: `bot` + `applications.commands`
- Permissions: Send Messages, Attach Files, Use Slash Commands

### 5. Test
In Discord: `/help_gfx`

---

## Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/welcome` | Player welcome poster | `/welcome player_name: Joshua team_name: Blaze` |
| `/announcement` | Player announcement | `/announcement player_name: MASE title: NEW PLAYER` |
| `/recruit` | Recruitment poster | `/recruit game: Fortnite role: Pro` |
| `/design` | Custom graphic | `/design prompt: Twitter banner` |
| `/help_gfx` | Show all commands | `/help_gfx` |

---

## Customization

### Edit Default Colors
Open `main.py` and find `create_default_template()`:
```python
color = (100 + alpha // 5, 0, 0)  # Adjust RGB values
```

### Add Custom Fonts
1. Add `.ttf` file to `fonts/` folder
2. Edit `main.py` font loading:
```python
font = ImageFont.truetype("fonts/myfont.ttf", font_size)
```

### Add Templates
1. Create image in Canva/Photoshop (export as PNG)
2. Save to `templates/` folder
3. Use in bot:
```python
img = Image.open("templates/mybanner.png")
```

---

## Common Issues

**"Token not found"**
→ Create `.env` file with `TOKEN=your_token`

**"Bot not responding"**
→ Restart Discord, check bot is in server

**"Module not found: discord"**
→ Run: `pip install -r requirements.txt`

**"No such file or directory"**
→ Make sure terminal is in `bot.py` folder

---

## Deployment (Keep Running 24/7)

### Railway (Recommended)
1. Push code to GitHub
2. Connect to [Railway.app](https://railway.app)
3. Add `TOKEN` environment variable
4. Deploy!

### Glitch
1. Create project
2. Import GitHub repo
3. Add environment variables
4. Done!

---

## Next Steps

1. ✅ Get the bot running
2. ✅ Test basic commands
3. 📸 Add custom templates
4. 🚀 Deploy to hosting service
5. 🎨 Customize styling and fonts

---

## Resources

- [discord.py Docs](https://discordpy.readthedocs.io/)
- [Pillow Docs](https://pillow.readthedocs.io/)
- [Discord Developer Docs](https://discord.com/developers/docs)
- [Canva](https://canva.com) - Design templates

---

Good luck with your bot! 🚀🎨
