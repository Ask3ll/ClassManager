import json

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
        self.window = _window

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

    def seat(self, desk_id, column, _index, classroom):
        score = 0
        mate = classroom[column][desk_id][int(not bool(_index))][1]
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
                if desk_id in [0, 1, 2]:
                    score += 25 // (desk_id + 1)
                else:
                    score -= 3 * desk_id + 1
            elif mate != "-" and prefer == "Лучше сидеть с мальчиком":
                if mate.sex == "Мальчик":
                    score += 15
                elif mate.sex == "Девочка":
                    score -= 8
            elif mate != "-" and prefer == "Лучше сидеть с девочкой":
                print(mate)
                if mate.sex == "Мальчик":
                    score -= 12
                elif mate.sex == "Девочка":
                    score += 15
            elif prefer == "Лучше сидеть сзади":
                if desk_id in [5, 4, 3]:
                    score += 5 * desk_id
                else:
                    score -= 25 // (desk_id + 1)
            elif prefer == "Лучше сидеть в середине":
                if desk_id in [2, 3]:
                    score += 20
                elif desk_id in [0, 5]:
                    score -= 20
            elif prefer == "Лучше сидеть спереди":
                if desk_id in [0, 1, 2]:
                    score += 25
                elif desk_id in [3, 4, 5]:
                    score -= 15
        if mate != "-" and mate in self.friends:
            score -= 50

        mates = []

        desk_up = [None, None]
        if desk_id - 1 > 0:
            desk_up = classroom[column][desk_id - 1][1]
            mates.append(desk_up[0])
            mates.append(desk_up[1])

        desk_right_up = [None, None]
        if column != 2 and desk_id - 1 > 0:
            desk_right_up = classroom[column + 1][desk_id - 1][1]
            mates.append(desk_right_up[0])
            mates.append(desk_right_up[1])

        desk_right = [None, None]
        if column != 2:
            desk_right = classroom[column + 1][desk_id][1]
            mates.append(desk_right[0])
            mates.append(desk_right[1])

        desk_right_down = [None, None]

        if column != 2 and desk_id + 1 <= 5:
            desk_right_down = classroom[column + 1][desk_id + 1][1]
            mates.append(desk_right_down[0])
            mates.append(desk_right_down[1])

        desk_down = [None, None]
        if desk_id + 1 <= 5:
            desk_down = classroom[column][desk_id + 1][1]
            mates.append(desk_down[0])
            mates.append(desk_down[1])

        desk_left_down = [None, None]
        if column != 0 and desk_id + 1 <= 5:
            desk_left_down = classroom[column - 1][desk_id + 1][1]
            mates.append(desk_left_down[0])
            mates.append(desk_left_down[1])

        desk_left = [None, None]
        if column != 0:
            desk_left = classroom[column - 1][desk_id][1]
            mates.append(desk_left[0])
            mates.append(desk_left[1])

        desk_left_up = [None, None]
        if column != 0 and desk_id - 1 > 0:
            desk_left_up = classroom[column - 1][desk_id - 1][1]
            mates.append(desk_left_up[0])
            mates.append(desk_left_up[1])
        for _mate in mates:
            if _mate in friends:
                score -= 5

        return score