import pickle

class UserList:
    def __init__(self):
        self.userlist = []
        self.serverlist = []

    def getServer(self,id: str):
        for server in self.serverlist:
            if server.id == id:
                return server
        return None

    def getUser(self,id: str):
        for user in self.userlist:
            if user.id == id:
                return user
        return None

    def addUser(self,id: str,serverid: str):
        user = self.getUser(id)
        server = self.getServer(serverid)
        if user is None:
            user = User(id)
            self.userlist.append(user)

        if server is None:
            server = Server(serverid)
            self.serverlist.append(server)

        user.serverIds.add(serverid)
        server.userIds.add(id)

        return user

    def save(self,savefile):
        f = open(savefile,"wb")
        pickle.dump(self,f)
        f.close()
        print("users saved")

    def load(self,loadfile):
        output = self
        try:
            f = open(loadfile,"rb")
            output = pickle.load(f)
            f.close()
        except FileNotFoundError:
            pass
        return output


class Server:
    def __init__(self,id: str):
        self.id = id
        self.userIds = set()

class User:
    def __init__(self,id: str):
        self.id = id
        self.serverIds = set()

if __name__ == "__main__":
    userlist1 = UserList()

    userlist1.addUser("u0005", "s0001")
    userlist1.addUser("u0005", "s0002")
    userlist1.addUser("u0003", "s0002")
    userlist1.addUser("u0004", "s0003")
    userlist1.addUser("u0001", "s0003")
    userlist1.addUser("u0006", "s0002")
    userlist1.addUser("u0001","s0001")
    userlist1.addUser("u0001", "s0002")
    userlist1.addUser("u0002", "s0001")
    userlist1.addUser("u0002", "s0003")

    print(len(userlist1.userlist))

    for u in userlist1.userlist:
        print(u.id)
        print(u.serverIds)

    print(len(userlist1.serverlist))

    for s in userlist1.serverlist:
        print(s.id)
        print(s.userIds)