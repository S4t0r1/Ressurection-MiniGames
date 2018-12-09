
# this func finds out an approx square root of a number without using any mathematical knowledge nor any math module
# as you can see at the bottom, it is less accurate than a google calc, thats why a MATH MODULE IN PYTHON IS VERY IMPORTANT !

# setting up approximity further in (num (- or +) 0.00...01) will fail the while loop as it will encounter its float limitations
# without a propper math module.. 
# the main idea behind this is to design a simple algorithm to solve a problem of this type
# ...no research..pure improvisation for the fun of it



def getSqrt(num):
    interval = ['', '']
    div_by = 2
    res = num / 2
    increment = 1
    while True:
        res = num / div_by
        if (num - 0.000000001) <= res**2 <= (num + 0.000000001):
            break
        else:
            if res**2 > num:
                interval[0] = div_by
            elif res**2 < num:
                interval[1] = div_by
        if all(x!='' for x in interval):
            increment = increment / 10
            div_by = interval[0] + increment
            interval = ['', '']
            continue
        div_by += increment
    return str(res)[:str(res).index('.')+12]


print(getSqrt(6))
print(getSqrt(7))
print(getSqrt(8))
# 2.44948974278
# 2.64575131106
# 2.82842712475

# example comparison on sqrt of 6, winner=Google calc., winner2=this func, winner3=result with the & decimalpoints of winner, winner2
winner = 2.44948974278**2 
winner2 = 2.44948974296**2
winner3 = 2.449489742**2
print()
print(6 - winner if winner<6 else winner - 6)
print(6 - winner2 if winner2<6 else winner2 - 6)
print(6 - winner3 if winner3<6 else winner3 - 6)


print("\n{}\n{}\n{}".format(winner, winner2, winner3))
