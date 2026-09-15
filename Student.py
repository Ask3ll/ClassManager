import json

import MainWindow


class Student:
    def __init__(self, _window, name, _id, sex, friends=None, prefers=None):
        if prefers is None:
            prefers = []
        if friends is None:
            friends = []

        self.name = name
        self.id = _id
        self.sex = sex
        self._friends = friends  # Список друзей (объектов Student)
        self.prefers = prefers  # Список пожеланий
        self.window: MainWindow = _window

    @property
    def friends(self):
        output = []
        for stud_id in self._friends:
            output.append(self.window.students[stud_id])

        return output

    @friends.setter
    def friends(self, fset):
        output = []
        for student in fset:
            output.append(self.window.students.index(student))

        self._friends = output

    def add_to_friends(self, friend):
        self._friends.append(self.window.students.index(friend))

    def del_from_friends(self, friend):
        self._friends.remove(self.window.students.index(friend))

    def __str__(self):
        return self.name

    def __repr__(self):
        return json.dumps(
            {"name": self.name, "_id": self.id, "sex": self.sex, "friends": self._friends, "prefers": self.prefers},
            ensure_ascii=True)

    def convert_to_str(self):
        return self.__repr__()

    def seat(self, line, row, _index, classroom) -> int:
        score = 0
        mate = classroom[row][line][int(not bool(_index))][1]
        friends = self.friends
        for prefer in self.prefers:
            for _student in self.window.students:
                if prefer.startswith("Нельзя сажать с ") and _student.name == prefer[len("Нельзя сажать с "):]:
                    friends.append(_student)
                    friends = list(set(friends))  # СДЕЛАТЬ ПРОВЕРКУ НА ДРУЗЕЙ И НЕЛЬЗЯ САЖАТЬ
                if self.sex == "Мальчик":
                    if "Лучше сидеть с мальчиком" in _student.prefers:
                        score += 30
                elif self.sex == "Девочка":
                    if "Лучше сидеть с девочкой" in _student.prefers:
                        score += 30

                if _student.name == mate:
                    mate = _student
            if prefer == "Зрение" or prefer == "Лучше сидеть спереди":
                if line in [0, 1, 2]:
                    score += 25 // (line + 1)
                else:
                    score -= 3 * line + 1
            elif mate != "-" and prefer == "Лучше сидеть с мальчиком":
                if mate.sex == "Мальчик":
                    score += 15
                elif mate.sex == "Девочка":
                    score -= 8
            elif mate != "-" and prefer == "Лучше сидеть с девочкой":

                if mate.sex == "Мальчик":
                    score -= 12
                elif mate.sex == "Девочка":
                    score += 15
            elif prefer == "Лучше сидеть сзади":
                lines = self.window.lines // 2
                values = (self.window.lines - i - 1 for i in range(lines))

                if line in values:
                    score += 5 * line
                else:
                    score -= 25 // (line + 1)

            elif prefer == "Лучше сидеть в середине":
                mid = self.window.lines // 2

                if line in range(mid - 1, self.window.lines - 1 - 1):
                    score += 20
                elif line in [0, 5]:
                    score -= 20
            elif prefer == "Лучше сидеть спереди":
                if line in [0, 1, 2]:
                    score += 25
                else:
                    score -= 15
        if mate != "-" and mate in self.friends:
            score -= 50

        mates = []

        desk_up = [None, None]
        if line != 0:
            desk_up = classroom[row][line - 1][1]
            mates.append(desk_up[0])
            mates.append(desk_up[1])

        desk_right_up = [None, None]
        if row != (self.window.rows - 1) and line != 0:
            desk_right_up = classroom[row + 1][line - 1][1]
            mates.append(desk_right_up[0])
            mates.append(desk_right_up[1])

        desk_right = [None, None]
        if row != (self.window.rows - 1):
            desk_right = classroom[row + 1][line][1]
            mates.append(desk_right[0])
            mates.append(desk_right[1])

        desk_right_down = [None, None]
        if row != (self.window.rows - 1) and line + 1 <= (self.window.lines - 1):
            desk_right_down = classroom[row + 1][line + 1][1]
            mates.append(desk_right_down[0])
            mates.append(desk_right_down[1])

        desk_down = [None, None]
        if line < self.window.lines - 1:
            desk_down = classroom[row][line + 1][1]
            mates.append(desk_down[0])
            mates.append(desk_down[1])

        desk_left_down = [None, None]
        if row != 0 and line < self.window.lines - 1:
            desk_left_down = classroom[row - 1][line + 1][1]
            mates.append(desk_left_down[0])
            mates.append(desk_left_down[1])

        desk_left = [None, None]
        if row != 0:
            desk_left = classroom[row - 1][line][1]
            mates.append(desk_left[0])
            mates.append(desk_left[1])

        desk_left_up = [None, None]
        if row != 0 and line != 0:
            desk_left_up = classroom[row - 1][line - 1][1]
            mates.append(desk_left_up[0])
            mates.append(desk_left_up[1])
        for _mate in mates:
            if _mate in friends:
                score -= 5

        return score
