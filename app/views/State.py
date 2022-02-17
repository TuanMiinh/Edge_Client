import enum


class ProcessType(enum.Enum):
    FACEFOOD = 0
    FEEDBACK = 1


class RecognizeState(enum.Enum):
    INIT = 0
    RECOGNIZING = 1
    RECOGNIZED = 2
    UN_RECOGNIZED = 3
    RECOGNIZED_SUCESSED = 4
    RECONIZED_FAILED = 5
    RETRY = 6
    RATING = 7


class RatingState(enum.Enum):
    FINISH = 1
    NOT_FINISH = 2
