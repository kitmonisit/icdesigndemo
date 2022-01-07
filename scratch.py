import sympy as sp

gm1, go1, CM, gm2, YL, s = sp.symbols("g_{m1} g_{o1} C_M g_{m2} Y_L s")
ro1, RL, GL, CL = sp.symbols("r_{o1} R_L G_L C_L")
w, f = sp.symbols(r'\omega f')

G_exact = sp.Matrix(
    [
        [0, 0, 0, 1],
        [-gm1, go1 + s * CM, -s * CM, 0],
        [0, gm2 - s * CM, YL + s * CM, 0],
        [1, 0, 0, 0],
    ]
)

I_vector = sp.Matrix([0, 0, 0, 1])

V_vector = G_exact.inv()*I_vector

gain = V_vector[2]


# \begin{align}
# \begin{bmatrix}
# i_i \\
# i_x \\
# i_o \\
# v_s
# \end{bmatrix}
# &=
# \begin{bmatrix}
      # 0 &             0 &        0 & 1 \\
# -g_{m1} & g_{o1} + sC_M &    -sC_M & 0 \\
      # 0 & g_{m2} - sC_M & Y_L+sC_M & 0 \\
      # 1 &             0 &        0 & 0
# \end{bmatrix}
# \begin{bmatrix}
# v_i \\
# v_x \\
# v_o \\
# i_s
# \end{bmatrix}
# \end{align}
