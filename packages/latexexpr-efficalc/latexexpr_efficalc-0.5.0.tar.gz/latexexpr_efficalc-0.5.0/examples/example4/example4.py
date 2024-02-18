import latexexpr_efficalc
import latexexpr_efficalc.sympy as lsympy

x = latexexpr_efficalc.Variable("x", None)
y = latexexpr_efficalc.Variable("y", None)
z = latexexpr_efficalc.Variable("z", None)
v1 = latexexpr_efficalc.Variable("v1", None)
v2 = latexexpr_efficalc.Variable("v2", None)
v3 = latexexpr_efficalc.Variable("v3", 1.23)
v4 = latexexpr_efficalc.Variable("v4", 4.56)


def printExpr(e1, e2=""):
    print("$$" + str(e1) + r"\ \ \ \ \ \ \ \ \ " + str(e2) + "$$\n")


# simplify
print("\n\nsimplify")
e1 = latexexpr_efficalc.Expression("e1", v1 + v1 + v2 + v3 + v2 + v3 - v4)
printExpr(e1, lsympy.simplify(e1))
printExpr(lsympy.simplify(e1))
e2 = latexexpr_efficalc.Expression(
    "e2", latexexpr_efficalc.sin(x) ** 2 + latexexpr_efficalc.cos(x) ** 2
)
printExpr(e2, lsympy.simplify(e2))
e3 = latexexpr_efficalc.Expression("e3", (x**3 + x**2 - x - 1) / (x**2 + 2 * x + 1))
printExpr(e3, lsympy.simplify(e3))

# expand
print("\n\nexpand")
e1 = latexexpr_efficalc.Expression("e1", (x + 1) ** 2)
printExpr(e1, lsympy.expand(e1, substituteFloats=True))
e2 = latexexpr_efficalc.Expression("e2", (x + 2) * (x - 3))
printExpr(e2, lsympy.expand(e2))
e3 = latexexpr_efficalc.Expression("e3", (x + 1) * (x - 2) - (x - 1) * x)
printExpr(e3, lsympy.expand(e3))

# factor
print("\n\nfactor")
e1 = latexexpr_efficalc.Expression("e1", x**3 - x**2 + x - 1)
printExpr(e1, lsympy.factor(e1))
e2 = latexexpr_efficalc.Expression("e2", x**2 * z + 4 * x * y * z + 4 * y**2 * z)
printExpr(e2, lsympy.factor(e2))

# collect
print("\n\ncollect")
e1 = latexexpr_efficalc.Expression("e1", x * y + x - 3 + 2 * x**2 - z * x**2 + x**3)
printExpr(e1, lsympy.collect(e1, x))

# cancel
print("\n\ncancel")
e1 = latexexpr_efficalc.Expression("e1", (x**2 + 2 * x + 1) / (x**2 + x))
printExpr(e1, lsympy.cancel(e1))
e2 = latexexpr_efficalc.Expression("e2", 1 / x + (3 * x / 2 - 2) / (x - 4))
printExpr(e2, lsympy.cancel(e2))
e3 = latexexpr_efficalc.Expression(
    "e3", (x * y**2 - 2 * x * y * z + x * z**2 + y**2 - 2 * y * z + z**2) / (x**2 - 1)
)
printExpr(e3, lsympy.cancel(e3))

# apart
print("\n\napart")
e1 = latexexpr_efficalc.Expression(
    "e1", (4 * x**3 + 21 * x**2 + 10 * x + 12) / (x**4 + 5 * x**3 + 5 * x**2 + 4 * x)
)
printExpr(e1, lsympy.apart(e1))
