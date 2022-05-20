#this will allow the user to interact with a comphrensive list of mudae bot bundles.
#accounts.txt is the file containing all accounts with username and pasword and disablelist. Disablelist Can have max 10 bundles (no duplicates), and displays the  totals 
#  fix the special characters issues in some bundles (the user can't type special characters!), 
import os
clear = lambda: os.system('cls')
import json
f = open('info.txt', encoding = 'utf8')
bundlesRaw = f.read().splitlines()
f.close()
bundles = {} #organize bundle into list of dictionaries
aFile = open('accounts.txt', encoding = 'utf8')
accounts = json.loads(aFile.read())
aFile.close()



for i in bundlesRaw: # we need to use a dictionary rather than an array with the names as keys obviously
    
    i = i.lower().split('\t') #names will be lower cased
    bundles[i[0]] = {
        'tot': int(i[1]),
        'wa': int(i[2]),
        'ha': int(i[3]),
        'wg': int(i[4]),
        'hg' : int(i[5]),
        '%wa': float(i[6]),
        '%ha': float(i[7]), #not sure why this is blue, but no errors so far!
        '%wg': float(i[8]),
        '%hg' : float(i[9])
    }

def bundlePrint(bundle):

    string = [bundle]

    for i2 in bundles[bundle]:

        string.append(i2 +': ' + str(bundles[bundle][i2]))

    print(' '.join(string))


def main(username):

    global accounts

    while True:

        cmd = input('enter commmand ').lower().split(' ') #input will be case insensitive
        clear() #we want to clear the console after a command is inputted
        args = cmd[1:len(cmd)]
        cmd = cmd[0]

        if cmd == "displayall":

            for bundle in bundles:

                bundlePrint(bundle)

        elif cmd == "display":

            if len(args) >= 3:

                quant = args[2]

                try: #check if quantity is a number

                    quant = int(quant)

                    attr = args[1]

                    if attr in bundles['western']: #Western is our first bundle which we are using as a template to check if attr is valid             
                        
                        if args[0] == 'min':

                            for bundle in bundles:

                                if bundles[bundle][attr] >= quant:

                                    bundlePrint(bundle)
                        
                        elif args[0] == 'max':

                            for bundle in bundles:

                                if bundles[bundle][attr] <= quant:
                                    
                                    bundlePrint(bundle)

                        else:

                            print('invalid first argument')
                    
                    else:

                        print('invalid attribute')

                except:

                    print('invalid quantity')
            else:

                print('not enough arguments given')

        elif cmd == 'add':

            names = ' '.join(args)
            names = names.split(' $') #names are seperated using a space and $ sign at the start of a new name.
            dl = accounts[username]['dl']

            for name in names:
                
                if name in bundles:

                    if len(dl['list']) < 10 and bundles[name]['tot'] + dl['tot'] <= 21000 and name not in dl['list']: #if the disablelist is not full and we are not adding a duplicate or nonexistent bundle

                        dl['list'][name] = bundles[name]
                        # add everything to disablelist
                        dl['tot'] += bundles[name]['tot']
                        dl['wa'] += bundles[name]['wa']
                        dl['ha'] += bundles[name]['ha']
                        dl['wg'] += bundles[name]['wg']
                        dl['hg'] += bundles[name]['hg']
                        print('{} added to disablelist.'.format(name))

                    else:

                        print('Cannnot add ' + name +  ' to the disablelist')
                
                else:

                    print(name + ' is an invalid bundle name')

        elif cmd == 'remove':
            
            names = ' '.join(args)
            names = names.split(' $') #names are seperated using a space and $ sign at the start of a new name
            dl = accounts[username]['dl']

            for name in names:

                if name in dl['list']:

                    del dl['list'][name]
                    dl['tot'] -= bundles[name]['tot']
                    dl['wa'] -= bundles[name]['wa']
                    dl['ha'] -= bundles[name]['ha']
                    dl['wg'] -= bundles[name]['wg']
                    dl['hg'] -= bundles[name]['hg'] 
                    print('{} removed from disablelist.'.format(name))
                    
                else:

                    print(name + ' is not a valid bundle name!')

        elif cmd == "list":
            
            dl = accounts[username]['dl']

            for bundle in dl['list']:

                bundlePrint(bundle)
            
            print('\nnum: {}; tot: {}; wa: {}; ha: {}; wg: {}; hg: {}'.format(str(len(dl['list'])), dl['tot'], dl['wa'], dl['ha'], dl['wg'], dl['hg']))

        elif cmd == 'quit':

            break
        
        elif cmd == 'help':
            print(menuString)
        
        elif cmd == 'find': #user types in a string and we try to find all bundles that contain that string in their name and display them. We ignore capitalization here.
            searchString = ' '.join(args)

            for bundle in bundles:

                if searchString in bundle:
                    
                    bundlePrint(bundle)

        elif cmd == 'clear':

            accounts[username]['dl'] = {
                                "list": {},
                                "tot": 0,
                                "wa": 0,
                                "ha": 0,
                                "wg": 0,
                                "hg": 0
                            }
            print('disablelist cleared')
        
        elif  cmd == 'delete':

            while True:

                answer  = input("Are you sure you want to delete this account and all of its information? Y/N ")
                clear()

                if answer == 'y' or answer == 'yes':

                    del accounts[username]
                    print('account has been deleted')
                    return login()
                
                elif answer == 'n' or answer == 'no':

                    break

                else:

                    print('YES OR NO')

        elif cmd== 'logout':

            return login()

        else:

            print('invalid command')


menuString = 'Choose a command:\n"displayall" displays all bundles and information\n"display ["min" or "max"] [attribute] [quantity] displays all bundles with an attribute -- tot, wa, ha, wg, hg -- with the minimum or maximum quantity. Add a % to the end of the attribute for the % total of that attribute. Parameters should be space seperated.\n"add [name]" to add a bundle with name to disablelist\n"remove [name]" to remove a bundle with name from disablelist.\n"list" to display your disablelist information.\n"quit" to quit the program.\n"clear" to clear the disablelist.\n"logout" to logout\n"delete" to delete your account.\n"help" to repeat this menu.'
#first, get them to login.
def login():

    global accounts

    while True:
        
        cmd = input("Login, Signup, Reset, or Quit? ").lower()
        clear()

        if cmd == 'login':

            while True:

                inp = input("Enter Username or quit ")
                clear()

                if inp.lower() == 'quit':
                    break

                else:

                    username = inp

                    if username in accounts:

                        password = input("Enter password or quit ")
                        clear()

                        if password == 'quit':

                            break
                        
                        else:

                            if accounts[username]['pass'] == password:

                                print('login successful')
                                print(menuString)
                                return main(username)

                            else:

                                print('invalid password')

                    else:
                        print('invalid username')

        elif cmd == 'signup':
            
            while True:

                inp = input('Enter unique username or quit ')
                clear()

                if inp.lower() == 'quit':
                    break

                elif inp not in accounts:

                    username = inp
                    password = input('Enter password or quit ')
                    clear()

                    if password == 'quit':

                        break
                    
                    else:

                        accounts[username] = {
                            'pass': password,
                            'dl': {
                                "list": {},
                                "tot": 0,
                                "wa": 0,
                                "ha": 0,
                                "wg": 0,
                                "hg": 0
                            }
                        }
                        print('account creation successful')
                        print(menuString)
                        return main(username)

                else:

                    print('username already in use')

        elif cmd == 'reset':

            while True: 

                answer = input('Are you sure you want to reset? This will delete everyone\'s account information. Y/N ').lower()
                clear()

                if answer == 'y' or answer == 'yes':

                    accounts = {}
                    print('accounts have been reset')
                    break
                
                elif answer == 'n' or answer == 'no':

                    break

                else:

                    print('YES OR NO')
        
        elif cmd == 'quit':

            break

        else:

            print('invalid command, try again')

login()
aFile = open('accounts.txt', 'w', encoding  = 'utf8')
aFile.write(json.dumps(accounts))
aFile.close()