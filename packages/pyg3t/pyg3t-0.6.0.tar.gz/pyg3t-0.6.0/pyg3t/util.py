from codecs import lookup, StreamReaderWriter
import io
import re
import sys


def regex(pattern, flags=0):
    assert flags & re.UNICODE == 0
    flags |= re.UNICODE
    return re.compile(pattern, flags)


_colors = {'blue': '0;34',
           'light red': '1;31',
           'light purple': '1;35',
           'brown': '0;33',
           'purple': '0;35',
           'yellow': '1;33',
           'dark gray': '1;30',
           'light cyan': '1;36',
           'black': '0;30',
           'light green': '1;32',
           'cyan': '0;36',
           'green': '0;32',
           'light blue': '1;34',
           'light gray': '0;37',
           'white': '1;37',
           'red': '0;31',
           'old': '1;30;41',  # To do: proper names, reorganize
           'new': '1;37;42',  # These are used by gtprevmsgdiff
           None: None}


def _ansiwrap(string, id):
    if id is None:
        return string
    tokens = []
    for line in string.split('\n'):
        if len(line) > 0:
            line = '\x1b[%sm%s\x1b[0m' % (id, line)
        tokens.append(line)
    return '\n'.join(tokens)


def noansi(string):
    return ansipattern.sub('', string)


class ANSIColors:
    def get(self, name):
        color = _colors[name.replace('_', ' ')]

        def colorize(string):
            return _ansiwrap(string, color)
        return colorize

    __getitem__ = get
    __getattr__ = get


ansi_nocolor = '\x1b[0m'
ansipattern = regex('\x1b\\[[;\\d]*[A-Za-z]')
ansi = ANSIColors()


class NullDevice:
    def write(self, txt):
        pass


def get_bytes_output(name='-'):
    if name == '-':
        return sys.stdout.buffer
    else:
        try:
            return io.open(name, 'wb')
        except IOError as err:
            raise PoError('open-bytes-output', str(err))


def get_bytes_input(name='-'):
    if name == '-':
        return sys.stdin.buffer
    else:
        try:
            return io.open(name, 'rb')
        except IOError as err:
            raise PoError('open-bytes-input', str(err))


def get_encoded_output(encoding, name='-', errors='strict'):
    if name == '-':
        return _srw(sys.stdout.buffer, encoding, errors=errors)
    else:
        try:
            return io.open(name, 'w', encoding=encoding, errors=errors)
        except IOError as err:
            raise PoError('open-encoded-output', str(err))


def _srw(fd, encoding, errors='strict'):
    info = lookup(encoding)
    srw = StreamReaderWriter(fd, info.streamreader, info.streamwriter,
                             errors=errors)
    return srw


class PoError(Exception):
    def __init__(self, errtype, *args, **kwargs):
        # errtype is a unique short string identifying the error.
        # It is used to distinguish different errors by the test suite.
        self.errtype = errtype
        self.lineno = None
        self.fname = None
        self.exitcode = 2  # Default to 2 because OptionParser.error() does.
        super(PoError, self).__init__(*args, **kwargs)

    # Subclasses should override this
    def get_errmsg(self):
        tokens = []
        tokens.append(super(PoError, self).__str__())
        if self.fname is not None:
            tokens.append('\n')
            tokens.append('File: %s\n' % self.fname)
        if self.lineno is not None:
            tokens.append('Line: %d\n' % self.lineno)
        return ''.join(tokens)

    # Subclasses should leave this alone
    def __str__(self):
        return self.get_errmsg()


def pyg3tmain(build_parser):
    """Decorator for pyg3t main functions.

    Use like this:

        def build_parser():
            return OptionParser(...)

        @pyg3tmain(build_parser)
        def main(parser):
            ...

        main()

    The decorated main function does the following:
     * Decode sys.argv to unicode from locale's preferred encoding in Python2
     * Create parser from build_parser()
     * Run main(parser) where main is the undecorated function
     * Handle known errors gracefully (quit and write intelligible message)

    gtcat is the reference example of how to use it."""
    def main_decorator(main):
        def pyg3tmain():
            try:
                parser = build_parser()
                main(parser)
            except KeyboardInterrupt:
                progname = parser.get_prog_name()
                print('%s: %s' % (progname, 'Interrupted by keyboard'),
                      file=sys.stderr)
            except PoError as err:
                progname = str(parser.get_prog_name())
                print(str('%s: error: %s\n') % (progname, str(err)),
                      file=sys.stderr)
                sys.exit(err.exitcode)
        return pyg3tmain
    return main_decorator
