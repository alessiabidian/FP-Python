import unittest

from domain.entities import Laborator
from domain.validators import LaboratorValidator
from exceptions.exceptions import ValidationException


class TestCaseLaboratorDomain(unittest.TestCase):
    def setUp(self) -> None:
        self.__validator = LaboratorValidator()

    def test_create_laborator(self):
        laborator1 = Laborator(702, 'Alg de calculare produs', '22.02.2022')
        self.assertEqual(laborator1.getNR(), 702)
        self.assertEqual(laborator1.getDescriere(), 'Alg de calculare produs')
        self.assertEqual(laborator1.getDeadline(), '22.02.2022')

        laborator1.setNR(601)
        laborator1.setDescriere('Backtracking')
        laborator1.setDeadline('28.02.2022')

        self.assertEqual(laborator1.getNR(), 601)
        self.assertEqual(laborator1.getDescriere(), 'Backtracking')
        self.assertEqual(laborator1.getDeadline(), '28.02.2022')

    def test_equals_laborator(self):
        laborator1 = Laborator(702, 'Alg de calculare produs', '22.02.2022')
        laborator2 = Laborator(702, 'Alg de calculare produs', '22.02.2022')

        self.assertEqual(laborator1, laborator2)

        laborator3 = Laborator(804, 'Alg de sortare', '15.01.2022')
        self.assertNotEqual(laborator1, laborator3)

    def test_laborator_validator(self):
        laborator1 = Laborator(702, 'Alg de calculare produs', '22.02.2022')
        self.__validator.validate(laborator1)
        laborator2 = Laborator(702, '', '28.02.2022')

        #self.assertRaises(ValidationException, self.__validator.validate, laborator2)


unittest.main()