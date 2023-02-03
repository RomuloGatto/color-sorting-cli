import inspect
from typing import Any, Callable, Dict, Optional, Type, Union

import rich
import typer
from typer import core, models

from harmony import __version__


class HarmonyTyper(typer.Typer):
    """Adapter for `typer.Typer`"""

    # pylint: disable=too-many-locals,redefined-builtin

    def command(
        self,
        name: Optional[str] = None,
        *,
        cls: Optional[Type[core.TyperCommand]] = None,
        context_settings: Optional[Dict[Any, Any]] = None,
        help: Optional[str] = None,
        epilog: Optional[str] = None,
        short_help: Optional[str] = None,
        options_metavar: str = "[OPTIONS]",
        add_help_option: bool = True,
        no_args_is_help: bool = False,
        hidden: bool = False,
        deprecated: bool = False,
        # Rich settings
        rich_help_panel: Union[str, None] = models.Default(None),
    ) -> Callable[[models.CommandFunctionType], models.CommandFunctionType]:
        if cls is None:
            cls = core.TyperCommand

        def decorator(
            command: models.CommandFunctionType,
        ) -> models.CommandFunctionType:
            command.__doc__ = self._add_version(command)

            def print_error_wrapper(*args, **kwargs):
                try:
                    command(*args, **kwargs)

                except Exception as exception:
                    rich.print(f"[bright_red] ERROR: {exception}")
                    raise typer.Exit(code=1)

            print_error_wrapper.__name__ = command.__name__
            print_error_wrapper.__doc__ = command.__doc__
            setattr(print_error_wrapper, "__signature__", inspect.signature(command))

            self.registered_commands.append(
                models.CommandInfo(
                    name=name,
                    cls=cls,
                    context_settings=context_settings,
                    callback=print_error_wrapper,
                    help=help,
                    epilog=epilog,
                    short_help=short_help,
                    options_metavar=options_metavar,
                    add_help_option=add_help_option,
                    no_args_is_help=no_args_is_help,
                    hidden=hidden,
                    deprecated=deprecated,
                    # Rich settings
                    rich_help_panel=rich_help_panel,
                )
            )
            return command

        return decorator

    def _add_version(self, command: Callable[..., None]):
        command_docs = command.__doc__

        if not command_docs:
            command_docs = ""

        return f"*Harmony {__version__} [{command.__name__}]*\n\n{command.__doc__}"
