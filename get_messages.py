import discord
import csv

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
# channels = discord.Client.get_all_channels()

channel_list = []
all_messages = []

# To log when connection is successful.
@client.event
async def onready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    # check if message origins came from us
    if message.author == client.user:
        return

    if message.content.startswith("hello"):
        await message.channel.send("Greetings !!!")

    if message.content.startswith("_channels"):
        for guild in client.guilds:
            for channel in guild.text_channels:
                for elem in str(channel).split(" "):
                    channel_list.append(elem)
        await message.channel.send(f"Here are the channels you requested!\n{channel_list}")
        
    if message.content.startswith("collect_text"):
        
        with open("messages.csv", "w", newline="", encoding="utf-8") as f:
            
            writer = csv.writer(f)
            writer.writerow(["timestamp", "guild", "channel", "author", "content"])
            
            for guild in client.guilds:
                for channel in guild.text_channels:
                    await message.channel.send(f"Working on {channel} now.")
                    try:
                        async for message in channel.history(limit=None, oldest_first=True):
                            print(f"Working on {str(message.content.replace("\n", " ").strip())} now")
                            # all_messages.append({
                            writer.writerow([
                                message.created_at,
                                guild.name,
                                channel.name,
                                message.content.replace("\n", " ").strip()
                            ])
                    except discord.Forbidden:
                        print(f"Access denied to #{channel.name}")
                    except discord.HTTPException as e:
                        print(f"Failed to fetch messages from #{channel.name} with exception {e}")

            print(f"Fetched {len(all_messages)} messages total.")
            # for msg in all_messages[:10]:
            #     print(f"[{msg.channel}]) {msg.author}: {msg.content}")

    

client.run("some tokens probably")
