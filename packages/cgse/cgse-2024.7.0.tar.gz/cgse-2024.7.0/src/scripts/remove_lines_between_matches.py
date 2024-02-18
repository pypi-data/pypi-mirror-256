"""
This script is intended to be used for log files that contain errors or warnings that completely flood all other
messages and therefore make it very hard to analyse the log. The script will first rename the log-file with a '.orig'
extension and then filters out all lines between a matching start pattern and a matching end pattern.
The filtered output is written into the original file.

Example usage:

    $ python remove_lines_between_matches.py ~/Desktop/general-sron.log.2023-07-14 \
      -sp 'Executing is_connected failed' -ep '^(NotImplementedError|AttributeError)'

This command will filter out all occurrences of the following two error messages:

    level=ERROR ts=2023-07-14T00:00:01,065950 process=MainProcess process_id=2583919 caller=egse.protocol:595 msg="Executing is_connected failed."
    Traceback (most recent call last):
      File "/cgse/lib/python/egse/protocol.py", line 593, in handle_device_method
        response = method(*args, **kwargs)
      File "/cgse/lib/python/egse/tempcontrol/beaglebone/beaglebone.py", line 294, in is_connected
        return all([heater.connected for heater in self.heaters])
      File "/cgse/lib/python/egse/tempcontrol/beaglebone/beaglebone.py", line 294, in <listcomp>
        return all([heater.connected for heater in self.heaters])
    AttributeError: 'int' object has no attribute 'connected'

and

    level=ERROR ts=2023-07-14T00:00:01,285946 process=MainProcess process_id=2585980 caller=egse.protocol:595 msg="Executing is_connected failed."
    Traceback (most recent call last):
      File "/cgse/lib/python/egse/protocol.py", line 593, in handle_device_method
        response = method(*args, **kwargs)
      File "/cgse/lib/python/egse/socketdevice.py", line 124, in is_connected
        response = self.get_idn()
      File "/cgse/lib/python/egse/socketdevice.py", line 42, in get_idn
        raise NotImplementedError
    NotImplementedError

"""

from __future__ import annotations

import argparse
import os
import re
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def stash_file(file_name: str | Path, stash_name: str | Path = None) -> Path:
    """
    In the context of `stash_file` the file named `file_name` will be renamed to `stash_name`.
    If `stash_name` is None, the suffix '.orig' will be appended to the `file_name` and used
    as stash_name.

    Upon leaving the context, the file named `file_name` will be restored to its original
    content and file `stash_name` will be deleted.

    Args:
        file_name: the name or path of the file to stash
        stash_name: the optional name of the stashed file
    Returns:
        The name of the stashed file.
    Raises:
        An exception is raised if the stash_name file already exists.
    """

    file_name = Path(file_name).expanduser()

    if stash_name is None:
        stash_name = Path(f"{file_name}.orig")
    else:
        stash_name = Path(stash_name)

    # Since —on unix— the `os.rename()` function will overwrite stash_name when it exists,
    # we already here check if the file exists.

    if stash_name.exists():
        raise EnvironmentError(f"{stash_name} already exists, please remove/rename it before proceeding.")

    try:
        os.rename(file_name, stash_name)
    except FileNotFoundError as exc:
        raise EnvironmentError(f"No such file: {file_name}") from exc
    except OSError as exc:
        raise EnvironmentError(f"Please remove {stash_name}") from exc

    try:
        yield stash_name
    finally:
        os.replace(stash_name, file_name)


def rename_file(name: str | Path, new_name: str | Path) -> Path:
    """
    Rename a file.

    This will also work if the new_name is in a different folder as the original name.

    Args:
        name: the name of the original file to be stashed
        new_name: the name to use for the stashed file

    Returns:
        The name of the stashed file.
    Raises:
        An exception is raised if the stash_name file already exists.

    """
    name = Path(name).expanduser()
    new_name = Path(new_name).expanduser()

    # Since —on unix— the `os.rename()` function will overwrite stash_name when it exists,
    # we already here check if the file exists.

    if new_name.exists():
        raise EnvironmentError(f"{new_name} already exists, please remove/rename it before proceeding.")

    try:
        os.rename(name, new_name)
    except FileNotFoundError as exc:
        raise EnvironmentError(f"No such file: {name}") from exc
    except OSError as exc:
        raise EnvironmentError(f"{new_name} already exists, please remove/rename it before proceeding.") from exc

    return new_name


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--start_pattern", "-sp", required=True)
    parser.add_argument("--end_pattern", "-ep", required=True)
    parser.add_argument("path")

    args = parser.parse_args()

    moved_fn = rename_file(args.path, f"{args.path}.orig")

    start_marker = args.start_pattern
    end_marker = args.end_pattern

    with open(moved_fn, mode='r') as in_fd, open(args.path, mode='w') as out_fd:
        ignore_lines = False
        last_line_empty = False
        for line in in_fd:
            if re.search(start_marker, line):
                ignore_lines = True
            elif re.search(end_marker, line):
                ignore_lines = False
            elif not ignore_lines:
                if line.strip() == '':
                    if not last_line_empty:
                        last_line_empty = True
                        out_fd.write(line)
                else:
                    out_fd.write(line)
                    last_line_empty = False


def test_stash_file():

    fn = Path("~/Desktop/xxx.txt").expanduser()
    assert fn.exists()

    with stash_file(fn) as sfn:
        stash_name = sfn
        assert stash_name.exists()
        assert not fn.exists()

    assert fn.exists()
    assert not stash_name.exists()


def test_rename_file():

    fn = Path("~/Desktop/xxx.txt").expanduser()

    assert fn.exists()

    moved_fn = rename_file(fn, "~/tmp/yyy.out")

    assert not fn.exists()
    assert moved_fn.exists()


if __name__ == '__main__':
    main()
    # test_stash_file()
    # test_move_file()
