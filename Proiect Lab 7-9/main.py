from domain.validators import StudentValidator, LaboratorValidator, NotaValidator
from repository.studs_repo import InMemoryRepository_Stud, StudFileRepoInheritance
from repository.labs_repo import InMemoryRepository_Lab, LabFileRepoInheritance
from repository.grades_repo import InMemoryRepository_Grade, GradeFileRepoInheritance
from service.studs_service import StudentService
from service.labs_service import LaboratorService
from service.grades_service import NotaService
from ui.console import Console

repo_stud = StudFileRepoInheritance('data/students.txt')
val_stud = StudentValidator()
srv_stud = StudentService(repo_stud, val_stud)

repo_lab = LabFileRepoInheritance('data/labs.txt')
val_lab = LaboratorValidator()
srv_lab = LaboratorService(repo_lab, val_lab)

repo_grade = GradeFileRepoInheritance('data/grades.txt')
val_grade = NotaValidator()
srv_grade = NotaService(repo_grade, val_grade, repo_stud, repo_lab)

ui = Console(srv_stud, srv_lab, srv_grade)
ui.choose_ui()