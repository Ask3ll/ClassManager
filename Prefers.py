
class Prefer:
    def __init__(self, text, student=None):
        self.student = None
        if student:
            self.student = student

        self.text = text

    def serialize(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.text

    def __str__(self):
        return self.__repr__()

    def delete(self):
        if self.student:
            # noinspection PyUnresolvedReferences
            self.student.prefers.remove(self)


class VisionPrefer(Prefer):
    def __init__(self, student=None):
        super().__init__("Зрение", student)


class DoNotSeatWithPrefer(Prefer):
    def __init__(self, student=None, other_student_id=None):
        if not student and not other_student_id:
            super().__init__("Нельзя сажать с этим учеником", student)
        else:
            super().__init__("Нельзя сажать с ", student)
        self.other_student_id = other_student_id
        self.other_student = None

    def __repr__(self):
        if self.other_student_id is not None:
            self.other_check()
            return self.text + self.other_student.name
        else:
            return self.text

    def serialize(self):
        self.other_check()
        return [self.__class__.__name__, self.other_student.id]

    def other_check(self):
        if not self.other_student:
            # noinspection PyUnresolvedReferences
            self.other_student = self.student.window.get_student(self.other_student_id)


class SeatNextToMalePrefer(Prefer):
    def __init__(self, student=None):
        super().__init__("Лучше сидеть с мальчиком", student)


class SeatNextToFemalePrefer(Prefer):
    def __init__(self, student=None):
        super().__init__("Лучше сидеть с девочкой", student)


class SeatInBackPrefer(Prefer):
    def __init__(self, student=None):
        super().__init__("Лучше сидеть сзади", student)


class SeatInMiddlePrefer(Prefer):
    def __init__(self, student=None):
        super().__init__("Лучше сидеть в середине", student)


class SeatInFrontPrefer(Prefer):
    def __init__(self, student=None):
        super().__init__("Лучше сидеть спереди", student)


all_prefers = [VisionPrefer(), DoNotSeatWithPrefer(), SeatNextToMalePrefer(), SeatNextToFemalePrefer(),
               SeatInBackPrefer(), SeatInMiddlePrefer(), SeatInFrontPrefer()]

prefers_dict = {
    "Зрение": VisionPrefer,
    "Нельзя сажать с этим учеником": DoNotSeatWithPrefer,
    "Нельзя сажать с ": DoNotSeatWithPrefer,
    "Лучше сидеть с мальчиком": SeatNextToMalePrefer,
    "Лучше сидеть с девочкой": SeatNextToFemalePrefer,
    "Лучше сидеть сзади": SeatInBackPrefer,
    "Лучше сидеть в середине": SeatInMiddlePrefer,
    "Лучше сидеть спереди": SeatInFrontPrefer,
}
