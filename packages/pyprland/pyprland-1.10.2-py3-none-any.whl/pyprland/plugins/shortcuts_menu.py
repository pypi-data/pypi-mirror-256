" Shortcuts menu "
import asyncio
from asyncio import subprocess

from .interface import Plugin
from ..adapters.menus import MenuRequiredMixin
from ..common import apply_variables


class Extension(MenuRequiredMixin, Plugin):
    "Shows a menu with shortcuts"

    # Commands

    async def run_menu(self, name=""):
        """[name] Shows the menu, if "name" is provided, will only show this sub-menu"""
        await self.ensure_menu_configured()
        options = self.config["entries"]
        if name:
            for elt in name.split("."):
                options = options[elt]

        def _format_title(label, obj):
            if isinstance(obj, dict):
                suffix = self.config.get("submenu_end", "➜")
                prefix = self.config.get("submenu_start", "")
            else:
                suffix = self.config.get("command_end", "")
                prefix = self.config.get("command_start", "")

            return f"{prefix} {label} {suffix}".strip()

        while True:
            if isinstance(options, str):
                self.log.info("running %s", options)
                await self._run_command(options.strip())
                break
            if isinstance(options, list):
                self.log.info("interpreting %s", options)
                await self._handle_chain(options)
                break
            try:
                formatted_options = {_format_title(k, v): v for k, v in options.items()}
                selection = await self.menu.run(formatted_options)
                options = formatted_options[selection]
            except KeyError:
                self.log.info("menu command canceled")
                break

    # Utils

    async def _handle_chain(self, options):
        "Handles a chain of special objects + final command string"
        variables: dict[str, str] = {}
        for option in options:
            if isinstance(option, str):
                await self._run_command(option, variables)
            else:
                choices = []
                var_name = option["name"]
                if option.get("command"):  # use the option to select some variable
                    proc = await asyncio.create_subprocess_shell(
                        option["command"], stdout=subprocess.PIPE
                    )
                    assert proc.stdout
                    await proc.wait()
                    choices.extend(
                        [
                            line.strip()
                            for line in (await proc.stdout.read()).decode().split("\n")
                        ]
                    )
                elif option.get("options"):
                    choices.extend(option["options"])
                variables[var_name] = await self.menu.run(choices)

    async def _run_command(self, command, variables=None):
        "Runs a shell `command`, optionally replacing `variables`"
        self.log.info("Executing %s (%s)", command, variables)
        await asyncio.create_subprocess_shell(
            apply_variables(command, variables) if variables else command
        )
