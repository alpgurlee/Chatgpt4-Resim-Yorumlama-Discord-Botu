import discord
from discord.ext import commands
import openai
from discord.ext.commands import CommandInvokeError
from openai.error import RateLimitError
from google.cloud import vision

bot_prefix = "!"
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix=bot_prefix, intents=intents)  # Bot nesnesini yalnızca bir kez oluşturun

# Google Cloud Vision API anahtarını ayarlayın
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your_google_cloud_api_key_path.json"

TOKEN = ''  # Buraya botunuzun tokenini yazın
openai.api_key = ""  # Buraya OpenAI API anahtarınızı ekleyin

@bot.command()
async def resim_yorumla(ctx, resim_url):
    # Resmi metne çevir
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = resim_url

    response = client.label_detection(image=image)
    labels = response.label_annotations

    # Resmin içeriğini açıklayan metni oluştur
    description = "Bu resimde "
    for label in labels:
        description += label.description + ", "

    description += "görülüyor."
    
async def gpt4(ctx, *, prompt):
    prompt = "Türkçe asistan: " + prompt
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.8,
    )

    answer = response.choices[0].text.strip()
    await ctx.send(answer)

@bot.event
async def on_ready():
    print(f'{bot.user} adlı bot çalışmaya başladı.')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandInvokeError):
        original = error.original
        if isinstance(original, RateLimitError):
            await ctx.send("API kotası aşıldı, lütfen daha sonra tekrar deneyin.")
    else:
        # Diğer hatalar için başka işlemler yapabilirsiniz
        pass

bot.run(TOKEN)
