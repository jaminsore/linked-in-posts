import pathlib
import pickle
import tempfile

import pytest
from fasttext import FastText

from linked_in_posts import pickling


def test_fasttext_model_cannot_be_pickled(fasttext_model: FastText._FastText) -> None:  # type: ignore[no-any-unimported]
    with pytest.raises(TypeError, match=r"cannot pickle 'fasttext_pybind\.fasttext' object"):
        pickle.dumps(fasttext_model)


def test_picklable_fasttext_is_picklable(fasttext_model: FastText._FastText) -> None:  # type: ignore[no-any-unimported]
    picklable_model = pickling.PicklableFastText.from_pretrained(fasttext_model)

    with tempfile.TemporaryDirectory() as d:
        model_file = pathlib.Path(d) / picklable_model._tmp_filename
        picklable_model.save_model(str(model_file))
        from_file = picklable_model.load(str(model_file))
        from_bytes = picklable_model.load(picklable_model.serialize())

    assert from_file.words == picklable_model.words
    assert from_bytes.words == picklable_model.words
    assert picklable_model.words == fasttext_model.words

    with pytest.raises(FileNotFoundError):
        picklable_model.load("a/path/that/does/not/exist.bin")
