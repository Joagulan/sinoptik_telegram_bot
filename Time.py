import datetime

d = datetime.datetime.now().strftime("%H:%M:%S")
if d == '22:21:10':
    print('yes')
else:
    print('no')