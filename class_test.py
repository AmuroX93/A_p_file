class Mobile_suits():
    def __init__(self,name,cost):
        self.name=name
        self.cost=cost
    def shoot(self):
        print(f"{self.name} is now shooting")
    def defend(self):
        print(f"{self.name} is now defending")

Gundam=Mobile_suits('gundam',2000)
print(Gundam.name)
Gundam.shoot()
Gundam.defend()