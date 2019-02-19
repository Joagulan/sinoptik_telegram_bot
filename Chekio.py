time = '12:30'
a = int(time[0]+time[1])
b = int(time[3]+time[4])
if a == 12:
    print(f'{a}:{b} p.m.')
elif a > 12:
    print(a)
