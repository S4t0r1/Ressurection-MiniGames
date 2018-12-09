
# this func finds out an approx square root of a number without using any special mathematical knowledge nor any math module
# as you can see at the bottom, it is less accurate than a google calc, thats why a MATH MODULE IN PYTHON IS VERY IMPORTANT !

# setting up approximity further in (num (- or +) 0.00...01) will fail the while loop as it will encounter its float limitations
# without a propper math module.. 
# the main idea behind this is to design a simple algorithm to solve a problem of this type
# ...no research..pure boredom


def getSqrt(num, div_by=1, increment=1):
    div_start = None
    while True:
        res = num / div_by
        if (num - 0.000000001) <= res**2 <= (num + 0.000000001):
            return float(str(res)[:str(res).index('.')+12])
        else:
            if res**2 > num:
                div_start = div_by
            else:
                increment = increment / 10
                div_by = div_start
        div_by += increment

for num in (6, 7, 8, 1.5):
    print(getSqrt(num))
print()

# GOOGLE CALC resuls for sqrt of 6; 7; 8, 1.5
# 2.44948974278
# 2.64575131106
# 2.82842712475
# 1.22474487139

# example comparison for the sqrt of 6
winner = 2.44948974278**2    #google calc result
winner2 = 2.44948974296**2   #this func result
winner3 = 2.449489742**2     # the & (=intersection) of decimal points from the above results

for num, candidate in zip([6 for i in range(3)], (winner, winner2, winner3)):
    print("total diff with num {} -> {}".format(num, (num - candidate if (candidate < num) else candidate - num)))
