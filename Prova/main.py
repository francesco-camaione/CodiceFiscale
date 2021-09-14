class Car:
    def __init__(self, name, brand, engine_power, hp):
        self.name = name
        self.brand = brand
        self.engine_power = engine_power
        self.hp = hp

    def bollo(self):
        return self.engine_power * self.hp


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    m3 = Car("M3", "BMW", 2.0, 170)
    print(f"Pagherai euro {m3.bollo()}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
