from calculator_logic import CalculatorLogic

calc = CalculatorLogic(angle_mode="DEG")

tests = [
    "2+3*5",
    "2^8",
    "sqrt(64)",
    "root(27,3)",
    "sin(30)",
    "log(100)",
    "log(8,2)",
    "ln(e)",
    "1/0",
    "tan(90)",
    "fact(5)",
    "nPr(5,2)",
    "nCr(5,2)",
    "exp(2)"
]

for t in tests:
    print(t, "=>", calc.evaluate(t))
