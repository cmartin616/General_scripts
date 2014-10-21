import time
import datetime

today= datetime.date.today()

version = raw_input("Enter the version number: ")
raw_input('Press enter to start.   ')
tic = time.time()
raw_input('Press enter to stop.   ')
toc = time.time()
s = toc-tic

m, s = divmod(s, 60)
h, m = divmod(m, 60)
timeFormat = "%d:%02d:%02d" % (h, m, s)


reconcileFile = r'c:/users/christopher.martin/desktop/rec_time.txt'
f = open(reconcileFile, 'a')
output = [version, ' - ', str(today),' - ',  str(timeFormat), ' to reconcile.\n']
f.write(''.join(output))
f.close
