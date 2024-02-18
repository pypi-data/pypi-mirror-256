import functools
import importlib
import inspect
import textwrap
from collections import defaultdict
from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass
from graphlib import TopologicalSorter
from pathlib import Path
from typing import Any, Union, get_args, get_origin, get_type_hints, Type
import typing
import click
from boltons.strutils import under2camel
from numpydoc.docscrape import NumpyDocString
from toolz import dicttoolz
from tqdm.auto import tqdm

from pyxel import __version__
from pyxel.pipelines import DetectionPipeline

NONE_TYPE = type(None)


@dataclass(frozen=True)
class Klass:
    cls: type
    base_cls: type | None = None

    @property
    def name(self) -> str:
        return self.cls.__name__


@dataclass(frozen=True)
class ClassDescription:
    base_cls: Type | None
    doc: str
    parameters: Mapping


@functools.cache
def create_klass(cls: type | str) -> Klass:
    import pyxel.detectors

    if isinstance(cls, str):
        cls_type: type = getattr(pyxel.detectors, cls)
        return create_klass(cls_type)

    # Try to find a base class
    if (origin := get_origin(cls)) is not None:
        args: Sequence = get_args(cls)

        if origin == Union:
            if len(args) != 2:
                raise NotImplementedError

            # Optional type
            klass = args[0]

        else:
            raise NotImplementedError
    else:
        klass = cls

    _, *base_classes, _ = inspect.getmro(klass)

    if base_classes:
        return Klass(klass, base_cls=base_classes[0])

    return Klass(klass)


class AllClasses:
    def __init__(self):
        # Dependency graph
        self._graph: dict[Klass, set[Klass]] = defaultdict(set)

    def add(self, cls: type | str) -> None:
        klass: Klass = create_klass(cls)


@functools.cache
def get_modules() -> Mapping[str, Type]:
    locals_dct: dict[str, Type] = {}
    for module_name in ["pyxel.detectors"]:
        module = importlib.import_module(module_name)
        locals_dct |= dict(inspect.getmembers(module, predicate=inspect.isclass))

    return locals_dct


@functools.cache
def get_class(name: str) -> tuple[ClassDescription, dict[str, set[str]]]:
    locals_dct: Mapping[str, type] = get_modules()

    assert name in locals_dct
    cls = locals_dct[name]
    assert inspect.isclass(cls)

    graph: dict[str, set[str]] = defaultdict(set)
    # from pyxel.detectors import APD, CCD, CMOS, MKID

    # TODO: Refactor this into a function '.get_detectors()'
    # classes:Sequence = (APD,CCD,CMOS,MKID)

    # Build a dependency graph
    # graph: Mapping[Klass, set[Klass]] = defaultdict(set)

    # DEBUG
    # cls = APD

    # Extract Base class
    assert inspect.isclass(cls)
    _, *base_classes, _ = inspect.getmro(cls)

    base_description: ClassDescription | None = None
    if base_classes:
        assert len(base_classes) == 1
        base_cls = base_classes[0]

        base_description, base_graph = get_class(name=base_cls.__name__)
        graph |= base_graph

    # Extract documentation
    doc: str | None = inspect.getdoc(cls)
    assert doc is not None
    doc_numpy = NumpyDocString(doc)
    doc_summary, *_ = doc_numpy["Summary"]

    # TODO: Extract this

    # Extract signature
    signature: inspect.Signature = inspect.signature(
        cls,
        locals=locals_dct,
        eval_str=True,
    )

    dct: dict = {}
    for param_name, parameter in signature.parameters.items():
        # get_type_hints, get_args, get_origin
        print(f"{get_origin(parameter.annotation)=}")
        print(f"{parameter.annotation=}, {parameter.annotation.__name__=}")

        # annotation = parameter.annotation
        match parameter.annotation:
            case annotation if getattr(annotation, "__name__", None) in locals_dct:
                cls_description, cls_graph = get_class(annotation.__name__)

                print("Hello World")

            case annotation if get_origin(annotation) == typing.Union:
                match get_origin(annotation):
                    case typing.Union:

                        match get_args(annotation):
                            case (cls_opt, NONE_TYPE) if cls_opt.__name__ in locals_dct:
                                cls_description, cls_graph = get_class(cls_opt.__name__)

                                dct[param_name] = cls_description
                                graph |= cls_graph
                                graph[name].add(cls_opt.__name__)

                            # case [*more_cls]:
                            #     raise NotImplementedError

                            case other:
                                dct[param_name] = Union[other]

                    case _:
                        raise NotImplementedError

        # match get_origin(annotation):
        #     case typing.Union:
        #
        #         match get_args(annotation):
        #             case (
        #                 optional_cls,
        #                 NONE_TYPE,
        #             ) if optional_cls.__name__ in locals_dct:
        #                 cls_description, cls_graph = get_class(optional_cls.__name__)
        #
        #                 dct[param_name] =cls_description
        #                 graph |= cls_graph
        #                 graph[name].add(optional_cls.__name__)
        #                 print("Hello")
        #                 # else:
        #                 #     dct[name] = optional_cls | None
        #                 #     print("Hello")
        #
        #             # case [*more_cls]:
        #             #     raise NotImplementedError
        #
        #             case other:
        #                 dct[param_name] = Union[other]
        #
        #     case _:
        #         raise NotImplementedError

        # foo = get_class(name=parameter.annotation.__name__)
        return (
            ClassDescription(
                base_cls=base_description, doc=doc_summary, parameters=dct
            ),
            graph,
        )

    baz = signature.parameters["geometry"]

    print("Hello World")
    print("Hello World")


def generate_code() -> Iterator[str]:
    # TODO: Generate classes (Detector, ...)
    # TODO: Generate ModelGroups
    # TODO: Generate Models
    get_class(name="APD")
    pass


def create_auto_generated(filename: Path) -> None:
    """Create an auto-generated file."""
    with Path(filename).open("w") as fh:
        for line in tqdm(generate_code()):
            fh.write(f"{line}\n")


@click.command()
@click.option(
    "-f",
    "--filename",
    default="./auto_generated.py",
    type=click.Path(),
    help="Auto generated filename.",
    show_default=True,
)
@click.version_option(version=__version__)
def main(filename: Path):
    """Create an auto-generated file."""
    create_auto_generated(filename)


if __name__ == "__main__":
    main()
