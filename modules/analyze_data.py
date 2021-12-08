class AnalyzeData:
    region = 0

    salary = 0
    purchase_amount = []

    history_salary = [0]

    def __init(self, a):
        a = 1

    def overwrite(self):
        self.history_salary = [0]
        self.salary = 0
        self.purchase_amount = []

    def sell(self, money):
        if not self.purchase_amount == []:
            for i in self.purchase_amount:
                self.salary += (money - i)
            self.purchase_amount = []

        self.history_salary.append(self.salary)

    def buy(self, money):
        if self.purchase_amount == []:
            self.purchase_amount.append(money)

        self.history_salary.append(self.salary)

    def append(self):
        self.history_salary.append(self.history_salary[-1])

    def total(self):
        print(self.salary, self.purchase_amount)


