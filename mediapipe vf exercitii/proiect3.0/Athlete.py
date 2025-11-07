class Athlete():
    def __init__(self, firstName, secondName, age, gender, height, weight):
        self.firstName = firstName
        self.secondName = secondName
        self.age = int(age)
        self.gender = gender
        self.height = float(height)
        self.weight = float(weight)

    def __str__(self):
        return f"{self.firstName} {self.secondName}, {self.age} ani, {self.gender}, {self.height} m, {self.weight} kg"
