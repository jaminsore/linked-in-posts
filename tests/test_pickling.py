import pickle

import pytest
from fasttext import FastText


def test_fasttext_model_cannot_be_pickled(fastext_model: FastText._FastText) -> None:  # type: ignore[no-any-unimported]
    with pytest.raises(TypeError, match=r"cannot pickle 'fasttext_pybind\.fasttext' object"):
        pickle.dumps(fastext_model)
