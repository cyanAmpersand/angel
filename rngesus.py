import random
import re

class Roll:
    def __init__(self,max,n=1,mod=0,adv=None):
        self.max = max
        self.n = n
        self.mod = mod
        if adv == "a" or adv == "d":
            self.adv = adv
        else:
            self.adv = None
        self.results = []
        self.results_high = []
        self.results_low = []
        for r in range(n):
            r1 = random.randint(1,max) + self.mod
            r2 = random.randint(1,max) + self.mod
            self.results.append(r1)
            if r1 > r2:
                self.results_high.append(r1)
                self.results_low.append(r2)
            else:
                self.results_high.append(r2)
                self.results_low.append(r1)

    def sum(self):
        sum_result = 0
        if self.adv is None:
            for x in self.results:
                sum_result += x
        elif self.adv == "a":
            for x in self.results_high:
                sum_result += x
        elif self.adv == "d":
            for x in self.results_low:
                sum_result += x
        return sum_result

    def string(self):
        if self.n == 8 and self.max == 8 and self.mod == 0:
            response = "rolled the fluorite octet"
        else:
            response = "rolled " + str(self.n) + "d" + str(self.max)
        if self.mod > 0:
            response += "+" + str(self.mod)
        elif self.mod < 0:
            response += str(self.mod)
        if self.adv == "a":
            response += " with advantage"
        elif self.adv == "d":
            response += " with disadvantage"
        response += ":\n"
        for i in range(self.n):
            if self.adv is None:
                response += str(self.results[i] - self.mod)
            elif self.adv == "a":
                response += "**" + str(self.results_high[i] - self.mod) + "**|" + str(self.results_low[i] - self.mod)
            elif self.adv == "d":
                response += "**" + str(self.results_low[i] - self.mod) + "**|" + str(self.results_high[i] - self.mod)

            if self.mod > 0:
                response += "+" + str(self.mod)
            elif self.mod < 0:
                response += str(self.mod)

            if i != self.n - 1:
                response += " + "
        result_sum = 0
        if self.adv is None:
            result_sum += sum(self.results)
        elif self.adv == "a":
            result_sum += sum(self.results_high)
        elif self.adv == "d":
            result_sum += sum(self.results_low)
        response += " = " + str(result_sum)
        return response

def advantage(roll1,roll2):
    result = []
    n = len(roll1)
    for x in range(n):
        if roll1[x] > roll2[x]:
            result.append(roll1[x])
        else:
            result.append(roll2[x])
    return result

def disadvantage(roll1,roll2):
    result = []
    n = len(roll1)
    for x in range(n):
        if roll1[x] < roll2[x]:
            result.append(roll1[x])
        else:
            result.append(roll2[x])
    return result

def parseroll(rollstr):
    valid = True
    rollstr = rollstr.lower().strip()
    if re.fullmatch("\d*d\d+([+-]\d+)?[da]?", rollstr) is not None:
        adv = None
        if rollstr[-1] == "a":
            adv = "a"
            rollstr = rollstr[:-1]
        elif rollstr[-1] == "d":
            adv = "d"
            rollstr = rollstr[:-1]
        if rollstr[0] != "d":
            n = int(rollstr.split("d")[0])
            if n < 1:
                valid = False
        else:
            n = 1
        rollstr = rollstr.split("d")[1]
        mod = 0
        if len(rollstr.split("+")) == 2:
            mod = int(rollstr.split("+")[1])
        if len(rollstr.split("-")) == 2:
            mod = int(rollstr.split("-")[1]) * -1
        max = int(re.split("[+-]", rollstr)[0])

        # n = rollstr.split("d")[0]
        # adv = None
        # if n == "": n = 1
        # else:
        #     n = int(n)
        #     if n < 1: valid = False
        # if rollstr[-1] == "a":
        #     adv = "a"
        #     rollstr = rollstr[:-1]
        # elif rollstr[-1] == "d":
        #     adv = "d"
        #     rollstr = rollstr[:-1]
        # min = 1
        # max = int(re.split("[+-]",rollstr.split("d")[1])[0])
        if valid:
            #print("parse successful")
            #print(n,max,mod,adv)
            #return roll(n,1,max,mod)
            return [n,max,mod,adv]

    print("pasring failed")
    return None

def messagestring(roll):
    result = ""


if __name__ == "__main__":
    parsing_test_cases = [
        "4d20+1a",
        "5d8+1d",
        "6d12+1",
        "2d6a",
        "4d4",
        "d12d",
        "0d20",
        "99999d99999",
        "99999d99999+99999a"
    ]

    for test in parsing_test_cases:
        print("#parsing " + test)
        parsed = parseroll(test)
        print(parsed)
        if parsed is not None:
            n = parsed[0]
            max = parsed[1]
            mod = parsed[2]
            adv = parsed[3]
            test_roll = Roll(max,n,mod,adv)
            print(test_roll.string())
        print()
