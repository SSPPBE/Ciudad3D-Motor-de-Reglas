from enum import Enum

class ErrorType(Enum):
    
    NOT_FOUND=0
    REPOSITORY=1
    FOUND=2
    NOT_VALID=3
    INTERNAL=4