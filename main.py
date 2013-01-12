import actions
from version import __version__
from commando import Application, command, store, subcommand, true, version
from fswrap import File
from gitbot.util import getLoggerWithConsoleHandler
import yaml


logger = getLoggerWithConsoleHandler('gitbot-builder')


class Engine(Application):

    def __init__(self, raise_exceptions=False):
        self.raise_exceptions = raise_exceptions
        super(Engine, self).__init__()

    def run(self, args=None):
        """
        The engine entry point.
        """

        # Catch any errors thrown and log the message.

        try:
            super(Engine, self).run(args)
        except Exception, e:
            if self.raise_exceptions:
                raise
            elif self.__parser__:
                self.__parser__.error(e.message)
            else:
                logger.error(e.message)
                return -1

    @command(description='gitbot-builder - Create or update a gitbot stack',
        epilog='Use %(prog)s {command} -h to get help on individual commands')
    @true('-v', '--verbose', help="Show detailed information in console")
    @version('--version', version='%(prog)s ' + __version__)
    def main(self, args):
        print 'args=', args
        pass

    @subcommand('www',
        help='Generates and pushes the www project.')
    @store('-c', '--config', default='data.yaml', help="Config file")
    def www(self, args):
        data = yaml.load(File(args.config).read_all())
        actions.www(data)

    @subcommand('api',
        help='Generates and pushes the api project.')
    @store('-c', '--config', default='data.yaml', help="Config file")
    def api(self, args):
        data = yaml.load(File(args.config).read_all())
        actions.app(data)

    @subcommand('all',
        help='Generates and pushes the both projects.')
    @store('-c', '--config', default='data.yaml', help="Config file")
    def all(self, args):
        data = yaml.load(File(args.config).read_all())
        actions.all(data)

    @subcommand('refresh',
        help='Generates both the projects only if needed.')
    @store('-c', '--config', default='data.yaml', help="Config file")
    def refresh(self, args):
        data = yaml.load(File(args.config).read_all())
        actions.refresh(data)


def main():
    """Main"""
    Engine(raise_exceptions=True).run()

if __name__ == "__main__":
    main()
