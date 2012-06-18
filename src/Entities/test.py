'''
Created on 2012-6-4

@author: Sky
'''
a = []
a.append("11")
a.append("22")
print("11" in a)

b = {}
b["12"] = "23"
b["34"] = "45"
for i in b.values():
    del i
print(b["34"])