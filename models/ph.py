from scipy.integrate import solve_ivp
from scipy.optimize import fsolve
from numpy import eye

# pH neutralization Model
# note to add ref

def pH_model(u, x0, t, ts):

    C = eye(4)

    pk1 = 6.35
    pk2 = 10.25

    x = x0
    q1, q2, q3 = u

    solution = solve_ivp(fun = pH, t_span=(t, t+ts), y0=x, method='RK45', args=(q1, q2, q3), dense_output=True)
    x = solution.y[:, -1]

    y = C@x

    func = lambda pH_in :  y[1] + 10**(pH_in - 14) + y[2]*((1 + 2*10**(pH_in - pk2))/(1 + 10**(pk1-pH_in) + 10**(pH_in-pk2))) - 10**(-pH_in)
    pH_out = fsolve(func, x0=y[-1])

    y[-1] = pH_out
    
    return pH_out, x

def pH(t, y, q1, q2, q3):

    A = 207
    Cv = 8.75

    wa1 = 3e-3
    wa2 = -3e-2
    wa3 = -3.05e-3

    wb1 = 0
    wb2 = 3e-2
    wb3 = 5e-5

    h, wa4, wb4, pH_out = y

    dh = 1/A * (q1 + q2 + q3 - Cv*(h**0.5))
    dwa4 = 1/(A*h) * ((wa1 - wa4)*q1 + (wa2-wa4)*q2 + (wa3-wa4)*q3)
    dwb4 = 1/(A*h) * ((wb1 - wb4)*q1 + (wb2-wb4)*q2 + (wb3-wb4)*q3)

    return dh, dwa4, dwb4, pH_out



