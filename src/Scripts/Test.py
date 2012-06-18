'''
Created on 2012-6-3

@author: Sky
'''
class A:
    def __init__(self):
        self.x = {}
        self.x["11"] = "22"
        self.x["33"] = "44"
    
    def __iter__(self):
        for i in self.x:
            yield i
            
    def __getitem__(self, index):
        return self.x[index]
            
a = A()
for i in a:
    print(a[i])
for i in a:
    print(i)
