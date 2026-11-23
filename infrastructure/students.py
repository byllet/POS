from domain.evaluation import Evaluation
from domain.rubricator import Rubricator
from domain.score import Score
from domain.student import Student, StudentName

from .csv_store import CsvStore
from .rubricator import CsvRubricatorRepository


class CsvStudentRepository:
    def __init__(self, store: CsvStore, rubricator: CsvRubricatorRepository):
        self._store = store
        self._rubricator = rubricator

    def _roster(self) -> dict[int, Student]:
        roster = {}
        for key, name in self._store.students.read():
            student_id = int(key)
            if student_id in roster:
                raise ValueError(f"В students.csv повторяется ID {student_id}.")
            roster[student_id] = Student(student_id, StudentName(name))
        return roster

    def create(self, name: StudentName) -> Student:
        roster = self._roster()
        student = Student(max(roster, default=0) + 1, name)
        roster[student.id] = student
        self._store.students.write((s.id, str(s.name)) for s in roster.values())
        return student

    def get_all_with_rubricator(self) -> tuple[list[Student], Rubricator]:
        rubricator = self._rubricator.load()
        students = self._roster()
        for key, criterion_id, points in self._store.evaluations.read():
            student = students.get(int(key))
            if student is None:
                raise ValueError(f"В evaluations.csv указан неизвестный студент {key}.")
            student.add_evaluation(Evaluation(rubricator, int(criterion_id), Score(int(points))))
        return list(students.values()), rubricator

    def get_with_rubricator(self, student_id: int) -> tuple[Student, Rubricator]:
        students, rubricator = self.get_all_with_rubricator()
        for student in students:
            if student.id == student_id:
                return student, rubricator
        raise ValueError(f"Студент с ID {student_id} не найден.")

    def get(self, student_id: int) -> Student:
        student, _ = self.get_with_rubricator(student_id)
        return student

    def get_all(self) -> list[Student]:
        students, _ = self.get_all_with_rubricator()
        return students

    def save(self, student: Student) -> None:
        if student.id not in self._roster():
            raise ValueError(f"Студент с ID {student.id} не найден.")
        rows = [row for row in self._store.evaluations.read() if int(row[0]) != student.id]
        grades = [(student.id, grade.criterion_id, int(grade.score)) for grade in student.evaluations.values()]
        self._store.evaluations.write([*rows, *grades])
