import abc
import dataclasses
import io
import json
import os
import pathlib
import tomllib
import typing

from slcfg import item

type Transformer[T, S] = typing.Callable[[T], S]
type Layer = Source[item.Items]


@dataclasses.dataclass
class Source[T](abc.ABC):
    getter: typing.Callable[[], T]

    def __or__[S](self, t: Transformer[T, S]):
        return Source(getter=lambda: t(self.getter()))


### File Sources


def file_source(path: pathlib.Path, *, optional: bool):
    def getter():
        try:
            return io.BytesIO(path.read_bytes())
        except FileNotFoundError:
            if optional:
                return io.BytesIO()
            raise

    return Source(getter=getter)


def file_layer(
    path: pathlib.Path, parser: Transformer[io.BytesIO, typing.Any], *, optional: bool = False
):
    return file_source(path, optional=optional) | parser | item.list_items


def json_file_layer(path: pathlib.Path, *, optional: bool = False):
    return file_layer(path, json.load, optional=optional)


def toml_file_layer(path: pathlib.Path, *, optional: bool = False):
    return file_layer(path, tomllib.load, optional=optional)


### Env Sources


def env_source():
    return Source(getter=lambda: list(os.environ.items()))


def case_transform(vars: list[tuple[str, str]]):
    return [(k.lower(), v) for k, v in vars]


def prefix_transformer(prefix: str):
    def transormer(vars: list[tuple[str, str]]):
        return [(k.removeprefix(prefix), v) for k, v in vars if k.startswith(prefix)]

    return transormer


def delimiter_transformer(delimiter: str):
    def transormer(vars: list[tuple[str, str]]):
        return [(k.split(delimiter), v) for k, v in vars]

    return transormer


def item_transform(vars: list[tuple[list[str], str]]) -> item.Items:
    return [item.Item(k, v) for k, v in vars]


def env_layer(prefix: str, nested_delimiter: str, *, case_sensitive: bool = False):
    source = env_source()

    if not case_sensitive:
        prefix = prefix.lower()
        nested_delimiter = nested_delimiter.lower()
        source = source | case_transform

    return (
        source
        | prefix_transformer(prefix)
        | delimiter_transformer(nested_delimiter)
        | item_transform
    )
