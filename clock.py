


def get_clock(x, y):
    try:
        m = y/x
    except ZeroDivisionError:
        m=4
    if y > 0:
        if x > 0:
            quad = 1
        elif x <= 0:
            quad = 2

    elif y <= 0:
        if x < 0:
            quad = 3
        elif x >= 0:
            quad = 4

    if quad == 1 or quad == 4:
        if m >= 4:
            clock = 12
        elif 4>m>=1:
            clock = 1
        elif 1>m>=.25:
            clock = 2
        elif .25>m>=-.25:
            clock = 3
        elif -.25>m>=-1:
            clock = 4
        elif -1>m>=-4:
            clock = 5
        elif m<-4:
            clock = 6
    elif quad == 2 or quad == 3:
        if m < -4:
            clock = 12
        elif -4<=m<-1:
            clock = 11
        elif -1<=m<-.25:
            clock = 10
        elif -.25<=m<.25:
            clock =9
        elif .25<=m<1:
            clock = 8
        elif 1<=m<4:
            clock = 7
        elif m>=4:
            clock = 6
    else:
        print("your code is incorrect")
    
    clock = str(clock) + " o'clock"

    return clock


#t.speak(get_clock(x, y))
