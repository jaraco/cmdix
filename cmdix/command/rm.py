import pathlib
import stat
import types


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "print name of current/working directory"
    p.add_argument('FILE', nargs='+', type=pathlib.Path)
    p.add_argument(
        "-f",
        "--force",
        action="store_true",
        dest="force",
        help="ignore nonexistent files, never prompt",
    )
    p.add_argument(
        "-r",
        "-R",
        "--recursive",
        action="store_true",
        dest="recursive",
        help="remove directories and their contents recursively",
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="explain what is being done",
    )
    return p


class Handler(types.SimpleNamespace):
    verbose: bool
    force: bool

    @classmethod
    def from_args(cls, args):
        return cls(**vars(args))

    def run(self, path):
        action = self.remove_dir if self.recursive else self.remove_file
        return action(path)

    def remove_dir(self, path):
        """
        Remove directory recursively.
        """
        if not path.is_dir():
            self.remove_file(path)

        for root, subs, files in path.walk():
            for name in files:
                self.remove_file(root / name)
            for name in subs:
                self.remove_dir(root / name)
            subs.clear()

        self.try_op(root, root.rmdir)
        self.verbose and print(root)

    def remove_file(self, path):
        """
        Remove a single file.
        """
        self.try_op(path, path.unlink)
        self.verbose and print(path)

    def try_op(self, path, op):
        exceptions = (OSError,) if self.force else ()
        try:
            op()
        except exceptions:
            path.chmod(stat.S_IWRITE)
            op()


def func(args):
    handler = Handler.from_args(args)
    tuple(map(handler.run, args.FILE))
