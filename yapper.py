import discord, orjson, os
from discord.ext import commands

intents = discord.Intents(messages=True, guilds=True)
bot = commands.AutoShardedBot(
    command_prefix="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    help_command=None,
    intents=intents,
    chunk_guilds_at_startup=False,
    member_cache_flags=discord.MemberCacheFlags.none(),
    allowed_mentions=discord.AllowedMentions.none(),
)

try:
    with open("yapping.json", "rb") as f:
        yapping_channels = orjson.loads(f.read())
except FileNotFoundError:
    yapping_channels = []

@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.event
async def on_message(message):
    if message.channel.type == discord.ChannelType.public_thread and message.channel.parent_id in yapping_channels and message.author.id != message.channel.owner_id and (not message.interaction_metadata or message.interaction_metadata.user.id != message.channel.owner_id):
        await message.delete()

def save():
    with open('yapping.json', 'wb') as f:
        f.write(orjson.dumps(yapping_channels))

@bot.tree.command(description="Make the bot track a channel as a yapping channel")
@discord.app_commands.default_permissions(manage_channels=True)
async def addyappingchannel(message, channel: discord.ForumChannel):
    yapping_channels.append(channel.id)
    save()
    await message.response.send_message(f"<#{channel.id}> is now a yapping channel!")

@bot.tree.command(description="Make the bot no longer track a channel as a yapping channel")
@discord.app_commands.default_permissions(manage_channels=True)
async def removeyappingchannel(message, channel: discord.ForumChannel):
    yapping_channels.remove(channel.id)
    save()
    await message.response.send_message(f"<#{channel.id}> is no longer a yapping channel!")

bot.run(os.environ["YAPPER_TOKEN"])
