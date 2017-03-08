from ugen import xucc


root = 'C:\Users\colin_000\Documents\GitHub\DarkestHour/DH_Engine/Classes'

# for filename in os.listdir(root):
#     xucc.compile(open(os.path.join(root, filename)).read())

# xucc.compile(open(os.path.join(root, 'DHAntiVehicleProjectile.uc')).read())
# xucc.compile(open('src/TestPackage/DarkestHourGame.uc').read())
xucc.compile(open('src/TestPackage/TestClass.uc').read())
