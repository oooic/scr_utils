from absl import app
from absl import flags
import time
from os.path import expanduser
import os
import signal
from .mv_screenshot import mv_default
from .settings import init, change_savedir, change_jikanwari
from .daemonize import interval_run, start_daemon, log_to_stdout


FLAGS = flags.FLAGS
flags.DEFINE_bool(
    'reset',
    False,
    'reset all settings of this program',
    short_name='r')
flags.DEFINE_bool(
    'settings',
    False,
    'edit save directory',
    short_name='es')
flags.DEFINE_bool(
    'jikanwari',
    False,
    'edit jikanwari',
    short_name='ej')
flags.DEFINE_bool(
    'startdaemon',
    False,
    'daemonize program',
    short_name='start')
flags.DEFINE_bool(
    'stopdaemon',
    False,
    'stop daemon',
    short_name='kill')
flags.DEFINE_bool(
    'test',
    True,
    'test',
    short_name='t')


def screenshot_daemon(arg=None, kws=None, pf=log_to_stdout):
    while True:
        mv_default()
        time.sleep(60)


home = expanduser("~")
base = os.path.join(home, ".myscreenshot")

start_daemon = start_daemon(log_to_stdout)
screenshot_daemon = interval_run(1)(screenshot_daemon)


def main(argv):
    if flags.jikanwari:
        change_jikanwari()
        return 0
    if flags.reset:
        init()
    if flags.settings:
        change_savedir()
    if flags.test:
        mv_default()
    if flags.startdaemon:
        start_daemon(
            screenshot_daemon,
            'screenshot_daemon',
            pidpath=os.path.join(base, "python_daemon.pid"),
            logpath=os.path.join(base, "python_daemon.log"),
            kws=None
        )
    elif flags.stopdaemon:
        with open(os.path.join(base, "python_daemon.pid"), "rb") as f:
            pid = f.read().rstrip()
        os.kill(int(pid), signal.SIGKILL)


if __name__ == '__main__':
    app.run(main)
