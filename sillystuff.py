import random
import botfunctions

def infinitysnap(members):
    deaths = 0
    response = "```"
    for m in members:
        name = m.name
        if (random.random() > 0.5 or m.id == "125424672765509632") and m.id != "190065758267637760":
            response += name + " was killed.\n"
            deaths += 1
        else:
            response += name + " was spared.\n"
    response += str(deaths) + "/" + str(len(members)) + " users were killed. The server is now balanced, as all things should be.```"
    return response

def infinitysnaptest(usernames):
    response = "```"
    for u in usernames:
        if random.random() > 0.5:
            response += usernames[u] + " was killed.\n"
        else:
            response += usernames[u] + " was spared.\n"
    response += "```"
    return response

if __name__ == "__main__":
    all_users = {
        "160481323746590731": "chloe",
        "190065758267637760": "zoey",
        "125424672765509632": "tenttle",
        "196422115212132353": "rory",
        "166068876008882176": "chris",
        "208122604161204224": "autumn",
        "140324228745396225": "bard",
        "262794787248144385": "shannon",
        "204439791675113473": "tosh",
        "195339166769217536": "kit"
    }

    print(infinitysnaptest(all_users))