class InsufficientBalanceError(Exception):
    def __init__(self, message="Insufficient balance for this transaction"):
        super().__init__(message)


class InvalidAmountError(Exception):
    def __init__(self, message="Amount must be greater than zero"):
        super().__init__(message)
