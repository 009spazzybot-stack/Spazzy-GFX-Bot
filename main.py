import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import aiohttp
import os
from urllib.parse import quote
from dotenv import load_dotenv
from io import BytesIO
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Get token from environment
DISCORD_TOKEN = os.getenv("TOKEN")
BING_API_KEY = os.getenv("BING_API_KEY")

# Folder structure
TEMPLATES_DIR = "templates"
FONTS_DIR = "fonts"
SKINS_DIR = "skins"
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(FONTS_DIR, exist_ok=True)
os.makedirs(SKINS_DIR, exist_ok=True)


@bot.event
async def on_ready():
    logger.info(f"{bot.user} has connected to Discord!")
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")


def get_font(font_name="Anton-Regular.ttf", font_size=40):
    """Load a font from fonts folder or fallback to system font."""
    font_path = os.path.join(FONTS_DIR, font_name)
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, font_size)
        except Exception:
            pass
    try:
        return ImageFont.truetype(font_name, font_size)
    except Exception:
        return ImageFont.load_default()


def draw_centered_text(img, text, position, font, fill=(255, 255, 255), stroke_width=0, stroke_fill=None):
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x, y = position
    x -= text_width // 2
    y -= text_height // 2
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)
    return img


def create_base_background(width, height, accent=(220, 20, 20)):
    img = Image.new("RGB", (width, height), (15, 8, 15))
    draw = ImageDraw.Draw(img)

    # diagonal gradient
    for i in range(width):
        alpha = int(255 * (i / width))
        r = min(15 + int(accent[0] * (i / width) * 0.75), 255)
        g = min(8 + int(accent[1] * (i / width) * 0.3), 255)
        b = min(15 + int(accent[2] * (i / width) * 0.3), 255)
        draw.line([(i, 0), (i, height)], fill=(r, g, b), width=1)

    # subtle glow bars
    for y in range(0, height, 120):
        draw.rectangle([0, y, width, y + 10], fill=(40, 0, 0))

    # vignette
    vignette = Image.new("L", (width, height), 0)
    vign_draw = ImageDraw.Draw(vignette)
    vign_draw.ellipse([-(width * 0.2), -(height * 0.2), width * 1.2, height * 1.2], fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(200))
    img.putalpha(255)
    img = Image.composite(img, Image.new("RGBA", img.size, (0, 0, 0, 255)), vignette)
    return img.convert("RGB")


def load_image(path, size=None):
    if not os.path.exists(path):
        return None
    img = Image.open(path).convert("RGBA")
    if size:
        img = img.resize(size, Image.LANCZOS)
    return img


async def download_skin_image(skin_name):
    clean_name = skin_name.strip().lower().replace(" ", "_")
    skin_path = os.path.join(SKINS_DIR, f"{clean_name}.png")
    if os.path.exists(skin_path):
        return skin_path

    if not BING_API_KEY:
        return None

    query = quote(f"Fortnite {skin_name} skin render transparent background")
    url = f"https://api.bing.microsoft.com/v7.0/images/search?q={query}&count=1&safeSearch=Strict"

    headers = {
        "Ocp-Apim-Subscription-Key": BING_API_KEY
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                return None
            data = await response.json()
            if not data.get("value"):
                return None
            image_url = data["value"][0].get("thumbnailUrl") or data["value"][0].get("contentUrl")
            if not image_url:
                return None

        async with session.get(image_url) as img_resp:
            if img_resp.status != 200:
                return None
            raw = await img_resp.read()
            try:
                with Image.open(BytesIO(raw)).convert("RGBA") as downloaded:
                    downloaded.save(skin_path, format="PNG")
                return skin_path
            except Exception:
                return None


def load_skin_image(skin_name, target_size):
    clean_name = skin_name.strip().lower().replace(" ", "_")
    skin_path = os.path.join(SKINS_DIR, f"{clean_name}.png")
    if not os.path.exists(skin_path):
        skin_path = os.path.join(SKINS_DIR, "default.png")
    return load_image(skin_path, size=target_size)


def paste_skin(img, skin_img, target_box):
    if not skin_img:
        return img
    skin = skin_img.copy().convert("RGBA")
    skin = skin.resize((target_box[2] - target_box[0], target_box[3] - target_box[1]), Image.LANCZOS)
    img.paste(skin, target_box, skin)
    return img


def create_template_image(template_name, size, accent=(220, 20, 20)):
    template_path = os.path.join(TEMPLATES_DIR, f"{template_name}.png")
    if os.path.exists(template_path):
        return load_image(template_path, size=size)
    return create_base_background(size[0], size[1], accent=accent)


@bot.tree.command(name="welcome", description="Create a welcome poster for a player")
async def welcome(
    interaction: discord.Interaction,
    player_name: str,
    skin_name: str = "default",
    team_name: str = "Blaze Esports",
    color: str = "red"
):
    await interaction.response.defer()
    try:
        width, height = 1920, 1080
        img = create_template_image("welcome", (width, height), accent=(255, 50, 50))

        # Skin art area
        skin_path = await download_skin_image(skin_name)
        skin_img = load_image(skin_path, size=(760, 920)) if skin_path else None
        if skin_img:
            img = paste_skin(img, skin_img, (1120, 80, 1880, 1000))

        # Add top branding
        font_header = get_font("Anton-Regular.ttf", 64)
        img = draw_centered_text(img, team_name.upper(), (520, 120), font_header, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))

        # Main hero text
        font_large = get_font("Anton-Regular.ttf", 200)
        img = draw_centered_text(img, "WELCOME", (520, 360), font_large, fill=(255, 90, 90), stroke_width=3, stroke_fill=(20, 0, 0))
        img = draw_centered_text(img, player_name.upper(), (520, 560), font_large, fill=(245, 245, 245), stroke_width=2, stroke_fill=(10, 10, 10))

        # Subtitle
        font_small = get_font("Anton-Regular.ttf", 42)
        img = draw_centered_text(img, f"Fortnite Pro Player", (520, 680), font_small, fill=(210, 210, 210))
        img = draw_centered_text(img, f"Skin: {skin_name.title()}", (520, 760), font_small, fill=(255, 180, 50))

        # Footer
        footer_box = Image.new("RGBA", (width, 120), (10, 10, 10, 190))
        img.paste(footer_box, (0, height - 120), footer_box)
        draw = ImageDraw.Draw(img)
        draw.text((40, height - 90), f"{team_name}  •  @BLZESP", font=get_font("Arial.ttf", 32), fill=(255, 255, 255))

        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        embed = discord.Embed(
            title="🎉 Welcome Poster",
            description=f"Welcome {player_name} to {team_name}! Skin: {skin_name.title()}",
            color=discord.Color.red()
        )
        await interaction.followup.send(
            embed=embed,
            file=discord.File(img_bytes, filename="welcome_poster.png")
        )
    except Exception as e:
        logger.error(f"Error in welcome command: {e}")
        await interaction.followup.send(f"❌ An error occurred: {str(e)}")


@bot.tree.command(name="announcement", description="Create a player announcement poster")
async def announcement(
    interaction: discord.Interaction,
    player_name: str,
    skin_name: str = "default",
    title: str = "PLAYER ANNOUNCEMENT",
    team_name: str = "Blaze Esports"
):
    await interaction.response.defer()
    try:
        width, height = 1200, 630
        img = create_template_image("announcement", (width, height), accent=(255, 70, 70))

        skin_path = await download_skin_image(skin_name)
        skin_img = load_image(skin_path, size=(440, 560)) if skin_path else None
        if skin_img:
            img = paste_skin(img, skin_img, (720, 40, 1160, 600))

        font_title = get_font("Anton-Regular.ttf", 56)
        img = draw_centered_text(img, title.upper(), (320, 120), font_title, fill=(255, 90, 90), stroke_width=2, stroke_fill=(10, 0, 0))

        font_player = get_font("Anton-Regular.ttf", 96)
        img = draw_centered_text(img, player_name.upper(), (320, 320), font_player, fill=(245, 245, 245), stroke_width=2, stroke_fill=(5, 5, 5))

        font_meta = get_font("Anton-Regular.ttf", 36)
        img = draw_centered_text(img, team_name.upper(), (320, 500), font_meta, fill=(220, 220, 220))
        img = draw_centered_text(img, f"Skin: {skin_name.title()}", (320, 560), font_meta, fill=(255, 165, 60))

        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        embed = discord.Embed(
            title="📢 Announcement Poster",
            description=f"{title}: {player_name} (Skin: {skin_name.title()})",
            color=discord.Color.red()
        )
        await interaction.followup.send(
            embed=embed,
            file=discord.File(img_bytes, filename="announcement_poster.png")
        )
    except Exception as e:
        logger.error(f"Error in announcement command: {e}")
        await interaction.followup.send(f"❌ An error occurred: {str(e)}")


@bot.tree.command(name="recruit", description="Create a recruitment poster")
async def recruit(
    interaction: discord.Interaction,
    game: str = "Fortnite",
    role: str = "Player",
    team_name: str = "Blaze Esports",
    skin_name: str = "default"
):
    await interaction.response.defer()
    try:
        width, height = 1200, 630
        img = create_template_image("recruitment", (width, height), accent=(220, 180, 30))

        skin_path = await download_skin_image(skin_name)
        skin_img = load_image(skin_path, size=(420, 560)) if skin_path else None
        if skin_img:
            img = paste_skin(img, skin_img, (720, 40, 1140, 600))

        font_title = get_font("Anton-Regular.ttf", 58)
        img = draw_centered_text(img, "RECRUITING", (320, 120), font_title, fill=(255, 50, 50), stroke_width=2, stroke_fill=(10, 0, 0))

        font_role = get_font("Anton-Regular.ttf", 90)
        img = draw_centered_text(img, role.upper(), (320, 270), font_role, fill=(245, 245, 245))

        font_game = get_font("Anton-Regular.ttf", 42)
        img = draw_centered_text(img, f"{game} Players", (320, 370), font_game, fill=(220, 220, 220))
        img = draw_centered_text(img, f"Join {team_name}", (320, 450), font_game, fill=(255, 200, 60))
        img = draw_centered_text(img, f"Skin: {skin_name.title()}", (320, 520), font_game, fill=(255, 180, 40))

        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        embed = discord.Embed(
            title="💼 Recruitment Poster",
            description=f"{team_name} is recruiting {role}s for {game}! Skin: {skin_name.title()}",
            color=discord.Color.gold()
        )
        await interaction.followup.send(
            embed=embed,
            file=discord.File(img_bytes, filename="recruitment_poster.png")
        )
    except Exception as e:
        logger.error(f"Error in recruit command: {e}")
        await interaction.followup.send(f"❌ An error occurred: {str(e)}")


@bot.tree.command(name="design", description="Create a custom graphic design")
async def design(
    interaction: discord.Interaction,
    prompt: str,
    skin_name: str = "default",
    width: int = 1200,
    height: int = 630
):
    await interaction.response.defer()
    try:
        img = create_template_image("custom", (width, height), accent=(180, 40, 40))

        skin_path = await download_skin_image(skin_name)
        skin_img = load_image(skin_path, size=(int(width * 0.35), int(height * 0.8))) if skin_path else None
        if skin_img:
            img = paste_skin(img, skin_img, (width - int(width * 0.38), int(height * 0.08), width - 40, int(height * 0.88)))

        font_prompt = get_font("Anton-Regular.ttf", 56)
        img = draw_centered_text(img, prompt.upper(), (width // 2 - 80, height // 2), font_prompt, fill=(245, 245, 245), stroke_width=2, stroke_fill=(10, 10, 10))

        img = draw_centered_text(img, f"Skin: {skin_name.title()}", (width // 2 - 80, height - 80), get_font("Anton-Regular.ttf", 32), fill=(255, 180, 50))

        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        embed = discord.Embed(
            title="🎨 Custom Design",
            description=f"Design: {prompt} (Skin: {skin_name.title()})",
            color=discord.Color.red()
        )
        await interaction.followup.send(
            embed=embed,
            file=discord.File(img_bytes, filename="custom_design.png")
        )
    except Exception as e:
        logger.error(f"Error in design command: {e}")
        await interaction.followup.send(f"❌ An error occurred: {str(e)}")


@bot.tree.command(name="help_gfx", description="Show available commands")
async def help_gfx(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎨 GFX Bot Help",
        description="Create professional esports graphics instantly! Add a Fortnite skin name to each command.",
        color=discord.Color.red()
    )

    embed.add_field(
        name="/welcome",
        value="Create a welcome poster for a player\n`/welcome player_name: Joshua skin_name: spookz team_name: Blaze Esports`",
        inline=False
    )

    embed.add_field(
        name="/announcement",
        value="Create a player announcement poster\n`/announcement player_name: MASE skin_name: spookz title: PLAYER ANNOUNCEMENT`",
        inline=False
    )

    embed.add_field(
        name="/recruit",
        value="Create a recruitment poster\n`/recruit game: Fortnite role: Pro Player team_name: Blaze Esports skin_name: spookz`",
        inline=False
    )

    embed.add_field(
        name="/design",
        value="Create a custom design from text\n`/design prompt: Twitter banner for Blaze Esports skin_name: spookz`",
        inline=False
    )

    embed.add_field(
        name="Skin Images",
        value="Put Fortnite skin PNG files in the `skins/` folder. Name files like `default.png`, `spookz.png`, etc.",
        inline=False
    )

    embed.set_footer(text="Generated by GFX Bot | Powered by Pillow")
    await interaction.response.send_message(embed=embed)


# Run the bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
