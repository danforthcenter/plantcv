import numpy as np
combined_matrix = np.arange(1, 50).reshape(7, 7)


_, t_r, t_g, t_b, s_r, s_g, s_b = np.split(combined_matrix, 7, 1)

t_r2 = combined_matrix[:, 1].reshape(-1, 1)
t_g2 = combined_matrix[:, 2].reshape(-1, 1)

print(combined_matrix)
print(t_r)
print(t_r2)
print(t_g)
print(t_g2)