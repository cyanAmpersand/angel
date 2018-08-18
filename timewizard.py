import pickle

def loadTimezones(loadfile):
    try:
        f = open(loadfile,"rb")
        output = pickle.load(f)
        f.close()
    except FileNotFoundError:
        output = {}
    return output

def saveTimezones(savefile,timezones):
    f = open(savefile,"wb")
    pickle.dump(timezones,f)
    f.close()
    print("timezones saved")

def listTimes(users,timezones,time):
    result = "```"
    for z in timezones:
        for u in timezones[z]:
            result += timeString(time[0],time[1])[0]

def timeString(hour,minute):

    minute_s = "%02d"%minute
    time24 = "%02d"%hour + ":" + minute_s

    if hour == 0 or hour == 12:
        time12 = "12"
    else:
        time12 = str(hour)

    time12 += ":" + minute_s

    if hour < 12:
        time12 += " am"
    else:
        time12 += " pm"

    return [time24,time12]

if __name__ == "__main__":
    users = {
        "160481323746590731": "cyan",
        "190065758267637760": "zoey",
        "125424672765509632": "tenttle"
    }
    testcases = [
        [0,0],
        [1,0],
        [11,0],
        [12,0],
        [13,0],
        [23,0]
    ]
    for t in testcases:
        print(timeString(t[0],t[1])[0] + " = " + timeString(t[0],t[1])[1])