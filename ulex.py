from ugen import xucc
import os


root = 'C:\Users\colin_000\Documents\GitHub\DarkestHour/DH_Weapons/Classes'

for filename in os.listdir(root):
    print filename
    xucc.compile(open(os.path.join(root, filename)).read())

# xucc.compile(open(os.path.join(root, 'DHBot.uc')).read())
# xucc.compile(open('src/TestPackage/DarkestHourGame.uc').read())
# xucc.compile(open('src/TestPackage/TestClass.uc').read())
