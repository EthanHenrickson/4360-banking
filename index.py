from tinydb import TinyDB, Query

class Bank:
    def __init__(self):
        self.db = TinyDB('db.json')

    def locked(self,username):
        return self.db.search(Query().username == username)[0]['locked']

    def transferBalance(self, fromUsername, toUsername, amount):
        user1data = self.db.search(Query().username == fromUsername)
        user2data = self.db.search(Query().username == toUsername)

        if(len(user1data) and len(user2data)):
            user1amount = user1data[0]['balance']
            user2amount = user2data[0]['balance']

            if(user1data[0]['balance'] < amount or amount < 0):
                return "Can't transfer more than you have"
            self.db.update({"balance": user1amount - amount}, Query().username == fromUsername)
            self.db.update({"balance": user2amount + amount}, Query().username == toUsername)
            return f"Success, ${amount:.2f} was transferred to {toUsername}"
        else:
            return "That user does not exist"    

    def getBalance(self, username):
        data = self.db.search(Query().username == username)
        locked = self.locked(username)

        if(locked):
            return "Sorry, your account is locked, unlock it first with the 'unlock account' command"

        return f"Your current balance is {data[0]['balance']:.2f}"

    def removeBalance(self, username, amount):
        data = self.db.search(Query().username == username)
        prevAmount = data[0]["balance"]
        locked = self.locked(username)

        if(locked):
            return "Sorry, your account is locked, unlock it first with the 'unlock account' command"

        if(prevAmount < amount):
            return f"You can't withdraw more than {prevAmount:.2f}"
            
        if(amount < 0):
            return "Sorry, you cant withdraw negative amounts"
        self.db.update({"balance": prevAmount - amount}, Query().username == username)
        return f"Success, ${amount:.2f} has been removed to your account. You account balance is now ${prevAmount - amount:.2f} \n"

    def addBalance(self, username, amount):
        data = self.db.search(Query().username == username)
        prevAmount = data[0]["balance"]
        locked = self.locked(username)

        if(locked):
            return "Sorry, your account is locked, unlock it first with the 'unlock account' command"

        if(amount < 0):
            return "Sorry, you cant deposit negative amounts"
        self.db.update({"balance": amount + prevAmount}, Query().username == username)
        return f"Success, ${amount:.2f} has been added to your account. Your account balance is now ${amount + prevAmount:.2f} \n"

    def addUser(self, name, username, password, initBalance):
        self.db.insert({'name': name,'username':username,'password':password, 'balance': initBalance, 'locked':False})
        return f"User {name} created."

    def lockAccount(self, username, password):
        data = self.db.search(Query().username == username)

        if(data[0]["password"] == password):
            self.db.update({"locked": True}, Query().username == username)
            return "Success"
        else:
            return "Error, wrong password"
    
    def unlockAccount(self, username, password):
        data = self.db.search(Query().username == username)

        if(data[0]["password"] == password):
            self.db.update({"locked": False}, Query().username == username)
            return "Success"
        else:
            return "Error, wrong password"

        
    def login(self, username, password):
        data = self.db.search(Query().username == username)

        if(len(data) == 0) or data[0]["password"] != password:
            print("Incorrect username or password")
            return False

        print("Successful login")
        return True

def main():
    csbank = Bank()
    global username
    username = ""
    loginAttempt = 0
    transferAttempt = 0

    baseHelp = f"""
Welcome to the Bank! Please login or create an account to continue.
Commands -
    type 'login' or 'l' to login to your account
    type 'create account' or 'ca' to create an account
                """
    
    accountHelp = f"""
Commands -
    type 'transfer' or 't' to transfer money to another users account
    type 'deposit' or 'd' to deposit money to your account
    type 'withdraw' or 'w' to withdraw money from your account
    type 'get balance' or 'gb' to check your account balance
    type 'lock account' or 'la' to lock all payments too and from your account
    type 'unlock account' or 'ua' to unlock your account
    type 'log out' or 'lo' to log out of your account
    type 'exit' or e to quit the bank app
    """


    print(baseHelp)

    while True:

        if(loginAttempt == 3):
            print("Sorry, that was 3 failed log in attempts. Try again later")
            break

        if(transferAttempt == 3):
            print("Sorry, that was 3 failed transfer attempts. Try again later")
            break

        userInput = input("> ").lower()

        if(username == ""):
            if(userInput == "login" or userInput == "l"):
                usernameInput = input("Enter your username: ")
                passwordInput = input("Enter your password: ")
                if (csbank.login(usernameInput, passwordInput)):
                    username = usernameInput
                    print("Welcome back!")
                    print(accountHelp)
                else:
                    loginAttempt += 1
                    print(f"You have {3 - loginAttempt} attempts left. Create an account if you dont have one.")

            elif(userInput == "create account" or userInput == "ca"):
                    responseName = input("Enter name: ")
                    responseUsername = input("Enter username: ")
                    responsePass = input("Enter Password: ")
                    responseBalanced = float(input("Enter Initial Balance: "))
                    print(csbank.addUser(responseName, responseUsername, responsePass, responseBalanced))

            elif(userInput == "help" or userInput == "h"):
                print(baseHelp)

            else:
                print("Sorry, I dont believe that is a valid command. Type 'help' or 'h' for assistance.")
        
        else:
            if(userInput == "deposit" or userInput == 'd'):
                response = float(input("Enter amount to deposit in your account: "))
                print(csbank.addBalance(username, response))
            
            elif(userInput == "withdraw" or userInput == "w"):
                response = float(input("Enter amount to withdraw from your account: "))
                print(csbank.removeBalance(username, response))

            elif(userInput == "transfer" or userInput == "t"):
                responseUsername2 = input("Enter the username of the account you want too transfer money too: ")
                responseAmount = float(input("Enter the amount to transfer: "))

                response = csbank.transferBalance(username, responseUsername2, responseAmount)
                if(response == "That user does not exist"):
                    transferAttempt += 1
                    print(f"Invalid account, {3 - transferAttempt} attempts remaining")

                elif(response == "Can't transfer more than you have"):
                    transferAttempt += 1
                    print(f"Money error, invalid number or more than you have in your account, {3 - transferAttempt} attempts remaining")

                else:
                    print(response)

            elif(userInput == "get balance" or userInput == "gb"):
                print(csbank.getBalance(username))

            elif(userInput == "lock account" or userInput == "la"):
                response = input("Enter password to confirm: ")
                print(csbank.lockAccount(username, response))

            elif(userInput == "unlock account" or userInput == "ua"):
                response = input("Enter password to confirm: ")
                print(csbank.unlockAccount(username, response))
            
            elif(userInput == "log out" or userInput == "lo"):
                username = ""
                print("You've been logged out. See you soon!")

            elif(userInput == "help" or userInput == "h"):
                print(accountHelp)

            elif(userInput == "exit" or userInput == "e"):
                print("Goodbye!")
                break

            else:
                print("Sorry, I dont believe that is a valid command. Type 'help' for assistance.")

main()
