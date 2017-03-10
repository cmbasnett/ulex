from ugen import xucc
import os


root = 'C:/Users/colin_000/Documents/GitHub/DarkestHour/UCore/Classes'

# for filename in filter(lambda x: x.endswith('.uc'), os.listdir(root)):
#     print 'Parsing ' + filename
#     xucc.compile(open(os.path.join(root, filename)).read())

xucc.compile(open(os.path.join(root, 'TreeMap.uc')).read())
