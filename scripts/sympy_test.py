import sympy as sym
import time
# from matrices_and_parameters import dx, dy
# dx = sym.Rational(1, 2)
# dy = sym.Rational(1, 2)

a1, a2, a3, h, tau, dx, dy = sym.symbols('a1, a2, a3, h, tau, dx, dy')
Ah = sym.Matrix([[-dx*h, 0, a1*h,  0],
                [0, -dy*h, a2*h,  0],
                [0,    0,    0,    h],
                [0,    0,    0, a3*h]])

Ath = sym.Matrix([[-dx*(tau-h), 0, a1*(tau-h),  0],
                [0, -dy*(tau-h), a2*(tau-h),    0],
                [0,    0,        0,           (tau-h)],
                [0,    0,        0,        a3*(tau-h)]])

eAh = sym.exp(Ah)

print eAh
# int = sym.integrate(sym.exp(Ath), (tau, 0, h))
#
# print int

# print Ah.exp()
# print '-------'
# print sym.simplify(A.exp())
