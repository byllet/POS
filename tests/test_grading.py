import unittest

from domain.criterion import Criterion, CriterionName, Weight
from domain.evaluation import Evaluation
from domain.final_score_service import FinalScoreService
from domain.rubricator import Rubricator
from domain.score import Score
from domain.student import Student, StudentName


class GradingTests(unittest.TestCase):
    def setUp(self):
        self.lab = Criterion(1, CriterionName("Лабораторная"), Score(10), Weight(2))
        self.rubric = Rubricator()
        self.rubric.add(self.lab)
        self.student = Student(1, StudentName("Анна"))

    def test_score_must_be_within_inclusive_criterion_limits(self):
        for points in (0, 10):
            with self.subTest(points=points):
                grade = Evaluation(self.rubric, self.lab.id, Score(points))
                self.assertEqual(grade.score.value, points)
        for points in (-1, 11):
            with self.subTest(points=points), self.assertRaises(ValueError):
                Evaluation(self.rubric, self.lab.id, Score(points))

    def test_unknown_criterion_is_rejected(self):
        with self.assertRaises(ValueError):
            Evaluation(self.rubric, 99, Score(5))

    def test_names_must_contain_non_whitespace_characters(self):
        for name_type in (StudentName, CriterionName):
            for name in ("", " \t\n"):
                with self.subTest(name_type=name_type, name=name), self.assertRaises(ValueError):
                    name_type(name)

    def test_duplicate_grade_preserves_original_score(self):
        self.student.add_evaluation(Evaluation(self.rubric, self.lab.id, Score(8)))
        with self.assertRaises(ValueError):
            self.student.add_evaluation(Evaluation(self.rubric, self.lab.id, Score(9)))
        self.assertEqual(self.student.evaluations[self.lab.id].score, Score(8))

    def test_weighted_result_reflects_correction_and_removal(self):
        exam = Criterion(2, CriterionName("Защита"), Score(20), Weight(3))
        self.rubric.add(exam)
        self.student.add_evaluation(Evaluation(self.rubric, self.lab.id, Score(8)))
        self.student.add_evaluation(Evaluation(self.rubric, exam.id, Score(15)))
        service = FinalScoreService()
        self.assertEqual(service.calculate(self.student, self.rubric).percent, 77)

        self.student.change_evaluation(Evaluation(self.rubric, self.lab.id, Score(9)))
        self.assertEqual(service.calculate(self.student, self.rubric).percent, 81)

        self.student.remove_evaluation(exam.id)
        result = service.calculate(self.student, self.rubric)
        self.assertEqual(result.percent, 90)
        self.assertEqual((result.evaluated_count, result.criterion_count), (1, 2))

        self.student.add_evaluation(Evaluation(self.rubric, exam.id, Score(0)))
        result = service.calculate(self.student, self.rubric)
        self.assertEqual(result.percent, 36)
        self.assertEqual((result.evaluated_count, result.criterion_count), (2, 2))

    def test_no_evaluations_has_no_percentage(self):
        result = FinalScoreService().calculate(self.student, self.rubric)
        self.assertIsNone(result.percent)
        self.assertEqual((result.evaluated_count, result.criterion_count), (0, 1))

    def test_empty_rubric_has_no_percentage(self):
        result = FinalScoreService().calculate(self.student, Rubricator())
        self.assertIsNone(result.percent)
        self.assertEqual((result.evaluated_count, result.criterion_count), (0, 0))
