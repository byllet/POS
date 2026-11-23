from dependency_injector import containers, providers

from domain.final_score_service import FinalScoreService
from infrastructure.csv_results import CsvResultsWriter
from infrastructure.csv_store import CsvStore
from infrastructure.rubricator import CsvRubricatorRepository
from infrastructure.students import CsvStudentRepository
from presentation.cli import ConsoleApp
from presentation.criteria import CriteriaCommands
from presentation.evaluations import EvaluationsCommands
from presentation.reports import ReportsCommands
from presentation.students import StudentsCommands
from use_cases.add_criterion import AddCriterionRequestHandler
from use_cases.add_student import AddStudentRequestHandler
from use_cases.change_student_evaluation import ChangeStudentEvaluationRequestHandler
from use_cases.delete_student_evaluation import DeleteStudentEvaluationRequestHandler
from use_cases.evaluate_sudent import EvaluateStudentRequestHandler
from use_cases.export_results import ExportResultsRequestHandler
from use_cases.get_student_result import GetStudentResultRequestHandler
from use_cases.list_criterions import ListCriteriaRequestHandler
from use_cases.list_student_evaluations import ListStudentEvaluationsRequestHandler
from use_cases.list_sudents import ListStudentsRequestHandler


class Container(containers.DeclarativeContainer):
    store = providers.Dependency(instance_of=CsvStore)
    rubricator = providers.Singleton(CsvRubricatorRepository, store)
    students = providers.Singleton(CsvStudentRepository, store, rubricator)
    calculator = providers.Singleton(FinalScoreService)
    writer = providers.Factory(CsvResultsWriter)

    student_commands = providers.Factory(
        StudentsCommands,
        add_student=providers.Factory(AddStudentRequestHandler, students),
        list_students=providers.Factory(ListStudentsRequestHandler, students),
    )
    criterion_commands = providers.Factory(
        CriteriaCommands,
        add_criterion=providers.Factory(AddCriterionRequestHandler, rubricator),
        list_criteria=providers.Factory(ListCriteriaRequestHandler, rubricator),
    )
    grade_commands = providers.Factory(
        EvaluationsCommands,
        evaluate_student=providers.Factory(EvaluateStudentRequestHandler, students, rubricator),
        change_evaluation=providers.Factory(ChangeStudentEvaluationRequestHandler, students, rubricator),
        delete_evaluation=providers.Factory(DeleteStudentEvaluationRequestHandler, students),
        list_evaluations=providers.Factory(ListStudentEvaluationsRequestHandler, students),
    )
    report_commands = providers.Factory(
        ReportsCommands,
        get_result=providers.Factory(GetStudentResultRequestHandler, students, calculator),
        export_results=providers.Factory(ExportResultsRequestHandler, students, calculator, writer),
    )
    app = providers.Factory(ConsoleApp, student_commands, criterion_commands, grade_commands, report_commands)
