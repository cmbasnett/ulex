from ugen import xucc
import os

root = 'C:\Users\colin_000\Documents\GitHub\DarkestHour/DH_Engine/Classes'

for filename in os.listdir(root):
    print filename
    xucc.compile(open(os.path.join(root, filename)).read())
    print 'done'

# xucc.compile(open(os.path.join(root, 'DHAntiVehicleProjectile.uc')).read())
# xucc.compile(open('src/TestPackage/TestClass.uc').read())
