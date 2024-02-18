from cleo.events.console_events import COMMAND
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from poetry.console.commands.build import BuildCommand
from poetry.plugins.application_plugin import ApplicationPlugin
import docker


class MyApplicationPlugin(ApplicationPlugin):
    def activate(self, application: Application):
        application.event_dispatcher.add_listener(
            COMMAND, self.load_dotenv
        )

    def load_dotenv(
            self,
            event: ConsoleCommandEvent,
            event_name: str,
            dispatcher: EventDispatcher
    ) -> None:
        command = event.command
        if not isinstance(command, BuildCommand):
            return

        io = event.io
        c = docker.from_env()
        container = c.containers.run('ubuntu', 'ls -lah', detach=True)

        for line in container.logs(stream=True):
            print(line.decode().strip())

        if io.is_debug():
            io.write_line(
                "<debug>Loading environment variables.</debug>"
            )
