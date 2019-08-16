with open("eg_cleaning.py", 'r') as infile:
    hw = infile.readlines().replace(chr(0), '')