from cisc108 import assert_equal

class CaloricBalance:
    '''
    Constructor takes in 4 parameters:
        - gender(string)
        - age(float)
        - height(float)
        - weight(float)
    Should store weight as a datamember and initialize balance
    as the negative value of the getBMR method. Cannot test
    until getBMR method is made.
    '''
    def __init__(self, gender, age, height, weight):
        self.gender = gender
        self.age = age
        self.height = height
        self.weight = weight
        self.balance = -1 * float((self.getBMR(gender, age, height, weight)))
    '''
    Method takes in 4 parameters:
        - gender(string)
        - age(float)
        - height(float)
        - weight(float)
    It should calculate and return the BMR using the
    calculations given. If the gender != to 'm' or 'f' then it
    returns 0.0
    '''
    def getBMR(self, gender, age, height, weight):
        if gender == 'f':
            bmr = 655 + (4.7 * float(self.height)) + (4.35 * float(self.weight)) - (4.7 * float(self.age))
            return bmr
        elif gender == 'm':
            bmr = 66 + (12.7 * float(self.height)) + (6.23 * float(self.weight)) - (6.8 * float(self.age))
            return bmr
        else:
            return 0.0
    '''
    This method receives no additional parameters and returns
    the value of the balance datamember.
    '''
    def getBalance(self):
        balance = self.balance
        return balance

    def recordActivity(self, cb_per_lb_per_min, minutes):
        num_cal_burned = cb_per_lb_per_min * self.weight
        total_cal_burn = num_cal_burned * float(minutes)
        self.balance -= total_cal_burn
        
    def eatFood(self, calories):
        self.calories = calories
        self.balance += calories