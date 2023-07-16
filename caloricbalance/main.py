from caloric_balance import CaloricBalance
import sys

'''
Function receives no parameters. Must return a list of strings
that contains the lines of the menu.
'''
def formatMenu():
    menu = ['What would you like to do?', '[f] Record Food Consumption', '[a] Record Physical Activity', '[q] Quit']
    return menu
'''
Function receives no parameters. Must return a string that
contains the prompt to ask the user which menu option they
would like to select.
'''
def formatMenuPrompt():
    prompt = "Enter an option: "
    return prompt
'''
Function does not receive any parameters. Must return a list of
strings that contains the lines of the activities menu.
'''
def formatActivityMenu():
    activities = ['Choose an activity to record', '[j] jogging', '[r] running', '[s] sitting', '[w] walking']
    return activities
'''
Function receives 1 parameter:
    - prompt(string that contains a prompt for input)
It must return a string that contains the text input by the
user, with whitespace removed. If user gives an empty string,
prompt them again until they give a non-empty string.
'''
def getUserString(prompt):
    response = ""
    while response == "":
        response = input(prompt)
        response = response.strip()
    return response
'''
Function receives 1 parameter:
    - prompt(string that contains a prompt for input)
It must return a float that contains the number input by the
user. If the user enters a non-number or a number <= 0 it
should prompt them again.
'''
def getUserFloat(prompt):
    while True:
        response = input(prompt)
        try:
            response = float(response)
            if response > 0:
                return response
            else:
                print("The number must be greater than 0.")
        except ValueError:
            print("You can't convert that string to a float")
'''
Function receives no parameters.
It will prompt the user for their gender(f/m), age(float/int),
their height in inches(float/int), and their weight in pounds
(float/int). It will creat an instance of CaloricBalance and
return that instance. You will need to import your
caloric_balance module.
'''
def createCaloricBalance():
    gender = getUserString("What is your gender (f or m)? ")
    age = getUserFloat("What is your age? ")
    height = getUserFloat("What is your height in inches? ")
    weight = getUserFloat("What is your weight in pounds? ")
    cb = CaloricBalance(gender, age, height, weight)
    return cb
    
'''
Receives 1 parameter:
    - instance of CaloricBalance class
Prints the activities menu and prompts the user to choose
an activity.
'''
def recordActivityAction(balance):
    for line in formatActivityMenu():
        print(line)
    response = getUserString(formatMenuPrompt())
    if response == 'j':
        minutes = getUserFloat("For how many minutes did you perform this activity?")
        balance.recordActivity(0.074, minutes)
        print("Awesome! Your caloric balance is now " + str(balance.getBalance()))
        return balance
    elif response == 'r':
        minutes = getUserFloat("For how many minutes did you perform this activity?")
        balance.recordActivity(0.087, minutes)
        print("Awesome! Your caloric balance is now", str(balance.getBalance()))
        return balance
    elif response == 's':
        minutes = getUserFloat("For how many minutes did you perform this activity?")
        balance.recordActivity(0.009, minutes)
        print("Awesome! Your caloric balance is now ", str(balance.getBalance()))
        return balance
    elif response == 'w':
        minutes = getUserFloat("For how many minutes did you perform this activity?")
        balance.recordActivity(0.036, minutes)
        print("Awesome! Your caloric balance is now ", str(balance.getBalance()))
        return balance
    else:
        print("please enter j, r, s, or w")
'''
Receives 1 parameter:
    - instance of CaloricBalance class
Prompts the user to enter the number of calories consumed. It
then calls the eatFood method on the instance. Lastly it should
print a success message to the user with their new caloric
balance.
'''
def eatFoodAction(balance):
    calories = getUserFloat("Okay! How many calories did you just eat? ")
    balance.eatFood(calories)
    print("Sweet! Your caloric balance is now ", str(balance.getBalance()))
    return balance
'''
Receives 1 parameter:
    - instance of CaloricBalance class
Function will display a message to the user indicating the end
of the program. It will then terminate the program using
sys.exit(0). Be sure to do the correct import statement. This
function does not return anything.
'''
def quitAction(balance):
    print("You have now reached the end of the program.")
    sys.exit(0)
'''
Receives 2 parameters:
    - instance of CaloricBalance class
    - response(string)
Function will call the appropriate action function based on
the choice string. If the choice string does not match any
accepted choices, it will display a message to the user.
This function doesn't return anything.
'''
def applyAction(balance, choice):
    if choice == 'f': #Record Food Consumption
        recorded = eatFoodAction()
        return recorded
    elif choice == 'a': #Record Physical Activity
        recorded = recordActivityAction()
        return recorded
    elif choice == 'q': #Quit
        return quitAction(balance)
    else:
        print("error")
'''
receives 0 parameters and returns nothing.
This function ties everything together. Creates an instance
of CaloricBalance, repeatedly asking the user their choice
and taking appropriate action.
'''
def main():
    print("Hi! This program will calculate your caloric balance for the day!")
    print("Before we can start, I need some information about you. Be honest! :)")
    balance = createCaloricBalance()
    print("Thanks! Now, throughout the day, tell me each time you eat or move.")
    print("Your caloric balance is starting at ", str(balance.getBalance()))
    print("(you need to eat something)")
    recordActivityAction(balance)
    
if __name__ == '__main__':
    main()
    







