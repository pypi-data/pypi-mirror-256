# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0212,W0611,W0613,E0401


"runtime"


import getpass
import inspect
import os
import pwd
import readline
import sys
import termios
import time
import _thread


from .configs import Cfg


from . import Client, Command, Default, Error, Event, Object, Storage
from . import cdir, debug, launch, parse_cmd, spl, scan, update


def __dir__():
    return (
        'Console',
        'cmnd',
        'daemon',
        'forever',
        'main',
        'privileges',
        'wrap',
        'wrapped'
    )


__all__ = __dir__()


Storage.wd  = Cfg.wd


from . import modules


class Console(Client):

    def announce(self, txt):
        pass

    def callback(self, evt):
        Client.callback(self, evt)
        evt.wait()

    def poll(self):
        evt = Event()
        evt.orig = object.__repr__(self)
        evt.txt = input("> ")
        evt.type = "command"
        return evt

    def say(self, channel, txt):
        txt = txt.encode('utf-8', 'replace').decode()
        print(txt)


def checkpid(pid):        
    if not pid:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def cmnd(txt, out):
    clt = Client()
    clt.raw = out
    evn = Event()
    evn.orig = object.__repr__(clt)
    evn.txt = txt
    Command.handle(evn)
    evn.wait()
    return evn


def daemon(pidfile, verbose=False):
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")
    if os.path.exists(pidfile):
        os.unlink(pidfile)
    cdir(os.path.dirname(pidfile))
    with open(pidfile, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def forever():
    while 1:
        try:
            time.sleep(1.0)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def getpid():
    try:
        return int(open(Cfg.pidfile, encoding="utf-8").read())
    except (FileNotFoundError, ValueError):
        return None


def privileges(username):
    pwnam = pwd.getpwnam(username)
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


def wrap(func):
    old2 = None
    try:
        old2 = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    finally:
        if old2:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old2)


def main():
    Storage.skel()
    parse_cmd(Cfg, " ".join(sys.argv[1:]))
    update(Cfg, Cfg.sets)
    Cfg.mod += ",cmd,mod"
    if 'a' in Cfg.opts:
        Cfg.mod = ",".join(modules.__dir__())
    if "v" in Cfg.opts:
        dte = time.ctime(time.time()).replace("  ", " ")
        debug(f"{Cfg.name.upper()} {Cfg.opts.upper()} started {dte}")
    if "h" in Cfg.opts:
        scan(modules, Cfg.mod)
        from . import __doc__ as txt
        print(txt)
        return
    if "c" in Cfg.opts:
        scan(modules, Cfg.mod, True, Cfg.dis, True)
        csl = Console()
        csl.start()
        forever()
    if Cfg.otxt:
        Cfg.mod = ",".join(modules.__dir__())
        scan(modules, Cfg.mod, False, Cfg.sets.dis, False)
        return cmnd(Cfg.otxt, print)
    if checkpid(getpid()):
        print("daemon is already running.")
        return
    Cfg.mod = ",".join(modules.__dir__())
    daemon(Cfg.pidfile)
    privileges(Cfg.user)
    scan(modules, Cfg.mod, True, Cfg.dis, True)
    forever()


def wrapped():
    wrap(main)
    if "d" not in Cfg.opts:
        Error.show()


if __name__ == "__main__":
    wrapped()
