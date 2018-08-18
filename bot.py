import discord
import timewizard as twz
import rngesus
import botfunctions
import sillystuff
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
sillystuff_on = True
hexcodes_on = True
imageshortcuts_on = False
quotes_on = True
pinbot_on = True
poll_on = True

statuses = []

if twz_on:
    statuses.append("time wizard 2.0")
if rngesus_on:
    statuses.append("RNGesus 2.0")
if sillystuff_on:
    statuses.append("snapture")
if hexcodes_on:
    statuses.append("hex codes")
if imageshortcuts_on:
    statuses.append("image shortcuts")
if quotes_on and message_logging_on:
    statuses.append("quotes")
if pinbot_on:
    statuses.append("pinbot")

if linux:
    file_dir = "/home/chloe/angel/"
else:
    file_dir = ""

if testing:
    token = botfunctions.loadToken(file_dir + "testbot.tkn")
    cmd_prefix = "!t_"
    statuses = ["chloe is tinkering"]
else:
    token = botfunctions.loadToken(file_dir + "angel.tkn")
    cmd_prefix = "!"

client = discord.Client()

if testing:
    output_channel = "452631971764502528"
else:
    output_channel = "392516565364375576"

all_servers = {}
channels = []
message_logs = []
members = []
emoji = {}

async def bg_status():
    await client.wait_until_ready()
    counter = 0
    while not client.is_closed:
        await client.change_presence(game=discord.Game(name=statuses[counter%len(statuses)]))
        print(statuses[counter%len(statuses)])
        await asyncio.sleep(10)
        counter += 1

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await client.change_presence(game=discord.Game(name="initializing..."))

    friendzone = client.get_server("208293541435277313")

    for s in client.servers:
        all_servers[s.id] = s

    for c in friendzone.channels:
        channels.append(c)

    for m in friendzone.members:
        if not m.bot:
            members.append(m)
            print(m.display_name)

    if message_logging_on:
        for channel in channels:
            async for message in client.logs_from(channel,limit=999999):
                print(message.channel.name + " / " + message.author.name + ": " + message.clean_content)
                message_logs.append(message)

    #await client.change_presence(game=discord.Game(name="chloe is tinkering"))

    print("found " + str(len(message_logs)) + " messages in " + str(time.time() - start_time) + " seconds")

    c_output = friendzone.get_channel(output_channel)
    await client.send_message(c_output,"4N631 online.")

    print('ready')

@client.event
async def on_reaction_add(reaction,user):
    print("reaction added")
    e_pin = "\U0001F4CC"
    pin_threshold = 2
    if reaction.emoji == e_pin and pinbot_on:
        print("emoji = " + e_pin)
        for r in reaction.message.reactions:
            if r.emoji == e_pin:
                if r.count >= pin_threshold:
                    await client.pin_message(reaction.message)
                    await client.add_reaction(reaction.message,"\U0001F4CC")

@client.event
async def on_message(message):

    response = None
    responseChannel = message.channel

    if message.author.bot:
        pass
    else:
        if message.content.startswith(cmd_prefix):
            msgstr = message.content[len(cmd_prefix)::]
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
                        try:
                            await client.send_file(responseChannel,"colour.png")
                        except FileNotFoundError:
                            await client.send_file(responseChannel,rpi_dir + "colour.png")
                        #response = url
                    elif "roblox" in msgstr:
                        urllib.request.urlretrieve(hexcodes.get_hex_image("00F"), file_dir + "colour.png")
                        try:
                            await client.send_file(responseChannel,"colour.png")
                        except FileNotFoundError:
                            await client.send_file(responseChannel,rpi_dir + "colour.png")
                    else:
                        response = "Not a valid hex code."
            if sillystuff_on:
                if msgstr.startswith("snapture"):
                    msg_content = sillystuff.infinitysnap(members)
                    print("snap called")
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
client.run(token)