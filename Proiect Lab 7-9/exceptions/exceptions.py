class StudentManagerException(Exception):
    pass


class ValidationException(StudentManagerException):
    def __init__(self, msgs):
        """
        :param msgs: lista de mesaje de eroare
        :type msgs: msgs
        """
        self.__err_msgs = msgs

    def getMessages(self):
        return self.__err_msgs

    def __str__(self):
        return 'Validation Exception: ' + str(self.__err_msgs)


class RepositoryException(StudentManagerException):
    def __init__(self, msg):
        self.__msg = msg

    def getMessage(self):
        return self.__msg

    def __str__(self):
        return 'Repository Exception: ' + str(self.__msg)


class DuplicateIDException(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "ID duplicat.")


class GradeAlreadyAssignedException(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "Nota existenta deja pentru studentul si laboratorul dat.")


class StudentNotFoundException(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "Studentul nu a fost gasit.")


class GradeNotFoundException(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "Nota nu a fost gasita.")


class LaboratorNotFoundException(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "Problema de laborator nu a fost gasita.")


class GradeNotValid(StudentManagerException):
    def __init__(self):
        ValidationException.__init__(self, "Nota trebuie sa fie un nr intre 1 si 10.")


class CorruptedFileException(StudentManagerException):
    def __init__(self):
        pass
