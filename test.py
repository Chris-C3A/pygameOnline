class Player:
    def __init__(self, name, age):
        self.cls = "Player"
        self.name = name
        self.age = age

    def __str__(self):
        return self.cls

p = Player("Chris", 16)

print(str(p))
