from Prefers import *


# from MainWindow import MainWindow


class Student:
    def __init__(self, _window, name, sex, _id=None, friends=None, prefers=None):
        if _id is None:
            _id = _window.new_stud_id
            _window.new_stud_id += 1

        if friends is None:
            friends = []

        self.name = name
        self.id = _id
        self.sex = sex
        self._friends = friends  # Список друзей (объектов Student)
        self.prefers = prefers  # Список пожеланий (PrefersList)
        self.window = _window

        if prefers is None:
            self.prefers = PrefersList(self)
        else:
            self.prefers = PrefersList(self, from_json=prefers)

    @property
    def friends(self):
        output = []
        for stud_id in self._friends:
            output.append(self.window.get_student(stud_id))

        return output

    @friends.setter
    def friends(self, fset):
        output = []
        for student in fset:
            output.append(student.id)

        self._friends = output

    def add_to_friends(self, friend):
        self._friends.append(friend.id)

    def del_from_friends(self, friend):
        self._friends.remove(friend.id)

    def __str__(self):
        return self.name

    def __repr__(self):
        return json.dumps(
            {"name": self.name, "sex": self.sex, "_id": self.id, "friends": self._friends,
             "prefers": str(self.prefers)},
            ensure_ascii=True)

    def convert_to_str(self):
        return self.__repr__()

    def seat(self, classroom, line, row, _index, ) -> int:
        score = 0
        # if ((SeatInBackPrefer not in self.prefers) and (SeatInMiddlePrefer not in self.prefers)) and line in [0, 1, 2]:
        #     to_add = 3 - line
        #     if to_add > 0:
        #         print(to_add*10, 123)
        #         score += to_add*100

        mate = classroom[row][line][int(not bool(_index))][1]
        friends = self.friends.copy()
        for prefer in self.prefers:
            for _student in self.window.students:
                if isinstance(prefer, DoNotSeatWithPrefer):
                    if _student == prefer.other_student:
                        friends.append(_student)
                        friends = list(set(friends))
                if self.sex == "Мальчик":
                    if SeatNextToMalePrefer in _student.prefers:
                        score += 30
                elif self.sex == "Девочка":
                    if SeatNextToFemalePrefer in _student.prefers:
                        score += 30

                if _student.name == mate:
                    mate = _student
            if isinstance(prefer, VisionPrefer) or isinstance(prefer, SeatInFrontPrefer):
                if line in [0, 1, 2]:
                    score += 25 // (line + 1)
                else:
                    score -= 3 * line + 1
            elif mate != "-" and isinstance(prefer, SeatNextToMalePrefer):
                if mate.sex == "Мальчик":
                    score += 15
                elif mate.sex == "Девочка":
                    score -= 8
            elif mate != "-" and isinstance(prefer, SeatNextToFemalePrefer):
                if mate.sex == "Мальчик":
                    score -= 12
                elif mate.sex == "Девочка":
                    score += 15
            elif isinstance(prefer, SeatInBackPrefer):
                lines = self.window.lines // 2
                values = (self.window.lines - i - 1 for i in range(lines))

                if line in values:
                    score += 5 * line
                else:
                    score -= 25 // (line + 1)

            elif isinstance(prefer, SeatInMiddlePrefer):
                mid = self.window.lines // 2

                if line in range(mid - 1, self.window.lines - 1 - 1):
                    score += 20
                elif line in [0, 5]:
                    score -= 20

        if mate != "-" and mate in self.friends:
            score -= 50

        mates = []

        # noinspection PyUnusedLocal
        desk_up = [None, None]
        if line != 0:
            desk_up = classroom[row][line - 1][1]
            mates.append(desk_up[0])
            mates.append(desk_up[1])

        # noinspection PyUnusedLocal
        desk_right_up = [None, None]
        if row != (self.window.rows - 1) and line != 0:
            desk_right_up = classroom[row + 1][line - 1][1]
            mates.append(desk_right_up[0])
            mates.append(desk_right_up[1])

        # noinspection PyUnusedLocal
        desk_right = [None, None]
        if row != (self.window.rows - 1):
            desk_right = classroom[row + 1][line][1]
            mates.append(desk_right[0])
            mates.append(desk_right[1])

        # noinspection PyUnusedLocal
        desk_right_down = [None, None]
        if row != (self.window.rows - 1) and line + 1 <= (self.window.lines - 1):
            desk_right_down = classroom[row + 1][line + 1][1]
            mates.append(desk_right_down[0])
            mates.append(desk_right_down[1])

        # noinspection PyUnusedLocal
        desk_down = [None, None]
        if line < self.window.lines - 1:
            desk_down = classroom[row][line + 1][1]
            mates.append(desk_down[0])
            mates.append(desk_down[1])

        # noinspection PyUnusedLocal
        desk_left_down = [None, None]
        if row != 0 and line < self.window.lines - 1:
            desk_left_down = classroom[row - 1][line + 1][1]
            mates.append(desk_left_down[0])
            mates.append(desk_left_down[1])

        # noinspection PyUnusedLocal
        desk_left = [None, None]
        if row != 0:
            desk_left = classroom[row - 1][line][1]
            mates.append(desk_left[0])
            mates.append(desk_left[1])

        # noinspection PyUnusedLocal
        desk_left_up = [None, None]
        if row != 0 and line != 0:
            desk_left_up = classroom[row - 1][line - 1][1]
            mates.append(desk_left_up[0])
            mates.append(desk_left_up[1])
        for _mate in mates:
            if _mate in friends:
                score -= 5

        return score

