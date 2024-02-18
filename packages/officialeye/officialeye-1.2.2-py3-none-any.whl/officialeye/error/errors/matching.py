from abc import ABC

from officialeye.error.codes import ERR_MATCHING_INVALID_ENGINE_CONFIG, ERR_MATCHING_MATCH_COUNT_OUT_OF_BOUNDS
from officialeye.error.error import OEError
from officialeye.error.modules import ERR_MODULE_MATCHING


class ErrMatching(OEError, ABC):

    def __init__(self, code: int, code_text: str, while_text: str, problem_text: str, /, *, is_regular: bool, **kwargs):
        super().__init__(ERR_MODULE_MATCHING, code, code_text, while_text, problem_text, is_regular=is_regular)


class ErrMatchingMatchCountOutOfBounds(ErrMatching):
    def __init__(self, while_text: str, problem_text: str, /, **kwargs):
        super().__init__(
            ERR_MATCHING_MATCH_COUNT_OUT_OF_BOUNDS[0], ERR_MATCHING_MATCH_COUNT_OUT_OF_BOUNDS[1], while_text, problem_text, is_regular=True, **kwargs)

        self._init_args = while_text, problem_text, *kwargs

    def __reduce__(self):
        return self.__class__, self._init_args


class ErrMatchingInvalidEngineConfig(ErrMatching):
    def __init__(self, while_text: str, problem_text: str, /, **kwargs):
        super().__init__(
            ERR_MATCHING_INVALID_ENGINE_CONFIG[0], ERR_MATCHING_INVALID_ENGINE_CONFIG[1], while_text, problem_text, is_regular=False, **kwargs)

        self._init_args = while_text, problem_text, *kwargs

    def __reduce__(self):
        return self.__class__, self._init_args
