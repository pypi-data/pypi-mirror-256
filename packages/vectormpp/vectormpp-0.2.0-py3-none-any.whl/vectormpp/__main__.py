import os, sys, shutil, argparse, logging, traceback, multiprocessing
from datetime import datetime
from vectormpp.loggers import initCentralLogger, initWorkerLogger
from vectormpp.executor import Executor
from vectormpp.manifest import Manifest
from vectormpp import __version__

class CustomAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            setattr(namespace, self.dest, values)
        else:
            setattr(namespace, self.dest, ['all'])

def main():
    parser = argparse.ArgumentParser(description = 'Actian VectorMPP Installer', allow_abbrev = False)
    parser.add_argument('-m', "--manifest", dest = 'workdir', default = "", type = str, help = 'the Actian Manifest Directory, if not specified, use The Current Working Directory.')
    parser.add_argument('-r', "--rundir", default = "", type = str, help = 'the Directory containing runtime files, if not specified, use "The Actian Manifest Directory/runs/TIMESTAMP".')
    parser.add_argument('-l', "--loglevel", default = "info", choices = ['debug', 'info', 'warning', 'error'], help = 'verbose Level')
    parser.add_argument('-s', '--set', action='append', type=lambda kv: kv.split("="), dest='settings', help='overwrite fields in Actian VectorMPP Manifest')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', "--install", "--upgrade", "--install_or_upgrade", dest = "install_or_upgrade", nargs='*', action = CustomAction, help = 'install/upgrade Resource(s)')
    group.add_argument('-u', "--uninstall", nargs = '*', action = CustomAction, help = 'uninstall Resource(s)')
    group.add_argument('-g', "--graph", help=argparse.SUPPRESS, action = "store_true")
    parser.add_argument('-v', "--version", action = "store_true", help = 'print the Version of The VectorMPP Installer')
    args = parser.parse_args()

    if len(sys.argv) == 1 or not (args.install_or_upgrade or args.uninstall or args.graph or args.version):
        parser.print_help()
        parser.exit()

    if args.version:
        print(__version__)
        return

    if not args.workdir:
        args.workdir = os.getcwd()
    if not args.rundir:
        args.rundir = os.path.join(args.workdir, 'runs', datetime.now().strftime("%Y%m%d-%H-%M-%S"))
        os.makedirs(args.rundir, exist_ok=True)

    logger_queue = multiprocessing.Queue(-1)
    logger_process = multiprocessing.Process(target = initCentralLogger, args = (logger_queue, args.rundir, args.loglevel), name = "LogProcess")
    logger_process.start()

    try:
        code = 1
        initWorkerLogger(logger_queue)
        logger = logging.getLogger(__name__)
        logger.info(f"{multiprocessing.current_process().name} starts.")
        logger.info(f"Working Directory: {args.workdir}.")

        if not shutil.which("helm"):
            logger.error("Cannot find 'helm' executable")
            return
        if not shutil.which("kubectl"):
            logger.error("Cannot find 'kubectl' executable")
            return

        manifest = Manifest(args.workdir, args.rundir, args.settings)
        if not manifest.initialise():
            return

        if args.graph:
            manifest.print_graph()
            code = 0
            return

        if args.uninstall:
            action = "uninstall"
            manifest.reverse_dependencies()
            manifest.set_targets(args.uninstall)
        else:
            action = "install_or_upgrade"
            manifest.set_targets(args.install_or_upgrade)

        executor = Executor(manifest.generate_shared_resources(), logger_queue)
        processes = [multiprocessing.Process(target = executor.start, args = (action,), name = f"ProcessNo.{i}") for i in range(3)]
        for process in processes:
            process.start()
        for process in processes:
            process.join()
        if not executor.event.is_set():
            code = 0
    except Exception as e:
        logger.error(f"Receive Exception:\n{traceback.format_exc().strip()}")
    finally:
        logger.info(f"{multiprocessing.current_process().name} ends.")
        logger.info(f"Detailed Logs: {os.path.join(args.rundir, 'log', 'vectormpp.log')}")
        logger_queue.put(None)
        logger_process.join()
        sys.exit(code)

if __name__ == '__main__':
    main()
