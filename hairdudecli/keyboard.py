"""

 ___________________________________
|                                   |
| You selected:     keep it? (y/n)  |
|  bullshit.txt                     |
|                                   |
| Files selected                    |
|   other.txt, fold1/mud.dat        |
|___________________________________|

"""

print(" "+"_"*96)
msg = f" "
title = "You selected:"
print(f"|{msg:96s}|")
print(f"|{msg:96s}|")
print(f"|{msg:96s}|")
print(f"|{title:^96s}|")
print(f"|{msg:96s}|")
print(f"|{msg:96s}|")
print(f"|{msg:96s}|")
print(f"|{msg:96s}|")
print(f"|{msg:96s}|")
print(f"|{msg:96s}|")
print(f"|{msg:96s}|")
print("|"+ "_"*96 +"|")

p = [1,2,3,4,5,6,7,8,9]
count = 1
for num in p:
    print(count)
    if num % 2 == 0:
        count -= 1
        p.remove(num)
        continue
    count += 1