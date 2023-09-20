import pathlib
import tempfile
from typing import Callable, Self

import fasttext
from fasttext import FastText


class PicklableFastText(FastText._FastText):  # type: ignore[no-any-unimported]
    _tmp_filename = "model.bin"

    @classmethod
    def from_pretrained(cls, model: FastText._FastText) -> Self:  # type: ignore[no-any-unimported]
        self = cls.__new__(cls)
        self.__dict__.update(model.__dict__)
        return self

    @classmethod
    def load(cls, saved_model: bytes | str) -> Self:
        if isinstance(saved_model, str) and pathlib.Path(saved_model).exists():
            return cls.from_pretrained(fasttext.load_model(saved_model))

        if isinstance(saved_model, bytes):
            with tempfile.TemporaryDirectory() as d:
                model_path = pathlib.Path(d) / cls._tmp_filename
                model_path.write_bytes(saved_model)
                return cls.load(str(model_path))

        raise FileNotFoundError(saved_model)

    def serialize(self) -> bytes:
        with tempfile.TemporaryDirectory() as d:
            model_path = pathlib.Path(d) / self._tmp_filename
            self.save_model(str(model_path))
            return model_path.read_bytes()

    def __reduce__(self) -> tuple[Callable[[bytes | str], Self], tuple[bytes]]:
        return self.load, (self.serialize(),)
