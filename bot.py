import discord
import timewizard as twz
import rngesus
import botfunctions
import snapture
import hexcodes
import poll
import urllib.request
import time
import asyncio
import sys
import os
import random

start_time = time.time()

testing = True
linux = False
if sys.platform == "linux":
    print("running linux")
    linux = True
    testing = False
rpi_dir = "/home/chloe/angel/"

message_logging_on = False
twz_on = False
rngesus_on = True
snapture_on = False
hexcodes_on = True
imageshortcuts_on = False
quotes_on = True
pinbot_on = True
poll_on = True

logged_messages = []

statuses = []

message_logs = []

if twz_on:
    statuses.append("time wizard 2.0")
if rngesus_on:
    statuses.append("RNGesus 2.0")
if snapture_on:
    statuses.append("snapture")
if hexcodes_on:
    statuses.append("hex codes")
if imageshortcuts_on:
    statuses.append("image shortcuts")
if quotes_on and message_logging_on:
    statuses.append("quotes")
if pinbot_on:
    statuses.append("pinbot")

file_dir = "../"

if testing:
    token = botfunctions.loadToken(file_dir + "testbot.tkn").strip()
    cmd_prefix = "!t_"
    statuses = ["chloe is tinkering"]
else:
    token = botfunctions.loadToken(file_dir + "angel.tkn").strip()
    cmd_prefix = "!"

client = discord.Client()

output_channel = "395422229074018320"

all_servers = {}
all_channels = {}
message_logs = []
user_ids = {}
emoji = {}
snapture_editing = {
    "message":None,
    "edits":[],
    "content_new":""
}

async def bg_status():
    await client.wait_until_ready()
    counter = 0
    while not client.is_closed:
        await client.change_presence(game=discord.Game(name=statuses[counter%len(statuses)]))
        #print(statuses[counter%len(statuses)])
        await asyncio.sleep(10)
        counter += 1

async def snapture_edit():
    await client.wait_until_ready()
    while not client.is_closed:
        if snapture_editing["message"] is not None:
            print("snapping...")
            snapture_editing["content_new"] = snapture_editing["message"].content
            print(snapture_editing["edits"])
            for e in snapture_editing["edits"][:-1]:
                print(e)
                snapture_editing["content_new"] += "\n" + e
                await client.edit_message(snapture_editing["message"],"```" + snapture_editing["content_new"] + "```")
                await asyncio.sleep(3*random.random())
            await client.edit_message(snapture_editing["message"], "```" + snapture_editing["content_new"] + "```" + snapture_editing["edits"][-1])
            print("snap done")
            snapture_editing["message"] = None
            snapture_editing["edits"] = []
            snapture_editing["content_new"] = ""
        await asyncio.sleep(1)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    #await client.change_presence(game=discord.Game(name="initializing..."))

    for s in client.servers:
        all_servers[s.id] = s
        for c in s.channels:
            all_channels[c.id] = c
        for m in s.members:
            user_ids[m.id] = m.name

    for m in user_ids:
        print(m + " " + user_ids[m])

    if message_logging_on:
        for channel in all_channels:
            async for message in client.logs_from(channel,limit=999999):
                print(message.channel.name + " / " + message.author.name + ": " + message.clean_content)
                message_logs.append(message)

    #await client.change_presence(game=discord.Game(name="chloe is tinkering"))

    print("found " + str(len(message_logs)) + " messages in " + str(time.time() - start_time) + " seconds")

    c_output = client.get_channel(output_channel)
    await client.send_message(c_output,"4N631 online.")

    print('ready')

@client.event
async def on_reaction_add(reaction,user):
    print("reaction added")
    e_pin = "\U0001F4CC"
    pin_threshold = 3
    bandwagon_threshold = 5
    if reaction.emoji == e_pin and pinbot_on:
        print("emoji = " + e_pin)
        for r in reaction.message.reactions:
            if r.emoji == e_pin:
                if r.count >= pin_threshold:
                    await client.pin_message(reaction.message)
                if r.count >= bandwagon_threshold:
                    await client.add_reaction(reaction.message,"\U0001F4CC")

@client.event
async def on_message(message):

    response = None
    responseChannel = message.channel

    if message.author.bot:
        pass
    else:
        if message.content.startswith(cmd_prefix):
            msgstr = message.content[len(cmd_prefix)::].lower()
            if msgstr == "help":
                try:
                    await client.send_file(responseChannel,"help.png",filename="help.png")
                except FileNotFoundError:
                    await client.send_file(responseChannel,rpi_dir + "help.png", filename="help.png")
            if rngesus_on:
                if msgstr.startswith("roll "):
                    print("roll called")
                    print(msgstr)
                    parsed = rngesus.parseroll(msgstr[5:])
                    if parsed is None:
                        response = "fucka you"
                    else:
                        n = parsed[0]
                        max = parsed[1]
                        mod = parsed[2]
                        adv = parsed[3]
                        if n <= 100 and max <= 1000:
                            #response = rngesus.Roll(max,n,mod,adv).string()
                            r = rngesus.Roll(max,n,mod,adv)
                            response_embed = discord.Embed(title=str(r.sum()),description=r.string())
                            await client.send_message(message.channel, embed=response_embed)
                        else:
                            response = "out of range"
            if hexcodes_on:
                if msgstr.startswith("hex"):
                    print("hex called")
                    if hexcodes.is_valid_hex(msgstr[3::]):
                        url = hexcodes.get_hex_image(msgstr[3::])
                        urllib.request.urlretrieve(url,file_dir + "colour.png")
                        await client.send_file(responseChannel,file_dir + "colour.png")
                        #response = url
                    elif "roblox" in msgstr:
                        urllib.request.urlretrieve(hexcodes.get_hex_image("00F"), file_dir + "colour.png")
                        try:
                            await client.send_file(responseChannel,"colour.png")
                        except FileNotFoundError:
                            await client.send_file(responseChannel,rpi_dir + "colour.png")
                    else:
                        response = "Not a valid hex code."
            if snapture_on:
                if msgstr.startswith("snapture"):
                    print("snap called")
                    if "slow" in msgstr:
                        if snapture_editing["message"] is None:
                            try:
                                snap_message = await client.send_file(responseChannel, "snap.png", filename="snap.png")
                            except FileNotFoundError:
                                snap_message = await client.send_file(responseChannel, rpi_dir + "snap.png",filename="snap.png")
                            print(snap_message.id)
                            snapture_editing["edits"] = snapture.infinitysnap(message.server.members)
                            snapture_editing["message"] = snap_message
                        else:
                            await client.send_message(responseChannel,"Whoa there Thanos, there's a snapture already in progress.")
                    else:
                        snapstring = snapture.infinitysnap(message.server.members)
                        msg_content = "```" + "\n".join(snapstring[:-1]) + "```" + snapstring[-1]
                        try:
                            await client.send_file(responseChannel,"snap.png",filename = "snap.png",content=msg_content)
                        except FileNotFoundError:
                            await client.send_file(responseChannel, rpi_dir + "snap.png", filename="snap.png", content=msg_content)
            if quotes_on and message_logging_on:
                if msgstr.startswith("quote"):
                    msgid = msgstr.split("quote")[1].strip()
                    for m in message_logs:
                        if m.id == msgid:
                            response = "```#" + m.channel.name + " / " + m.author.display_name + "\n" + m.clean_content + "```"
                    if response == None:
                        response = "message with id " + msgid + " not found"
            if poll_on:
                if msgstr.startswith("poll"):
                    pollcommand = msgstr.split("poll")[1].strip()
                    response = poll.parsePoll(pollcommand)

        if (message.content.find("@someone") != -1 and not testing) or (message.content.find(cmd_prefix + "@someone") != -1 and testing):
            users = []
            for member in message.server.members:
                if not member.bot:
                    users.append(member)
            response = "**@someone:** " + random.choice(users).name

    if response is not None:
        await client.send_message(responseChannel,response)

client.loop.create_task(bg_status())
if snapture_on:
    client.loop.create_task(snapture_edit())
client.run(token)
