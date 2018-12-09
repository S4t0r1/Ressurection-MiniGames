
# this func finds out an approx square root of a number without using any mathematical knowledge nor any math module
# as you can see at the bottom, it is less accurate than a google calc, thats why a MATH MODULE IN PYTHON IS VERY IMPORTANT !

# setting up approximity further in (num (- or +) 0.00...01) will fail the while loop as it will encounter its float limitations
# without a propper math module.. 
# the main idea behind this is to design a simple algorithm to solve a problem of this type
# ...no research..pure improvisation for the fun of it


def getSqrt(num, interval=['', ''], div_by=2, increment=1):
    while True:
        res = num / div_by
        if (num - 0.000000001) <= res**2 <= (num + 0.000000001):
            return str(res)[:str(res).index('.')+12]
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

for num in (6, 7, 8):
    print(getSqrt(num))
print()

# GOOGLE CALC resuls for sqrt of 6; 7; 8
# 2.44948974278
# 2.64575131106
# 2.82842712475

# example comparison for the sqrt of 6
winner = 2.44948974278**2    #google calc result
winner2 = 2.44948974296**2   #this func result
winner3 = 2.449489742**2     # the & (=intersection) of decimal points from the above results

for num, candidate in zip([6 for i in range(3)], (winner, winner2, winner3)):
    print("total diff with num {} -> {}".format(num, (num - candidate if candidate<6 else candidate - num)))
