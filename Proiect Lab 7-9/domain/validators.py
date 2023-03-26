from domain.entities import Student
from exceptions.exceptions import ValidationException


class StudentValidator:
    def validate(self, student):
        errors = []
        if int(student.getID()) < 1000 or int(student.getID()) > 9999:
            errors.append('ID-ul trebuie sa aiba 4 cifre.')
        if len(student.getNume()) < 2:
            errors.append('Numele trebuie sa aiba cel putin 2 caractere.')
        if student.getGrup() < 0:
            errors.append('Numarul de grup trebuie sa fie mai mare de 0.')

        if len(errors) > 0:
            #errors_string = '\n'.join(errors)
            #raise ValueError(errors_string)
            raise ValidationException(errors)

class LaboratorValidator:
    def validate(self, laborator):
        errors = []
        if len(laborator.getDescriere()) < 2:
            errors.append('Descrierea trebuie sa aiba cel putin 2 caractere.')
        #if student.getNR():
           # errors.append('Numarul de grup trebuie sa fie mai mare de 0.')

        if len(errors) > 0:
            #errors_string = '\n'.join(errors)
            #raise ValueError(errors_string)
            raise ValidationException(errors)

class NotaValidator:
    def validate(self, grade):
        errors = []
        if grade.getNota() < 1 or grade.getNota() > 10:
            errors.append('Nota trebuie sa fie un numar intre 1 si 10.')

        if len(errors) > 0:
            #errors_string = '\n'.join(errors)
            #raise ValueError(errors_string)
            raise ValidationException(errors)


def test_student_validator():
    test_validator = StudentValidator()
    student1 = Student(8014, 'Ovidiu Toma', 916)
    test_validator.validate(student1)
    student2 = Student(1235, '', 916)

    try:
        test_validator.validate(student2)
        assert False
    except ValueError:
        assert True

    student3 = Student(12, 'Carina Malin', 916)
    try:
        test_validator.validate(student3)
        assert False
    except ValueError:
        assert True

#test_student_validator())