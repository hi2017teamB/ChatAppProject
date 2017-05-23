class Syntax:
    def __init__(self, span, days, time, in_lab, grade, item):
        self.span = span
        self.days = days
        self.time = time
        self.in_lab = in_lab
        self.grade = grade
        self.item = item

    def show_all(self):
        print(self.span)
        print(self.days)
        print(self.time)
        print(self.in_lab)
        print(self.grade)
        print(self.item)
