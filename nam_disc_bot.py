import discord
import csv

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
# channels = discord.Client.get_all_channels()



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

        channel_list = []
        for guild in client.guilds:
            for channel in guild.text_channels:
                for elem in str(channel).split(" "):
                    channel_list.append(elem)
                
        await message.channel.send(f"Here are the channels you requested!\n{channel_list}")

    if message.content.startswith("!collect_text"):
        
        with open("messages2.csv", "w", newline="", encoding="utf-8") as f:
            
            writer = csv.writer(f)
            writer.writerow(["timestamp", "guild", "channel", "author", "content"])
            
            for guild in client.guilds:
                for channel in guild.text_channels:
                    await message.channel.send(f"hi {channel} :3")
                    try:
                        async for message in channel.history(limit=None, oldest_first=True):
                            # print(f"hi team im reading {str(message.content.replace("\n", " ").strip())} now")
                            # all_messages.append({
                            writer.writerow([
                                message.created_at,
                                guild.name,
                                channel.name,
                                message.author,
                                message.content.replace("\n", " ").strip()
                            ])
                    except discord.Forbidden:
                        print(f"Access denied to #{channel.name}")
                    except discord.HTTPException as e:
                        print(f"Failed to fetch messages from #{channel.name} with exception {e}")

            print(f"Fetched {len(all_messages)} messages total.")
            # for msg in all_messages[:10]:
            #     print(f"[{msg.channel}]) {msg.author}: {msg.content}")

    if message.content.startswith("!send_this_message" ):
        serv_id = 1124717630079651881
        chan_id = 1124717630775898174 

        chan = client.get_channel(chan_id)
        if chan:
            await chan.send(str(message.content).replace("!send_this_message", ""))
    
my_disc_key= "this is not a key " 
client.run(my_disc_key)