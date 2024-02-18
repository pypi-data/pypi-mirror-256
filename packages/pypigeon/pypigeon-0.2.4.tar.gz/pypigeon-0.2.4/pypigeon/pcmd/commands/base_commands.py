import argparse
import json
import textwrap
import types
from typing import Any
from typing import Callable

import yaml
from pypigeon.client import PigeonClient


class BaseCommands:
    _func_args: dict[Callable[..., None], list[tuple[tuple[Any, ...], dict[str, Any]]]]

    def __init__(self, client: PigeonClient, args: argparse.Namespace) -> None:
        self.client = client
        self.core = client._client
        self.args = args

    def _output(self, data: Any) -> None:
        if self.args.output_type == "yaml":
            print(yaml.dump(data))

        elif self.args.output_type == "json":
            print(json.dumps(data, indent=2))

        else:
            raise ValueError(f"unknown output type: {self.args.output_type}")

    @classmethod
    def _add_to_parser(
        cls, subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]"
    ) -> None:
        for method in dir(cls):
            if method.startswith("_"):
                continue

            action = getattr(cls, method)
            action_doc = action.__doc__ if action.__doc__ is not None else ""
            help_line = (
                action_doc.splitlines()[0].strip().rstrip(".") if action_doc else ""
            )
            parser = subparsers.add_parser(
                method.replace("_", "-"),
                help=help_line,
                description=(
                    help_line
                    + "\n\n"
                    + textwrap.dedent("\n".join(action_doc.split("\n")[1:]))
                ),
                formatter_class=argparse.RawDescriptionHelpFormatter,
            )

            if type(action) == type(object) and issubclass(action, BaseCommands):
                action._add_to_parser(parser.add_subparsers(title="subcommands"))

            elif isinstance(action, types.FunctionType):
                if hasattr(cls, "_func_args"):
                    for args, kwargs in cls._func_args.get(action, []):
                        parser.add_argument(*args, **kwargs)
                parser.set_defaults(cls=cls, func=action)

    @classmethod
    def _with_arg(cls, *args: Any, **kwargs: Any) -> Callable[..., Callable[..., None]]:
        def _inner(func: Callable[..., None]) -> Callable[..., None]:
            if not hasattr(cls, "_func_args"):
                cls._func_args = {}
            cls._func_args.setdefault(func, []).insert(0, (args, kwargs))
            return func

        return _inner
