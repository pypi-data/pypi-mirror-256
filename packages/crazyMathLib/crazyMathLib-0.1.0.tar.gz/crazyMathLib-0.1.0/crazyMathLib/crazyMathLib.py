class TwoNumberMath:
    def __init__(self, firstNum, secondNum) -> None:
        self.firstNum = firstNum
        self.secondNum = secondNum
    def add(self):
        return self.firstNum + self.secondNum
    def subtract(self):
        if self.firstNum > self.secondNum:
            return self.firstNum - self.secondNum
        else:
            return self.secondNum - self.firstNum
    def multiply(self):
        return self.firstNum * self.secondNum
    def divide(self):
        return self.firstNum / self.secondNum
