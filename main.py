import pygame
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.constants import e, m_e

# Данные конденсатора и электрона
r = 7.5e-2  # Внутренний радиус конденсатора (м)
R = 16e-2  # Внешний радиус конденсатора (м)
V = 2e6  # Начальная скорость электрона (м/с)
L = 24e-2  # Длина конденсатора (м)

# Максимальное значение электрического поля
E_max = 5.78


# Функция для расчета изменяющегося электрического поля
def E_field(y):
    return E_max * (1 - y / (R - r))


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

# Визуализация движения частицы в конденсаторе на основе данных в виде рисунка с траекторией

# Параметры для рисования конденсатора
capacitor_length = L
capacitor_inner_radius = r
capacitor_outer_radius = R

# Создание фигуры для визуализации
plt.figure(figsize=(12, 6))

# Рисование конденсатора
cylinder_color = 'black'
plt.gca().add_patch(plt.Rectangle((0, -capacitor_inner_radius), capacitor_length, 2*capacitor_inner_radius,
                                  edgecolor=cylinder_color, fill=False, lw=2))
plt.gca().add_patch(plt.Rectangle((0, -capacitor_outer_radius), capacitor_length, 2*capacitor_outer_radius,
                                  edgecolor=cylinder_color, fill=False, lw=2, linestyle='dashed'))

# Рисование траектории частицы
particle_path_color = 'red'
plt.plot(V * sol.t, sol.y[0], color=particle_path_color, label='Trajectory of electron')

# Установка пределов отображения
plt.xlim(0, capacitor_length)
plt.ylim(-capacitor_outer_radius, capacitor_outer_radius)

# Настройка графика
plt.title('Visualization of Electron Movement in Capacitor')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.axhline(0, color='blue', lw=0.5)  # Ось x
plt.axvline(0, color='blue', lw=0.5)  # Ось y
plt.legend()

# Отображение графика
plt.show()

# Инициализация Pygame
pygame.init()

# Установка размеров окна
width, height = 600, 400
screen = pygame.display.set_mode((width, height))

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Преобразование координат электрона в пиксели
scale = width / L
electron_radius = 5  # Размер частицы в пикселях

# Основной цикл анимации
running = True
frame = 0
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.fill(WHITE)

    # Рисование конденсатора
    pygame.draw.rect(screen, BLACK, [0, height / 2 - r * scale, width, 2 * r * scale], 2)
    pygame.draw.rect(screen, BLACK, [0, height / 2 - R * scale, width, 2 * R * scale], 2)

    # Рисование электрона
    if frame < len(sol.t):
        x = V * sol.t[frame] * scale
        y = height / 2 + sol.y[0][frame] * scale
        pygame.draw.circle(screen, RED, (int(x), int(y)), electron_radius)

    # Обновление кадра
    pygame.display.flip()
    frame += 1

    # Задержка для контроля скорости анимации
    pygame.time.delay(10)

# Закрытие Pygame
pygame.quit()