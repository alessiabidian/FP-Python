import unittest

from domain.validators import NotaValidator

from domain.entities import Student, Laborator, Nota
from exceptions.exceptions import ValidationException


class TestCaseGradeDomain(unittest.TestCase):
    def setUp(self) -> None:
        self.__validator = NotaValidator()

    def test_create_grade(self):
        s = Student(2122, 'Elena Sirintra', 932)
        l = Laborator(501, 'Alg de sortare', '27.03.2022')

        n = Nota(l, s, 9)

        self.assertEqual(n.getStudent().getID(), 2122)
        self.assertEqual(n.getLab().getNR(), 501)
        self.assertEqual(n.getNota(), 9)

    def test_equal_grade(self):
        s1 = Student(2122, 'Elena Sirintra', 932)
        l = Laborator(501, 'Alg de sortare', '27.03.2022')

        n1 = Nota(l, s1, 9)
        n2 = Nota(l, s1, 9)

        self.assertEqual(n1.getLab(), n2.getLab())
        self.assertEqual(n1.getStudent(), n2.getStudent())
        self.assertEqual(n1.getNota(), n2.getNota())

        s2 = Student(1088, 'Andreea Trif', 112)
        n3 = Nota(l, s2, 5)
        self.assertNotEqual(n3, n2)

    def test_grade_validator(self):
        s = Student(2122, 'Elena Sirintra', 932)
        l = Laborator(501, 'Alg de sortare', '27.03.2022')

        n = Nota(l, s, 6.8)

        self.__validator = NotaValidator()
        self.__validator.validate(n)

        n1 = Nota(l, s, 100)
        #self.assertRaises(ValidationException, self.__validator.validate, n1)

unittest.main()