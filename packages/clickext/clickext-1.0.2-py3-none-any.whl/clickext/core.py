"""
clickext.core

Extended functionality for the click library.
"""

import typing as t

import click


__all__ = ["ClickextCommand", "ClickextGroup"]


class ClickextCommand(click.Command):
    """A clickext command.

    Clickext commands support aliases and marking options as mutually exclusive.

    Aliases have no effect unless the command is a subcommand in a `ClickextGroup`.

    Mutually exclusive options are validated before invoking the command. Validation fails when all of the mutually
    exclusive options are passed as arguments and one or more options has a value other than its default.

    :param aliases: Alternate names that should invoke this command.
    :param mx_opts: Groups of options that are mutually exclusive. Each item is a `tuple` of `click.Option` names that
    cannot be used together, e.g, `[("foo", "bar")]`.
    :param attrs: Extra arguments passed to `click.Command`.
    """

    def __init__(
        self,
        name: t.Optional[str] = None,
        aliases: t.Optional[list[str]] = None,
        mx_opts: t.Optional[list[tuple[str]]] = None,
        **attrs: t.Any,
    ):
        super().__init__(name, **attrs)

        self.aliases = sorted(aliases or [])
        self.mx_opts = mx_opts or []
        self.global_opts: dict[str, click.Option] = {}

    def parse_args(self, ctx: click.Context, args: t.List[str]) -> t.List[str]:
        """Parse arguments and update the context.

        Mutually exclusive options are validated after parsing because the resolved values are required to determine
        which were options passed and which are using default values.

        :param ctx: The current `click.Context` object.
        :param args: A list of arguments passed to the program.
        """
        args = super().parse_args(ctx, args)
        self.validate_mutually_exclusive_options(ctx)
        return args

    def validate_mutually_exclusive_options(self, ctx: click.Context) -> None:
        """Ensure mutually exclusive options have not been passed as arguments.

        Validation must be done after the arguments are parsed so only the options relevant to the command are
        considered and the resolved values can be compared to the default value for each option.

        :param ctx: The current `click.Context` object.

        :raises click.UsageError: When mutually exclusive options have been passed.
        """
        for mx_opts in self.mx_opts:
            passed = []

            for param in self.get_params(ctx):
                if param.name in mx_opts and param.name in ctx.params and ctx.params[param.name] != param.default:
                    passed.append(param.opts[0])

                    if len(passed) == len(mx_opts):
                        raise click.UsageError(f"Mutually exclusive options: {' '.join(passed)}", ctx)

    def list_global_options(self) -> list[click.Option]:
        """Get a list of global options registered with the command."""
        return list(self.global_opts.values())

    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """Writes the help into the formatter if it exists.

        :param ctx: The current `click.Context` object.
        :param formatter: The help output formatter.
        """
        super().format_help(ctx, formatter)
        self.format_aliases(ctx, formatter)

    def format_options(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """Add options to the program help display.

        Options are sorted alphabetically by the first CLI option string. If the command is part of a `ClickextGroup`
        global group options are included in the option display.

        :param ctx: The current `click.Context` object.
        :param formatter: The help output formatter.
        """
        params = self.get_params(ctx)

        if ctx.parent and not isinstance(self, ClickextGroup):
            params.extend(self.list_global_options())

        params.sort(key=lambda x: x.opts[0])

        opts = []

        for param in params:
            record = param.get_help_record(ctx)
            if record is not None:
                opts.append(record)

        if opts:  # pragma: no branch
            with formatter.section("Options"):
                formatter.write_dl(opts)

    def format_aliases(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """Add aliases to the program help display when command is a subcommand.

        :param ctx: The current `click.Context` object.
        :param formatter: The help output formatter.
        """
        if ctx.parent:
            aliases = []

            for alias in self.aliases:
                aliases.append((alias, ""))

            if aliases:
                with formatter.section("Aliases"):
                    formatter.write_dl(aliases)


class ClickextGroup(ClickextCommand, click.Group):
    """A clickext command group.

    Clickext command groups require `ClickextCommand` command instances. Groups support aliases, global options, shared
    subcommand options, and mutually exclusive options.

    Global options are options defined at the group level that may be passed as arguments to the group command
    and all subcommands in the group. Typically these options are used to change configuration or execution globally
    (e.g., to set verbosity level). Global options are extracted and prepended to the arguments prior to argument
    parsing; they are not passed to subcommands and must not be part of a subcommand function signature.

    Global option names cannot be the same as a subcommand name, subcommand option name, or share long/short option
    strings with a subcommand option. Additionally, non-flag global options should not accept values that begin with "-"
    or values identical to a subcommand name. Global options can be mutually exclusive with other group-level options,
    but not with subcommand options.

    Shared parameters are parameters defined at the group level that are attached to all subcommands in the group. These
    parameters cannot be passed to the group itself. Shared parameter names cannot be the same as a subcommand parameter
    name or share long/short option strings with a subcommand option. Shared parameters cannot be mutually exclusive
    with global options, but can be mutually exclusive with non-shared subcommand parameters.

    :param global_opts: `click.Option` names that can be passed to the group and all subcommands in the group.
    :param shared_params: `click.Parameter` names that can be passed to all subcommands in the group, but not the group
    itself.
    :param attrs: Extra arguments passed to `ClickextCommand` and `click.Group`.
    """

    def __init__(
        self,
        name: t.Optional[str] = None,
        global_opts: t.Optional[list[str]] = None,
        shared_params: t.Optional[list[str]] = None,
        **attrs: t.Any,
    ):
        super().__init__(name, **attrs)

        self.global_opts: dict[str, click.Option] = self.init_global_options(global_opts)
        self.shared_params: dict[str, click.Parameter] = self.init_shared_params(shared_params)

    def init_global_options(self, names: t.Optional[list[str]] = None) -> dict[str, click.Option]:
        """Find and validate global options for the group.

        :param names: A list of `click.Option` names to make global.

        :raises ValueError: When an option with the given name does not exist.
        :raises TypeError: When a parameter is not a `click.Option`.
        """
        names = names or []
        options: dict[str, click.Option] = {}

        for name in names:
            param = next((p for p in self.params if p.name == name), None)

            if not param:
                raise ValueError(f"Unknown global option {name}")

            if not isinstance(param, click.Option):
                raise TypeError(f"Invalid global option {name}; global options must be a 'click.Option'")

            options[name] = param

        return options

    def init_shared_params(self, names: t.Optional[list[str]] = None) -> dict[str, click.Parameter]:
        """Find, extract, and validate shared subcommand parameters from the group parameters.

        :param names: A list of parameter names to share with all subcommands.

        :raises ValueError: When a parameter with the given name does not exist.
        """
        names = names or []
        params: dict[str, click.Parameter] = {}

        for name in names:
            param = next((p for p in self.params if p.name == name), None)

            if not param:
                raise ValueError(f"Unknown shared parameter {name}")

            params[name] = param

        # subcommand parameters cannot be passed to the group
        self.params = [p for p in self.params if p.name not in names]

        return params

    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        """Parse arguments and update the context.

        Global options are extracted and prepended to the argument list before parsing.

        :param ctx: The current `click.Context` object.
        :param args: A list of arguments passed to the program.
        """
        args = self.parse_global_args(args)
        return super().parse_args(ctx, args)

    def parse_global_args(self, args: list[str]) -> list[str]:
        """Parse global arguments and update the argument order.

        Global options are extracted from the raw arguments and prepended to raw arguments to be consumed by the group.

        :param args: A list of arguments passed to the program.
        """
        grp_args: list[str] = []
        cmd_args: list[str] = []

        next_idx = 0
        for idx, arg in enumerate(args):
            # skip arguments consumed as values for a global option
            if idx != next_idx:
                continue

            gopt = next((go for go in self.list_global_options() if arg in go.opts), None)

            if gopt:
                grp_args.append(arg)

                value_idx = idx + 1
                if not gopt.is_flag and value_idx < len(args):
                    if not args[value_idx].startswith("-") and args[value_idx] not in self.commands:
                        grp_args.append(args[value_idx])
                        next_idx += 1
            else:
                cmd_args.append(arg)

            next_idx += 1

        return [*grp_args, *cmd_args]

    def add_command(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, cmd: ClickextCommand, name: t.Optional[str] = None
    ) -> None:
        """Register a command with this group.

        The command must be a `ClickextCommand`. Global options are stored separately on the command so they are
        available in the program help display.

        :param cmd: A `ClickextCommand` to add to the group.
        :param name: The command name.
        :raises TypeError: When a command that is not a `ClickextCommand` is added to the group.
        """
        if not isinstance(cmd, ClickextCommand):
            raise TypeError("Only 'ClickextCommand's can be registered with a 'ClickextGroup'")

        name = name or cmd.name

        if name is not None:  # pragma: no branch
            self.validate_command(cmd, name)
            cmd.global_opts = self.global_opts
            cmd.params.extend(self.list_shared_parameters())

        super().add_command(cmd, name)

    def get_command(self, ctx: click.Context, cmd_name: str) -> t.Optional[ClickextCommand]:
        """Get a command by name or alias.

        :param ctx: The current `click.Context` object.
        :param name: The command name.
        """
        for name, cmd in self.commands.items():
            if cmd_name == name or cmd_name in getattr(cmd, "aliases", []):
                cmd_name = name
                break

        return super().get_command(ctx, cmd_name)  # pyright: ignore[reportReturnType]

    def validate_command(self, cmd: ClickextCommand, name: str) -> None:
        """Validate global options and shared parameters for a command.

        :param cmd: A `ClickextCommand` to validate.
        :param name: The command name.

        :raises ValueError: When the command name is the same as a global option name, or a command parameter conflicts
        with a global option, shared parameter name, or option string.
        """
        if name in self.global_opts:
            raise ValueError(f"Subcommand {name} conflicts with a global option name")

        for param in cmd.params:
            if param.name in self.global_opts:
                raise ValueError(f"Subcommand option {param.name} conflicts with a global option name")

            if param.name in self.shared_params:
                raise ValueError(
                    f"Subcommand {param.param_type_name} {param.name} conflicts with a shared parameter name"
                )

            for opt in param.opts:
                if any(opt in gopt.opts for gopt in self.list_global_options()):
                    raise ValueError(f"Subcommand option string {opt} conflicts with a global option string")

                if any(opt in sopt.opts for sopt in self.list_shared_parameters()):
                    raise ValueError(f"Subcommand option string {opt} conflicts with a shared option string")

    def list_shared_parameters(self) -> list[click.Parameter]:
        """Get a list of parameters shared with all subcommands."""
        return list(self.shared_params.values())

    def format_commands(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """Add subcommands to the program help display.

        :param ctx: The current `click.Context` object.
        :param formatter: The help output formatter.
        """
        commands: list[tuple[str, click.Command]] = []

        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)

            if cmd is None or cmd.hidden:
                continue

            aliases = getattr(cmd, "aliases", [])

            if aliases:
                subcommand = f"{subcommand} ({','.join(aliases)})"

            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if commands:
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)
            rows = []

            for subcommand, cmd in commands:
                cmd_help = cmd.get_short_help_str(limit)
                rows.append((subcommand, cmd_help))

            if rows:  # pragma: no branch
                with formatter.section("Commands"):
                    formatter.write_dl(rows)

    def format_options(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """Add options and commands to the program help display.

        Options are sorted alphabetically by the first CLI option string.

        :param ctx: The current `click.Context` object.
        :param formatter: The help output formatter.
        """
        super().format_options(ctx, formatter)
        self.format_commands(ctx, formatter)
