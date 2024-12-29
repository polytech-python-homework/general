import math

class Quaternion:
    def __init__(self, a=0, b=0, c=0, d=0):
        '''q = a + bi + cj + dk'''
        self.a = a  # a
        self.b = b  # bi
        self.c = c  # cj
        self.d = d  # dk

    def __add__(self, other):
        '''Сложение кватернионов'''
        return Quaternion(self.a + other.a, 
                          self.b + other.b, 
                          self.c + other.c, 
                          self.d + other.d)

    def __sub__(self, other):
        '''Вычитание кватернионов'''
        return Quaternion(self.a - other.a, self.b - other.b, self.c - other.c, self.d - other.d)

    def __mul__(self, other):
        '''Умножение кватернионов некоммутативно'''
        if type(other) is Quaternion:
            # i^2=j^2=k^2=ijk=−1
            # ij=k
            # ji=−k
            # ki = j
            # ik = -j
            # jk = i
            # kj = -i
            a = self.a * other.a - self.b * other.b - self.c * other.c - self.d * other.d
            b = self.a * other.b + self.b * other.a + self.c * other.d - self.d * other.c
            c = self.a * other.c - self.b * other.d + self.c * other.a + self.d * other.b
            d = self.a * other.d + self.b * other.c - self.c * other.b + self.d * other.a
            return Quaternion(a, b, c, d)
        elif type(other) in (float, int):
            return Quaternion(other * self.a, other * self.b, other * self.c, other * self.d)
        else:
            raise TypeError("Type multiple operator with Quaternion in (Quaternion, float, int)")

    def norm(self):
        '''Вычисление нормы'''
        return math.sqrt(self.a**2 + self.b**2 + self.c**2 + self.d**2)

    def conjugate(self):
        '''Сопряженный кватернион'''
        return Quaternion(self.a, -self.b, -self.c, -self.d)

    def inverse(self):
        '''Обратный кватеорнион'''
        norm_sq = self.norm() ** 2
        if norm_sq == 0:
            raise ZeroDivisionError("Cannot invert a quaternion with zero norm.")
        return   self.conjugate() * (1.0 / norm_sq)

    def __repr__(self):
        return f"Quaternion({self.a}, {self.b}, {self.c}, {self.d})"


    def to_rotation_matrix(self):
        """Преобразование кватерниона в матрицу вращения 3x3."""
        a, b, c, d = self.a, self.b, self.c, self.d
        return [
            [1 - 2 * (c**2 + d**2), 2 * (b * c - a * d), 2 * (b * d + a * c)],
            [2 * (b * c + a * d), 1 - 2 * (b**2 + d**2), 2 * (c * d - a * b)],
            [2 * (b * d - a * c), 2 * (c * d + a * b), 1 - 2 * (b**2 + c**2)]
        ]
    
    @staticmethod
    def from_axis_angle(axis, angle):
        """Создание кватерниона из оси и угла вращения."""
        half_angle = angle / 2.0
        s = math.sin(half_angle)
        return Quaternion(math.cos(half_angle), axis[0] * s, axis[1] * s, axis[2] * s)

# Пример использования
q1 = Quaternion(1, 2, 3, 4)
q2 = Quaternion(2, 4, 6, 8)

# Сложение
q_sum = q1 + q2
print("Сумма:", q_sum)

# Умножение
q_product = q1 * q2
print("Произведение:", q_product)

# Норма
print("Норма q1:", q1.norm())

# Обратный кватернион
print("Обратный q1:", q1.inverse())

# Кватернион из оси и угла
axis = [0, 0, 1]  # Ось Z
angle = math.pi / 4  # 45 градусов
q_rotation = Quaternion.from_axis_angle(axis, angle)
print("Кватернион вращения:", q_rotation)

# Матрица вращения
rotation_matrix = q_rotation.to_rotation_matrix()
print("Матрица вращения:")
for elem in rotation_matrix:
    print(elem)

