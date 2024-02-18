"""This module performs functional tests of the pyg3t tools."""

import os
from pathlib import Path
import subprocess

import pytest


@pytest.fixture(scope='session')
def files():
    return Files(Path(__file__).parent.resolve())


class Files:
    def __init__(self, path):
        self.path = path
        self.datafiles = path / 'datafiles'

    @property
    def testpofile(self):
        return self.datafiles / 'testpofile.da.po'

    @property
    def testpodiff(self):
        return self.datafiles / 'testpodiff.podiff'

    def reference(self, name):
        return (self.datafiles / f'expected_outputs/{name}.out').read_text()

    @property
    def patched(self):
        return self.datafiles / 'patched.po'

    @property
    def old(self):
        return self.datafiles / 'old.po'

    @property
    def new(self):
        return self.datafiles / 'new.po'

    @property
    def testwdiff(self):
        return self.datafiles / 'testpodiff_gtwdiff.podiff'

    def relpath(self, path):
        return path.relative_to(self.datafiles)

    def run_command(self, command_args):
        """Run a command

        Args:
            command_args (list): List of command arguments e.g. ['ls', '-l']

        Returns:
            tuple: (return_code (int), stdout (str), stderr (str))
        """
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   cwd=self.datafiles,
                                   encoding='utf-8')
        stdout, stderr = process.communicate()
        process.wait()
        return process.returncode, stdout, stderr

    def standardtest(self, command_args, expected, return_code=0):
        """Perform the standard tests on a command.

        The standard tests consist of making sure that the return_code is as
        expected, that stderr is empty and that stdout has the expected value.
        """
        return_code_actual, stdout, stderr = self.run_command(command_args)

        if 'pyg3t_save_output' in os.environ:
            raise NotImplementedError

            # XXX Needs update
            with open('{0}_expected_output'.format(
                    command_args[0]), 'w') as fd:
                fd.write(stdout)
            return

        assert return_code_actual == return_code
        assert stderr == ''
        assert stdout == expected


def test_gtcat(files):
    process1 = subprocess.Popen(
        ['gtcat', '--encode', 'ISO-8859-1', files.old],
        stdout=subprocess.PIPE, cwd=files.path,
        encoding='utf-8',
    )
    # XXX Why does this not fail if it wants files.old inside files.path?

    process2 = subprocess.Popen(
        ['podiff', '-r', '-', files.relpath(files.new)], stdin=process1.stdout,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=files.datafiles,
        encoding='utf-8',
    )
    # Forward output
    process1.stdout.close()
    # Wait for process to close and set return code and check it
    process1.wait()
    assert process1.returncode == 0

    # Get final stdout and stderr
    stdout, stderr = process2.communicate()
    # Check return code
    process2.wait()
    assert process2.returncode == 0
    # Check stderr and stdout
    assert stderr == ''
    assert stdout == files.reference('gtcat')


def test_gtcheckargs(files):
    files.standardtest(
        ['gtcheckargs', files.testpofile],
        files.reference('gtcheckargs'),
        return_code=1)


def test_gtcompare(files):
    files.standardtest(
        ['gtcompare', files.testpofile, files.testpofile],
        files.reference('gtcompare'))


def test_gtgrep(files):
    files.standardtest(
        ['gtgrep', '-i', 'hello', '-s', 'hej', files.testpofile],
        files.reference('gtgrep'))


def test_gtmerge(files):
    files.standardtest(['gtmerge', files.testpofile, files.testpofile],
                       files.reference('gtmerge'))


def test_gtprevmsgdiff(files):
    files.standardtest(['gtprevmsgdiff', files.testpofile],
                       files.reference('gtprevmsgdiff'))


def test_gtwdiff(files):
    return_code, stdout, stderr = files.run_command(
        ['gtwdiff', files.testwdiff]
    )
    assert return_code == 0
    assert stderr == ''

    # We have problems with the diff coming out in different order on
    # different Python versions, so test for correct in and out but
    # not for the same order
    new_pattern = '\x1b[1;33;42m'
    old_pattern = '\x1b[1;31;41m'
    stop_pattern = '\x1b[0m'

    def parse_wdiff(text):
        out = {'new': '', 'old': '', 'unchanged': ''}
        state = 'unchanged'
        while text:
            if text.startswith(new_pattern):
                state = 'new'
                text = text.replace(new_pattern, '', 1)
            elif text.startswith(old_pattern):
                state = 'old'
                text = text.replace(old_pattern, '', 1)
            elif text.startswith(stop_pattern):
                state = 'unchanged'
                text = text.replace(stop_pattern, '', 1)
            else:
                out[state] += text[0:1]
                text = text[1:]
        return out
    from_stdout = parse_wdiff(stdout)
    from_expected = parse_wdiff(files.reference('gtwdiff'))
    assert from_stdout['new'] == from_expected['new']
    assert from_stdout['old'] == from_expected['old']
    assert from_stdout['unchanged'] == from_expected['unchanged']


def test_gtxml(files):
    # Need relative path here since it'll be included in the text output
    # and we wouldn't want it machine dependent:
    files.standardtest(['gtxml', files.relpath(files.testpofile)],
                       files.reference('gtxml'),
                       return_code=1)


def test_poabc(files):
    files.standardtest(['poabc', files.testpofile], files.reference('poabc'))


def test_podiff(files):
    files.standardtest(['podiff', '--relax',
                        files.relpath(files.old), files.relpath(files.new)],
                       files.reference('podiff'))


def test_popatch(files, tmp_path):
    """Functional test for popatch"""
    return_code, stdout, stderr = files.run_command(
        ['popatch', files.testpofile, files.testpodiff])
    assert return_code == 0
    assert stderr == ''

    patched = tmp_path / 'patched.po'
    patched.write_text(stdout)

    return_code, stdout, stderr = files.run_command(
        ['popatch', '--new', files.testpodiff])
    assert return_code == 0
    assert stderr == ''

    patched_new = tmp_path / 'patched.new.po'
    patched_new.write_text(stdout)

    return_code, stdout, stderr = files.run_command(
        ['popatch', '--old', files.testpodiff])
    assert return_code == 0
    assert stderr == ''

    patched_old = tmp_path / 'patched.old.po'
    patched_old.write_text(stdout)

    return_code, stdout, stderr = files.run_command(
        ['podiff', '-rf', patched_old, patched_new])
    assert return_code == 0
    assert stderr == ''

    with open(files.testpodiff) as fd:
        lines_diff = fd.readlines()

    lines_stdout = stdout.strip().split('\n')
    for line1, line2 in zip(lines_diff, lines_stdout):
        if line1.startswith('---'):
            continue
        assert line1 == line2 + '\n'


def test_poselect(files):
    files.standardtest(['poselect', '-ft', files.testpofile],
                       files.reference('poselect'))
