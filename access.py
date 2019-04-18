"""
Student: Kenneth Redillas
ID: 800100241
Date: 4/18/2019
Programming Assignment #2: MyFacebook
Class: CS465 - Cybersecurity
"""

# libraries that suffice
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
picture_tracking = dict()

# list to keep track of current picture objects
picture_objects = list()

# boolean values to keep track if someone is existing
is_viewing = False
does_admin_exist = False
admin = ''

# track who is viewing
who_is_viewing = []


class AccessControlList(object):
    pass


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


class Picture(object):
    name = ''
    picture_group = None
    owner = ''
    others = None  # TODO: difference of all friends and pricture_group
    permissions = None

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner


"""
Function: friendadd
Description: Creates an instance of a friend profile, not belonging to any list by default
"""


def friendadd(friendname):
    global does_admin_exist
    global admin
    if does_admin_exist == False:
        does_admin_exist = True
        admin = friendname

    if friendname in friend_txt_list:
        log_message("Error: Friend" + " " +
                    friendname + " already exists.")
        return
    #instance_friend = Friend(friendname)

    if is_viewing:
        if who_is_viewing[0] != admin:
            log_message("ERROR Friendadd failed: Username " + "\'" +
                        friendname + "\' is not an admin.")
            return

    friend_txt_list.append(friendname)
    log_message("Friend " + friendname + " added")
    with open('friends.txt', 'a+') as fObj:
        fObj.write(friendname + '\n')


def viewby(friendname):

    global is_viewing
    global who_is_viewing

    if friendname not in friend_txt_list:
        log_message("Login failed: invalid friend name")
        return
        # sys.exit(1)

    if (is_viewing == True):
        log_message("ERROR View failed: Username " + "\'" + who_is_viewing[0] +
                    "\' is viewing right now. " + "\'" + friendname +
                    "\' will not execute any commands then.")
        return
        # sys.exit(1)

    is_viewing = True
    who_is_viewing.append(friendname)
    if friendname == friend_txt_list[0]:
        log_message("Friend " + friendname +
                    " views the profile.")
    else:
        log_message("Friend " + friendname +
                    " views the profile.")


def logout():
    """
    A friend or you no longer views your profile
    """
    global is_viewing
    if is_viewing == False or len(who_is_viewing) == 0:
        pass
    else:
        is_viewing = False
        log_message("Friend " + who_is_viewing[0] + " has logged out.")
        who_is_viewing.pop()


def listadd(listname):
    global who_is_viewing
    if who_is_viewing[0] != friend_txt_list[0]:
        log_message("ERROR Listadd failed: Username " + "\'" + who_is_viewing[0] +
                    "\' can't  execute listadd because he/she is not the admin " + friend_txt_list[0])
        return
    if listname == "None" or listname == "nil" or listname == "null":
        log_message(
            "ERROR Listadd failed: Can't create a list called 'None' equivalent")
        return
    if listname in listOfFriendLists:
        log_message(
            "Error: Can't instantiate a list that already exists")
        return
    listOfFriendLists[listname] = list()
    log_message("List " + listname + " created")
    # 4/16/2019 7PM


def friendlist(friendname, listname):
    global who_is_viewing
    if friendname not in friend_txt_list:
        log_message("ERROR Username " + "\'" +
                    friendname + "\' does not exist")
        return
    if listname not in listOfFriendLists:
        log_message("ERROR Listname " + "\'" + listname + "\' does not exist")
        return
    if who_is_viewing[0] != friend_txt_list[0]:
        log_message("ERROR Username " + "'" +
                    who_is_viewing[0] + "' ain't an admin.")
        return
    temp = listOfFriendLists.get(listname)
    temp.append(friendname)
    log_message("Friend " + friendname + " added to list " + listname)


def postpicture(picturename):
    global is_viewing
    if is_viewing:
        temp = picturename
        if picturename.endswith('.txt'):
            temp = picturename.split('.txt')[0]
        if temp in picture_tracking:
            log_message("ERROR Posting picture failed: " +
                        picturename + " already exists")
            return
        picture_tracking[temp] = who_is_viewing[0]

        if not picturename.endswith('.txt'):
            picturename = picturename + '.txt'
        with open(picturename, 'a+') as fObj:
            fObj.write(temp + '\n')

        picture_obj = Picture(temp, who_is_viewing[0])
        picture_obj.permissions = {0: 'rw', 1: '--', 2: '--'}
        picture_objects.append(picture_obj)

        log_message("Picture " + temp + " with owner " +
                    picture_tracking[temp] + " and default permissions has been posted")

        with open('pictures.txt', 'w+') as fObj:
            fObj.write(picturename+'\n')

    else:
        log_message(
            "ERROR Posting picture failed: No one is viewing the profile")
        return


def chlst(picturename, listname):
    if is_viewing == False:
        log_message("ERROR chlst failed: Someone needs to view the profile.")
        return

    # if not picturename.endswith('.txt'):
    #     log_message("chlst failed: picturename must end with a .txt")
    #     return

    if listname not in listOfFriendLists:
        log_message("ERROR chlst failed: " + listname + " is not a list")
        return

    # valid
    nameOfPicture = picturename.split(".")[0]
    pic_reference = None
    for pic in picture_objects:
        if pic.name == nameOfPicture:
            pic_reference = pic
    if pic_reference == None:  # didn't find a pic object
        log_message("ERROR chlst failed: Reference to " +
                    picturename + " does not exist.")

    # at this point, we have found a picture object, compare owners
    if pic_reference.owner == picture_tracking[nameOfPicture] or pic_reference.owner == friend_txt_list[0]:
        if listname == "None" or listname == "nil":
            pic_reference.picture_group = None
            log_message(picturename + " is its own boss")
            return
        if who_is_viewing[0] == friend_txt_list[0]:
            pic_reference.picture_group = listOfFriendLists[listname]
            pic_reference.others = diffOf(
                friend_txt_list, listOfFriendLists[listname])

            log_message("List for " + picturename + " set to " +
                        listname + " by admin " + who_is_viewing[0])
            return
        elif pic_reference.owner not in listOfFriendLists[listname]:
            log_message("Error  with chlst: Friend " + pic_reference.owner +
                        " is not a member of friendlist " + listname)
            return
        else:
            pic_reference.picture_group = listOfFriendLists[listname]
            pic_reference.others = diffOf(
                friend_txt_list, listOfFriendLists[listname])
            log_message("List for " + picturename + " set to " +
                        listname + " by " + pic_reference.owner)

    else:
        log_message("ERROR chlst failed: User " +
                    who_is_viewing[0] + " can't chlst " + picturename)
        return


def chmod(picturename, perm_args):
    global is_viewing
    global who_is_viewing

    if is_viewing:
        for arg in perm_args:
            if len(arg) != 2:
                log_message("ERROR chmod: " + arg +
                            " is an invalid permission")
                return
            if not re.search('([r-])([w-])', arg):
                log_message(
                    "Error with chmod: permissions need correct format of set {rw-}")
                return
        # Check for whoever is viewing is the owner of the picture or is the profile owner
        if picturename.endswith('.txt'):
            picturename = picturename.split('.txt')[0]
        pic_reference = None
        for pic in picture_objects:
            if pic.name == picturename:
                pic_reference = pic
        if pic_reference == None:  # didn't find a pic object
            log_message("Error with chmod: " + picturename + " not found")
            return

        if who_is_viewing[0] == friend_txt_list[0] or who_is_viewing[0] == pic_reference.owner:
            pic_reference.permissions[0] = perm_args[0]
            pic_reference.permissions[1] = perm_args[1]
            pic_reference.permissions[2] = perm_args[2]
            print_this = ' '.join(perm_args)
            log_message("Permissions for " + picturename +
                        " set to " + print_this + " by " + who_is_viewing[0])
    else:
        log_message("ERROR chmod: no one is viewing the profile")
        return


def chown(picturename, friendname):
    if is_viewing == False:
        log_message("ERROR chown: Someone needs to view the profile")
        return
    if who_is_viewing[0] != admin:
        log_message("ERROR chown: User " +
                    who_is_viewing[0] + " is not an admin")
        return
    if friendname not in friend_txt_list:
        log_message("ERROR chown: User " + friendname + " not found")
        return

    if picturename.endswith('.txt'):
        picturename = picturename.split('.txt')[0]

    # if picturename not in picture_tracking:
    #     log_message("Picture " + picturename + " not found")

    for pic in picture_objects:
        if picturename == pic.name:
            pic.owner = friendname
            picture_tracking[picturename] = friendname
            log_message(picturename + "\'s owner is now " + friendname)
            return

    log_message("ERROR chown: Picture " + picturename + " not found")


def readcomments(picturename):
    if is_viewing:
        nameOfPicture = picturename.split(".txt")[0]
        pic_reference = None
        for pic in picture_objects:
            if pic.name == nameOfPicture:
                pic_reference = pic
        if pic_reference == None:  # didn't find a pic object
            log_message("ERROR readcomments failed: Reference to " +
                        picturename + " does not exist.")
            return

        # #CASES
        if pic_reference.picture_group == None:
            return

        if who_is_viewing[0] == pic_reference.owner and pic_reference.permissions[0][0] == 'r':
            with open(picturename, 'r') as fObj:
                line = fObj.readline()
                cnt = 0
                while line:
                    if cnt == 0:
                        print("User {}: {}".format(
                            who_is_viewing[0], line.strip()))
                    else:
                        print("Comment {}: {}".format(cnt, line.strip()))
                    line = fObj.readline()
                    cnt += 1

        #     pass

        elif who_is_viewing[0] != pic_reference.owner and who_is_viewing[0] in pic_reference.picture_group and pic_reference.permissions[1][0] == 'r':
            with open(picturename, 'r') as fObj:
                line = fObj.readline()
                cnt = 0
                while line:
                    if cnt == 0:
                        print("User {}: {}".format(
                            who_is_viewing[0], line.strip()))
                    else:
                        print("Comment {}: {}".format(cnt, line.strip()))
                    line = fObj.readline()
                    cnt += 1
        # pass
        elif who_is_viewing[0] != pic_reference.owner and (not (who_is_viewing[0] in pic_reference.picture_group)) and pic_reference.permissions[2][0] == 'r':
            with open(picturename, 'r') as fObj:
                line = fObj.readline()
                cnt = 0
                while line:
                    if cnt == 0:
                        print("User {}: {}".format(
                            who_is_viewing[0], line.strip()))
                    else:
                        print("Comment {}: {}".format(cnt, line.strip()))
                    line = fObj.readline()
                    cnt += 1
        # else:
            # log_message("OWNER:"+str(pic_reference.owner))
            # log_message("PERMISSIONS:"+str(pic_reference.permissions))
            # log_message("GROUP:"+str(pic_reference.picture_group))
            # log_message("OTHERS:"+str(pic_reference.others))
            # log_message(who_is_viewing[0]+" :ACCESS DENIED to " + picturename)
            # return

    else:
        log_message("Error: No one is viewing the profile.")
        return


def writecomments(picturename, text):
    if is_viewing:
        nameOfPicture = picturename.split(".txt")[0]
        pic_reference = None
        for pic in picture_objects:
            if pic.name == nameOfPicture:
                pic_reference = pic
        if pic_reference == None:  # didn't find a pic object
            log_message("ERROR writecomments failed: Reference to " +
                        picturename + " does not exist.")
            return

        # CASES

        if pic_reference.picture_group == None:
            return
            
        if who_is_viewing[0] == pic_reference.owner and pic_reference.permissions[0][1] == 'w':
            log_message(
                "Friend " + who_is_viewing[0] + " wrote to " + picturename + ": " + text)
            with open(picturename, 'a+') as fObj:
                fObj.write(text + '\n')
        elif who_is_viewing[0] != pic_reference.owner and (who_is_viewing[0] in pic_reference.picture_group) and pic_reference.permissions[1][1] == 'w':
            log_message(
                "Friend " + who_is_viewing[0] + " wrote to " + picturename + ": " + text)
            with open(picturename, 'a+') as fObj:
                fObj.write(text + '\n')
        elif who_is_viewing[0] != pic_reference.owner and (not (who_is_viewing[0] in pic_reference.picture_group)) and pic_reference.permissions[2][1] == 'w':
            log_message(
                "Friend " + who_is_viewing[0] + " wrote to " + picturename + ": " + text)
            
            with open(picturename, 'a+') as fObj:
                fObj.write(text + '\n')
        else:
            # log_message("OWNER:"+str(pic_reference.owner))
            # log_message("PERMISSIONS:"+str(pic_reference.permissions))
            # log_message("GROUP:"+str(pic_reference.picture_group))
            # log_message("OTHERS:"+str(pic_reference.others))
            log_message(who_is_viewing[0]+" :ACCESS DENIED to " + picturename)
            return

    else:
        log_message("Error: No one is viewing the profile.")
        return


def end():
    log_message("Terminated")


def switch_case(command_string, opt_arg1, opt_arg2, text):
    switcher = {
        "friendadd": lambda: friendadd(opt_arg1),
        "viewby": lambda: viewby(opt_arg1),
        "logout": logout,
        "listadd": lambda: listadd(opt_arg1),
        "friendlist": lambda: friendlist(opt_arg1, opt_arg2),
        "postpicture": lambda: postpicture(opt_arg1),
        "chlst": lambda: chlst(opt_arg1, opt_arg2),
        "chmod": lambda: chmod(opt_arg1, opt_arg2),
        "chown": lambda: chown(opt_arg1, opt_arg2),
        "readcomments": lambda: readcomments(opt_arg1),
        "writecomments": lambda: writecomments(opt_arg1, text),
        "end": lambda: end
    }
    func = switcher.get(command_string, lambda: "Invalid command")
    func()


def log_message(message):
    print(message)
    with open('audit.txt', 'a') as audit:
        audit.write(message + '\n')


def diffOf(bigpond, littlepond):
    return (list(set(bigpond) - set(littlepond)))


def main():
    # Clean slate
    with open('friends.txt', 'w+'), open('audit.txt.', 'w+'), open('pictures.txt.', 'w+'), open('lists.txt.', 'w+'):
        pass

    # Error Handling
    if (len(sys.argv) == 2):
        fileName = sys.argv[1]
        if not(fileName.endswith('.txt')):
            log_message("Your file should be in .txt format only!!!")
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
                log_message("You queried some invalid commands!")
                log_message("List of invalid commands: " + str(badCommands))
                return -1

            # if file is valid, continue checking
            if commands[0] != "friendadd":
                log_message("First command must be \"friendadd\".")

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
                    text = ''

                    if len(args) == 2:
                        parse = args[1]
                        parse = re.split('[\\s:/]', parse)
                        opt_arg1 = ''.join(parse)
                        # if "viewby" == command_arg and opt_arg1 == friend_txt_list[0]:
                        #     print(opt_arg1 + " now has administrator access!")
                        if len(opt_arg1) > 30:
                            log_message(
                                "ERROR Arguments must be less than 30 ascii")
                            return

                    elif command_arg == "chmod":
                        if len(args) != 5:
                            log_message("ERROR Must list 3 permissions")
                            return
                        parse = re.split('[\\s:/]', args[1])
                        opt_arg1 = ''.join(parse)
                        if len(opt_arg1) > 30:
                            log_message(
                                "ERROR Arguments must be less than 30 ascii")
                            return
                        my_list = [args[2], args[3], args[4]]
                        opt_arg2 = my_list

                    elif command_arg == "writecomments":
                        parse = query.split()[1]
                        parse = re.split('[\\s:/]', parse)
                        opt_arg1 = ''.join(parse)
                        divider = "writecomments " + opt_arg1
                        text = query.split(divider)[1]
                        if len(opt_arg1) > 30:
                            log_message(
                                "ERROR Arguments must be less than 30 ascii")
                            return

                    elif len(args) == 3:
                        parse = re.split('[\\s:/]', args[1])
                        parse2 = re.split('[\\s:/]', args[2])
                        opt_arg1 = ''.join(parse)
                        opt_arg2 = ''.join(parse2)
                        if len(opt_arg1) > 30:
                            log_message(
                                "ERROR Arguments must be less than 30 ascii")
                            return
                        if len(opt_arg2) > 30:
                            log_message(
                                "ERROR Arguments must be less than 30 ascii")
                            return

                    switch_case(command_arg, opt_arg1, opt_arg2, text)
            end()

        except IOError:
            log_message("File not found.")

    else:
        log_message(
            "Error: Need to have a test case file as an argument, where file is the one argument.")
        log_message("Format should be: python access.py [filename]")


if __name__ == "__main__":
    main()
