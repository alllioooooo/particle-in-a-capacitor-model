import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.constants import e, m_e
from scipy.optimize import fsolve

# Данные конденсатора и электрона
r = 7.5e-2  # Внутренний радиус конденсатора (м)
R = 16e-2  # Внешний радиус конденсатора (м)
V = 2e6  # Начальная скорость электрона (м/с)
L = 24e-2  # Длина конденсатора (м)

# Время пролета электрона через конденсатор
t_flight = L / V

# Функция для нахождения минимальной разности потенциалов
def find_min_voltage(U):
    E = U / (R - r)  # Электрическое поле
    a_y = e * E / m_e  # Ускорение в радиальном направлении
    y_displacement = 0.5 * a_y * t_flight**2  # Радиальное перемещение
    return y_displacement - (R - r)

# Использование fsolve для нахождения минимальной разности потенциалов
initial_guess = 1e5  # Начальное предположение для разности потенциалов
min_voltage = fsolve(find_min_voltage, initial_guess)[0]  # Минимальная разность потенциалов

# Расчёт минимального электрического поля, используя min_voltage
E_min = min_voltage / (R - r)

# Функция для расчета изменяющегося электрического поля
def E_field(y):
    return E_min * (-1 - y / (R - r))

# Начальные условия
initial_conditions = [0, 0]  # y и Vy в начальный момент времени

# Уравнение движения электрона в конденсаторе с изменяющимся полем
def motion(t, y):
    dy = y[1]
    dvy = e * E_field(y[0]) / m_e
    return [dy, dvy]

# Временной интервал интегрирования (пока электрон внутри конденсатора)
t_eval = np.linspace(0, L / V, num=1000)

# Решение уравнения движения
sol = solve_ivp(motion, [0, L / V], initial_conditions, t_eval=t_eval)

# Расчет ускорения в каждый момент времени
ay = e * np.array([E_field(y) for y in sol.y[0]]) / m_e

# Построение графиков
plt.figure(figsize=(14, 10))

# y(x)
plt.subplot(2, 2, 1)
plt.plot(V * sol.t, sol.y[0])
plt.title('y(x)')
plt.xlabel('x (m)')
plt.ylabel('y (m)')

# Vy(t)
plt.subplot(2, 2, 2)
plt.plot(sol.t, sol.y[1])
plt.title('Vy(t)')
plt.xlabel('Time (s)')
plt.ylabel('Vy (m/s)')

# ay(t)
plt.subplot(2, 2, 3)
plt.plot(sol.t, ay)
plt.title('ay(t)')
plt.xlabel('Time (s)')
plt.ylabel('ay (m/s²)')

# y(t)
plt.subplot(2, 2, 4)
plt.plot(sol.t, sol.y[0])
plt.title('y(t)')
plt.xlabel('Time (s)')
plt.ylabel('y (m)')

plt.tight_layout()
plt.show()
