import re

def parsePoll(pollstring):
    pollstring = pollstring.strip()
    #regex: [^<>]+((<[^<>]+>\s*){2,})
    match = re.match("[^<>]+((<[^<>]+>\s*)+)",pollstring)
    if match == None:
        return "invalid poll string. please use the format `question <option1> <option2> <option3>`"
    else:
        pollsplit = re.split("[<>]",pollstring)
        question = pollsplit[0]
        options = pollsplit[1::2]
    return str(question + "\n" + str(options))

if __name__ == "__main__":
    print(parsePoll("question <option1> <option2> <option3>"))