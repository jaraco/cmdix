class StdOutException(Exception):
    """
    Raised when data is written to stdout
    """

    def __init__(self, text, errno=1):
        """
        :text:  Output text
        ;errno: Exit status of program
        """
        self.text = text
        self.errno = errno

    def __str__(self):
        return self.text


class StdErrException(Exception):
    """
    Raised when data is written to stderr
    """

    def __init__(self, text, errno=2):
        """
        :text:  Error text
        ;errno: Exit status of program
        """
        self.text = text
        self.errno = errno

    def __str__(self):
        return self.text


class CommandNotFoundException(Exception):
    """
    Raised when an unknown command is requested
    """

    def __init__(self, prog):
        self.prog = prog

    def __str__(self):
        return f"Command `{self.prog}' not found."


class ExtraOperandException(StdErrException):
    """
    Raised when an argument is expected but not found
    """

    def __init__(self, program, operand, errno=1):
        """
        :program:   Program that caused the error
        :operand:   Value of the extra operand
        ;errno:     Exit status of program
        """
        self.program = program
        self.operand = operand
        self.errno = errno

    def __str__(self):
        return (
            "{0}: extra operand `{1}'. Try {0} --help' for more ".format(
                self.program, self.operand
            )
            + "information."
        )


class MissingOperandException(StdErrException):
    """
    Raised when an argument is expected but not found
    """

    def __init__(self, program, errno=1):
        """
        :program:   Program that caused the error
        ;errno:     Exit status of program
        """
        self.program = program
        self.errno = errno

    def __str__(self):
        return (
            "{0}: missing operand. Try `{0} --help'".format(self.program)
            + " for more information."
        )
