import discord
from discord.ext import commands
import sqlite3

from Config import token, client, bot_status, redeemrole

conn = sqlite3.connect('generatedKeys.db')

# Role Redeem
@client.command()
async def redeem_key(ctx, key):
    user_id = ctx.author.id
    c.execute("SELECT user_id FROM keys WHERE key=?", (key,))
    result = c.fetchone()
    if result and user_id == result[0]:
        role = discord.utils.get(ctx.guild.roles, name=redeemrole)
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention}, you have been given the '{role.name}' role.")
    else:
        await ctx.send(f"{ctx.author.mention}, the key you entered is invalid or doesn't belong to you.")

# Check for key registered to userid
@client.command()
async def get_key(ctx):
    user_id = ctx.author.id
    key = get_key_db(user_id)
    if key:
        user = await client.fetch_user(user_id)
        await user.send(f'Your key is: {key}')
        await ctx.send(f'{ctx.author.mention}, your key has been sent to your DMs.')
    else:
        await ctx.send(f'{ctx.author.mention}, no key found for your user ID.')

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS keys
             (user_id INTEGER PRIMARY KEY, key TEXT NOT NULL)''')

def get_key_db(user_id):
    c.execute("SELECT key FROM keys WHERE user_id=?", (user_id,))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return None

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=bot_status))


client.run(token)