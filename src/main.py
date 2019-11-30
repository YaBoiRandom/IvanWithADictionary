import requests
import json
import random
import discord
from discord.ext import commands

#Reading JSON Files
json_dirs = ["./settings/tokens.json", "./settings/settings.json"]
with open(json_dirs[0]) as f:
    tokens = json.load(f)

with open(json_dirs[1]) as f:
    settings = json.load(f)

#Some Variables/Keys
DISCORD_TOKEN = tokens["keys"]["DiscordAPI"]

TRANSLATE_API_KEY = tokens["keys"]["YandexAPI"]

translate_url = tokens["urls"]["YandexAPI"]

bot = commands.Bot(command_prefix = settings["bot"]["prefix"], description = settings["bot"]["desc"])

lang_codes = settings["Yandex"]["lang_codes"]

#Start up
bot.remove_command('help')
@bot.event
async def on_ready():
    print ("Bot logged in as " + bot.user.name)
    print ("ID: " + str(bot.user.id))
    print("Prefix: " + bot.command_prefix)
    print('------------------------------------')

#Translate Command
@bot.command()
async def translate(ctx, *, arg):
    rand_temp = False
    args_temp = arg.split()
    lang = args_temp[0].lower()

    if lang == "rand":
        rand_temp = True
        lang = lang_codes[random.randint(0, len(lang_codes) - 1)]

    if not(lang in lang_codes):
        await ctx.send("Invalid or missing language code. Please reference " + bot.command_prefix + "help translate for list of supported languages.")
        return

    args_temp.pop(0)
    text = ' '.join(args_temp)

    params = dict(key=TRANSLATE_API_KEY, text=text, lang=lang)

    res = requests.get(translate_url, params=params)

    if not(res):
        await ctx.send("Problem communicating with the API. (Error Code: " + str(res.status_code) + ")")
        return
    
    json = res.json()

    if rand_temp:
        translation = "Translation (" + lang + "): " + json['text'][0]
    else:
        translation = "Translation: " + json['text'][0]

    if len(translation) > 2000:
        await ctx.send("Sorry, but the translation exceedes the 2000 character limit. Try again with a shorter phrase.")
        return
    
    await ctx.send(translation)

#Help Command
@bot.command()
async def help(ctx, *, arg = 'nan'):
    args_temp = arg.split()
    helpcmd = args_temp[0].lower()

    if helpcmd == "help":
        embed = discord.Embed(title = "Help", description = "The help command.", color = 0xEEE657)
        embed.add_field(name = "Description", value = "A list of the possible commands and info on them.", inline = False)
        embed.add_field(name = "Usage", value = bot.command_prefix + "help <command (optional)>", inline = False)
        embed.add_field(name = "Example", value = bot.command_prefix + "help translate", inline = False)
    
    elif helpcmd == 'translate':
        embed = discord.Embed(title = "Translate", description = "The translate command.", color = 0xEEE657)
        embed.add_field(name = "Usage", value = bot.command_prefix + "translate <language code> <the phrase to translate>", inline = False)
        embed.add_field(name = "Example", value = bot.command_prefix + "translate es Hello! How are you?", inline = False)
        embed.add_field(name = "Supported Languages", value = "To find a list of languages supported by the Yandex API and their codes [click here](https://tech.yandex.com/translate/doc/dg/concepts/api-overview-docpage/).\nTo have it translate to a random language, use the code \"rand\".", inline = False)
    
    elif helpcmd == 'nan':
        embed = discord.Embed(title = "Commands", description = "The commands currently available (All of them must have the prefix of " + bot.command_prefix + ").\nFor more info on a command just type " + bot.command_prefix + "help <command name here>.", color = 0xEEE657)
        embed.add_field(name = "translate", value = "Translate any supported language into any other supported language.", inline = False)
        embed.add_field(name = "help", value = "This list of commands!", inline = False)
    
    else:
        embed = discord.Embed(title = "Invalid Command", description = "There is no command by the name " + helpcmd + ".", color = 0xEEE657)
    
    await ctx.send(embed=embed)

bot.run(DISCORD_TOKEN)