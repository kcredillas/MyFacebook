import cmd
import sys
import re


# list of valid commands to use in the test case file
validCommands = ['friendadd', 'viewby', 'logout', 'listadd', 'friendlist',
                 'postpicture', 'chlst', 'chmod', 'chown', 'readcomments', 'writecomments', 'end']

# list of all profiles online (in the friends.txt file)
friend_txt_list = list()

# list that keeps track of friend lists
listOfFriendLists = dict()

# dictionary that keeps track of picture associated to the owner and the pictures posted
picture_traking = dict()

# boolean value to keep track if someone is viewing or not
is_viewing = False

#track who is viewing
who_is_viewing = []


class AccessControlList(object):
    pass


class Person(object):
    pass
    """
    isFriend = False #default value of a friend
    def __init__(self, name, AccessControlList):
        self.name = name
        self.AccessControlList = AccessControlList

    def is_Friend(self):
        return self.isFriend
    """


class Admin(object):
    name = None
    AccessControlList = None
    online_status = False

    def __init__(self, name):
        self.name = name

    @classmethod
    def from_ACL(cls, AccessControlList):
        cls.AccessControlList = AccessControlList

    @classmethod
    def set_online(cls, online_status):
        cls.online_status = online_status


"""
Function: friendadd
Description: Creates an instance of a friend profile, not belonging to any list by default
"""


def friendadd(friendname):
    if friendname in friend_txt_list:
        print("Error: Username " + "\'" + friendname + "\' already exists.")
        # TODO: Report to audit.txt
        exit
    #instance_friend = Friend(friendname)
    friend_txt_list.append(friendname)
    
    with open('friends.txt', 'a+') as fObj:
        fObj.write(friendname + '\n')


def viewby(friendname):
    """ 
    To simplify the assignment MyFacebook does not support concurrent users.
    That is, only one friend at a time can view your profile.
    (If one of your friends is viewing your profile, another friend cannot view it.
    """
    global is_viewing
    global who_is_viewing

    if friendname not in friend_txt_list:
        print("Error: Username " + "\'" + friendname +
              "\' is not in friends.txt file.")
        return
        #sys.exit(1)

    if (is_viewing == True):
        print("Error: Username " + "\'" + who_is_viewing[0] +
              "\' is viewing right now. " + "\'" + friendname +
              "\' will not execute any commands then.")
        return
        #sys.exit(1)

    is_viewing = True
    who_is_viewing.append(friendname)
    if friendname == friend_txt_list[0]:
        print("Supreme Leader of MyFacebook " + "\'" + friendname +
              "\' is viewing his/her profile.")
    else:
        print("Friend " + "\'" + friendname +
              "\' is viewing the profile.")


def logout():
    """
    A friend or you no longer views your profile
    """
    global is_viewing
    if is_viewing == False or len(who_is_viewing) == 0:
        pass
    else:
        is_viewing = False
        print(who_is_viewing[0] + " is no longer viewing profile.")
        who_is_viewing.pop()

def listadd(listname):
    global who_is_viewing
    if who_is_viewing[0] != friend_txt_list[0]:
        print("Error: Username " + "\'" + who_is_viewing[0] +
              "\' can't  execute listadd because he/she is not the Supreme Leader of MyFacebook " + friend_txt_list[0])
        return
    if listname == "nil":
        print("Error: Can't create a list called 'nil'")
        return
    if listname in listOfFriendLists:
        print("Error: Can't instantiate a list that already exists")
        return
    listOfFriendLists[listname] = list()
    print(str(listOfFriendLists))
    #4/16/2019 7PM


    
    

def friendlist(friendname, listname):
    global who_is_viewing
    if friendname not in friend_txt_list:
        print("Error: Username " + "\'" + friendname + "\' does not exist")
        return
    if listname not in listOfFriendLists:
        print("Error: Listname " + "\'" + listname + "\' does not exist")
        return
    if who_is_viewing[0] != friend_txt_list[0]:
        print("Error: Username " + "'" + who_is_viewing[0] + "' ain't an admin.")
        return
    temp = listOfFriendLists.get(listname)
    temp.append(friendname)
    
    print(str(listOfFriendLists))

def postpicture():
    pass


def chlst():
    pass


def chmod():
    pass


def chown():
    pass


def readcomments():
    pass


def writecomments():
    pass


def end():
    pass


def switch_case(command_string, opt_arg1, opt_arg2):
    switcher = {
        "friendadd": lambda: friendadd(opt_arg1),
        "viewby": lambda: viewby(opt_arg1),
        "logout": logout,
        "listadd": lambda: listadd(opt_arg1),
        "friendlist": lambda: friendlist(opt_arg1, opt_arg2),
        "postpicture": postpicture,
        "chlst": chlst,
        "chmod": chmod,
        "chown": chown,
        "readcomments": readcomments,
        "writecomments": writecomments,
        "end": end
    }
    func = switcher.get(command_string, lambda: "Invalid command")
    func()


def main():
    # Clear and overwrite files
    with open('friends.txt', 'w+'), open('audit.txt.', 'w+'), open('pictures.txt.', 'w+'), open('lists.txt.', 'w+'):
        pass

    # Error Handling
    if (len(sys.argv) == 2):
        fileName = sys.argv[1]
        if not(fileName.endswith('.txt')):
            print("Your file should be in .txt format only!!!")
            return -1
        try:
            fObj = open(fileName, 'r')
            badCommands = list()
            queries = list()
            commands = list()
            for line in fObj:
                command = line.split(' ')[0]
                if command.strip() not in validCommands:
                    badCommands.append(command)
                else:
                    # this is a valid command!
                    queries.append(line.strip())
                    commands.append(command)
            fObj.close()

            if (len(badCommands) > 0):
                print("You queried some invalid commands!")
                print("List of invalid commands: " + str(badCommands))
                return -1

            # if file is valid, continue checking
            if commands[0] != "friendadd":
                print("First command must be \"friendadd\".")
                # TODO: report error to audit log file
                return -1
            else:  # parse the commands
                # if second command is not equal to viewby, repeat until he successfully goes through
                #admin = Admin(queries[0].split()[1])
                # print(admin.name)

                for query in queries:
                    args = query.split()
                    command_arg = args[0]
                    opt_arg1 = None
                    opt_arg2 = None
                    # TODO: Handle regex for friendname, listname, and picturename args
                    if len(args) == 2:
                        parse = args[1]
                        parse = re.split('[\\s:/]', parse)
                        opt_arg1 = ''.join(parse)
                        if "viewby" == command_arg and opt_arg1 == friend_txt_list[0]:
                            print(opt_arg1 + " now has administrator access!")
                            #TODO: give him priveleges

                    elif len(args) == 3:
                        parse = re.split('[\\s:/]', args[1])
                        parse2 = re.split('[\\s:/]', args[2])
                        opt_arg1 = ''.join(parse)
                        opt_arg2 = ''.join(parse2)

                    switch_case(command_arg, opt_arg1, opt_arg2)

        except IOError:
            print("File not found.")
            # TODO: report file error to audit log file

    else:
        print("Error: Need to have a test case file as an argument, where file is the one argument.")
        print("Format should be: python access.py [filename]")


if __name__ == "__main__":
    main()
