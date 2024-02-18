from cleo.commands.command import Command
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.console.application import Application
from poetry.core.masonry.builders.sdist import SdistBuilder


class GenerateSetupCommand(Command):
    name = 'generate-setup'
    description = 'Generate setup.py for setuptools'

    def handle(self) -> int:
        builder = SdistBuilder(self.application.poetry)
        setup = builder.build_setup()
        with open('setup.py', 'wb+') as f:
            f.write(setup)

        return 0


def factory():
    return GenerateSetupCommand()


class PoetryPluginGenerateSetup(ApplicationPlugin):
    def activate(self, application: Application):
        application.command_loader.register_factory('generate-setup', factory)
