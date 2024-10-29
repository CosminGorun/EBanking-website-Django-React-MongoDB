class Person:
    def __init__(self, name, ages, gender):
        self.name = name
        self.ages = ages
        self.gender = gender

    def toDic(self):
        return {"name": self.name, "ages": self.ages, "gender": self.gender}
