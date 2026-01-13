import math
import re

class CalculatorLogic:
    """
    Scientific Calculator Logic (Safe Evaluator)

    Features:
    - Safe math expression evaluation
    - sin, cos, tan in DEG/RAD mode
    - ln, log (base10), log(x, base)
    - sqrt, root(x, n)
    - power operator: ^ (converted to **)
    - constants: pi, e
    - history tracking
    """

    def __init__(self, angle_mode="DEG"):
        self.angle_mode = angle_mode  # "DEG" or "RAD"
        self.history = []

    # -------------------------
    # Utility / Settings
    # -------------------------

    def set_angle_mode(self, mode: str):
        mode = mode.upper().strip()
        if mode not in ("DEG", "RAD"):
            raise ValueError("Angle mode must be 'DEG' or 'RAD'")
        self.angle_mode = mode

    def clear_history(self):
        self.history.clear()

    def get_history(self):
        return list(self.history)

    # -------------------------
    # Internal Helpers
    # -------------------------

    def _to_radians(self, x: float) -> float:
        if self.angle_mode == "DEG":
            return math.radians(x)
        return x

    def _format_result(self, result):
        """
        Format output for display:
        - int-like floats -> int
        - trim long floats
        """
        if isinstance(result, float):
            if result.is_integer():
                return str(int(result))
            return f"{result:.12g}"
        return str(result)

    def _preprocess(self, expr: str) -> str:
        """
        Make expression user-friendly:
        - Replace '^' with '**'
        - Allow '×' and '÷'
        - Remove extra spaces
        - Fix common typing like 'sin 30' -> 'sin(30)' is NOT done automatically,
          because it can create wrong parses. Keep strict.
        """
        expr = expr.strip()

        expr = expr.replace("×", "*")
        expr = expr.replace("÷", "/")
        expr = expr.replace("^", "**")

        # Optional: block weird characters early
        # Allowed basic chars: digits, operators, parentheses, dot, comma, letters, underscore, spaces
        if not re.fullmatch(r"[0-9a-zA-Z_+\-*/%.(),\s]*", expr):
            return "__INVALID_CHARS__"

        return expr

    # -------------------------
    # Allowed math functions
    # -------------------------
    def _sin(self, x): return math.sin(self._to_radians(float(x)))
    def _cos(self, x): return math.cos(self._to_radians(float(x)))

    def _tan(self, x):
        angle = float(x)
        if self.angle_mode == "DEG":
            # tan undefined at 90 + k*180
            if abs((angle % 180) - 90) < 1e-12:
                raise ValueError("Domain Error")
        else:
            # RAD mode: undefined at pi/2 + k*pi
            if abs((angle - (math.pi / 2)) % math.pi) < 1e-12:
                raise ValueError("Domain Error")
        return math.tan(self._to_radians(angle))

    def _ln(self, x):
        x = float(x)
        if x <= 0:
            raise ValueError("Domain Error")
        return math.log(x)

    def _log10(self, x):
        x = float(x)
        if x <= 0:
            raise ValueError("Domain Error")
        return math.log10(x)

    def _log(self, x, base=10):
        """
        log(x) -> base 10 by default
        log(x, base) supported
        """
        x = float(x)
        base = float(base)
        if x <= 0 or base <= 0 or base == 1:
            raise ValueError("Domain Error")
        return math.log(x, base)

    def _sqrt(self, x):
        x = float(x)
        if x < 0:
            raise ValueError("Complex Result")
        return math.sqrt(x)

    def _root(self, x, n=2):
        """
        root(x, n) = nth root
        - supports negative x only for odd n (real root)
        """
        x = float(x)
        n = int(n)

        if n <= 0:
            raise ValueError("Invalid Root")

        if x < 0:
            if n % 2 == 0:
                raise ValueError("Complex Result")
            return -((-x) ** (1 / n))

        return x ** (1 / n)
    
    def _fact(self, n):
        n = float(n)
        if not n.is_integer():
            raise ValueError("Factorial needs integer")
        n = int(n)
        if n < 0:
            raise ValueError("Domain Error")
        return math.factorial(n)

    def _npr(self, n, r):
        n = float(n)
        r = float(r)
        if not n.is_integer() or not r.is_integer():
            raise ValueError("nPr needs integers")
        n, r = int(n), int(r)
        if n < 0 or r < 0 or r > n:
            raise ValueError("Domain Error")
        return math.factorial(n) // math.factorial(n - r)

    def _ncr(self, n, r):
        n = float(n)
        r = float(r)
        if not n.is_integer() or not r.is_integer():
            raise ValueError("nCr needs integers")
        n, r = int(n), int(r)
        if n < 0 or r < 0 or r > n:
            raise ValueError("Domain Error")
        return math.comb(n, r)


    # -------------------------
    # Safe Evaluation Core
    # -------------------------
    def evaluate(self, expression: str) -> str:
        """
        Evaluate the user expression safely.

        Returns:
        - formatted result as string
        - or an error message
        """
        expr = self._preprocess(expression)

        if expr == "":
            return ""

        if expr == "__INVALID_CHARS__":
            return "Error: Invalid Characters"

        # Safe environment: only what we allow
        safe_env = {
            "__builtins__": None,  # blocks dangerous builtins
            # constants
            "pi": math.pi,
            "e": math.e,

            # arithmetic helpers
            "abs": abs,
            "round": round,
            "pow": pow,

            # trig
            "sin": self._sin,
            "cos": self._cos,
            "tan": self._tan,

            # logs
            "ln": self._ln,
            "log": self._log,     # supports log(x) and log(x, base)
            "log10": self._log10, # optional explicit base10

            # roots
            "sqrt": self._sqrt,
            "root": self._root,

            # factorials
            "fact": self._fact,
            "nPr": self._npr,
            "nCr": self._ncr,
            "exp": math.exp,

        }

        try:
            # Evaluate expression safely
            result = eval(expr, safe_env, {})

            # Save history
            self.history.append((expression, result))

            return self._format_result(result)

        except ZeroDivisionError:
            return "Error: Division by Zero"
        except ValueError as ve:
            # We raise ValueError("Domain Error") etc.
            return str(ve)
        except SyntaxError:
            return "Error: Invalid Expression"
        except TypeError:
            return "Error: Invalid Expression"
        except Exception:
            return "Error: Invalid Expression"
