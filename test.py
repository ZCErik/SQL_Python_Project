f = open('eg_cleaning.py')
for l in f.readlines():
  print (l.replace("\0", ''))