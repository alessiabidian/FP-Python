import unittest

from domain.entities import Student
from domain.validators import StudentValidator
from exceptions.exceptions import ValidationException


class TestCaseStudentDomain(unittest.TestCase):
    def setUp(self) -> None:
        self.__validator = StudentValidator()

    def test_create_student(self):
        student1 = Student(1643, 'Ciara Gold', 211)
        self.assertEqual(student1.getID(), 1643)
        self.assertEqual(student1.getNume(), 'Ciara Gold')
        self.assertEqual(student1.getGrup(), 211)

        student1.setID(1666)
        student1.setNume('Georgiana Gold')
        student1.setGrup(911)

        self.assertEqual(student1.getID(), 1666)
        self.assertEqual(student1.getNume(), 'Georgiana Gold')
        self.assertEqual(student1.getGrup(), 911)

    def test_equals_serial(self):
        student1 = Student(1643, 'Ciara Gold', 211)
        student2 = Student(1643, 'Ciara Gold', 211)

        self.assertEqual(student1, student2)

        student3 = Student(9401, 'Tina Turner', 916)
        self.assertNotEqual(student1, student3)

    def test_student_validator(self):
        student1 = Student(1643, 'Ciara Gold', 211)
        self.__validator.validate(student1)
        student2 = Student(1643, '', 211)
        student3 = Student(94071, 'Tina Turner', 916)

        self.assertRaises(ValidationException, self.__validator.validate, student2)
        self.assertRaises(ValidationException, self.__validator.validate, student3)

unittest.main()