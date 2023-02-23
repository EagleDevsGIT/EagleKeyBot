import discord
from discord.ext import commands

intents = discord.Intents.all
client = commands.Bot(command_prefix="!", intents=intents())

redeemrole = 'Customer'

bot_status = "Support Online"

token = ''