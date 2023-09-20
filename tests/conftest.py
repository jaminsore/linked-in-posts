import pathlib
import tempfile

import fasttext
import pytest
from fasttext import FastText
from lorem_text import lorem


@pytest.fixture
def training_text() -> str:
    return "\n".join(f"{lorem.sentence()}" for _ in range(100)) + "\n"


@pytest.fixture
def fastext_model(training_text: str) -> FastText._FastText:  # type: ignore[no-any-unimported]
    with tempfile.TemporaryDirectory() as d:
        train_file = pathlib.Path(d) / "train.txt"
        train_file.write_text(training_text)
        return fasttext.train_unsupervised(str(train_file), model="cbow")
