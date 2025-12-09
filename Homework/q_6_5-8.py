class Element():
    def __init__(self,name,symbol,number):
        self.__name=name
        self.__symbol=symbol
        self.__number=number
    @property
    def name(self):
        print('inside the getter')
        return self.__name
    @name.setter
    def name(self,name):
        print('inside the setter')
        self.__name=name
    def __str__(self):
        return self.__name+' '+self.__symbol+' '+self.__number
#打印1
#    def dump(self):
#        print("This element's name is ",self.name,'\nsymbol is ',\
#              self.number,"\nnumber is ",self.symbol)

my_element={'name':'Hydrogen','symbol':'H','number':'1'}
hydrogen=Element(**my_element)
print(hydrogen.name)
#print(hydrogen)
#打印1
#hydrogen.dump()
#print(hydrogen.name,'\n',hydrogen.number,'\n',hydrogen.symbol)
