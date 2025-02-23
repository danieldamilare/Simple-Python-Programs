import random
import math

def same_date(num_people, num_same):
    possible_dates = range(366)
    birthdays = [0] * 366
    for p in range(num_people):
        birth_date = random.choice(possible_dates)
        birthdays[birth_date] += 1
    return max(birthdays) >= num_same

def birthday_problem(num_people, num_same, num_trials):
    num_hits = 0
    for i in range(num_trials):
        if same_date(num_people, num_same):
            num_hits +=1
    return num_hits/num_trials

def run_sim_birthday(num_trials_list, numtrial):
    for people in num_trials_list:
        print(f"For {people} people est. prob. of a shared birthday is",
              birthday_problem(people, 2, numtrial))
        numerator = math.factorial(366)
        denom = (366**people) * math.factorial(366-people)
        print(f'Actual probability for {people} people is ', 1 -numerator/denom)

def run_sim_die(goal, num_trials, txt):
    total = 0
    for i in range(num_trials):
        result = ''
        for j in range(len(goal)):
            result += str(roll_die())
            if result == goal:
                total += 1
    print(f"Actual probality of {txt} = {round(1/(6**len(goal)), 8)}")
    est_probability = round(total/num_trials, 8)
    print(f"Estimated probablility of {txt} = {est_probability}")

def roll_die():
    return random.randrange(1, 6)

if __name__ == "__main__":
    # run_sim_die('11111', 100000, '11111')
    run_sim_birthday([10, 20, 40, 100], 10000)
