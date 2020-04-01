import argparse
import os
import re
import subprocess


# Indicator on the first line of a file encrypted with ansible vault.
ANSIBLE_SIGN = bytes('ANSIBLE_VAULT', 'utf-8')


def encrypted_files(directory=os.curdir, recursive=True):
    '''Search files under the current directory for those encrypted with
    Ansible Vault.  Optionally, recurse under the current directory.
    '''

    items = [os.path.join(directory, item) for item in os.listdir(directory)]
    directories = [item for item in items if os.path.isdir(item)]
    files = [item for item in items if os.path.isfile(item)]

    for file_path in files:
        with open(file_path, 'rb') as f:
            if ANSIBLE_SIGN in f.readline():
                yield file_path

    if recursive:
        for dir_path in directories:
            yield from encrypted_files(dir_path, recursive)


def decrypt(file_path):
    '''Run ansible-vault decrypt on a file in a subprocess to obtain its
    contents.
    '''

    proc = subprocess.run(
        ['ansible-vault', 'decrypt', file_path, '--output', '-'],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL)

    return proc.stdout.decode('utf-8')


def _valid_dir(string):
    '''A `type` for an `ArgumentParser` that checks if a provided string is a
    valid directory.
    '''

    if not os.path.isdir(string):
        raise argparse.ArgumentTypeError(
            '{} is not a valid directory'.format(string))

    return string


def main():
    parser = argparse.ArgumentParser(
        description='Search ansible-vault encrypted files for a substring.')
    parser.add_argument(
        'search', type=str, help='regex to search for')
    parser.add_argument(
        '-d',
        '--directory',
        type=_valid_dir,
        help='Directory to start searching from.',
        default=os.curdir)
    parser.add_argument(
        '-r',
        '--norecurse',
        help='Flag to turn OFF recursive search into directories.',
        default=False,
        action='store_true')
    args = parser.parse_args()

    # Argparse is kind of weird in how it supports flags.  The `norecurse`
    # flag turns OFF recursive file search, because we want to default to
    # always recursing into sub-directories.
    files = encrypted_files(
        directory=args.directory,
        recursive=not args.norecurse)

    pattern = re.compile(args.search)

    for file_path in files:
        if pattern.search(decrypt(file_path)) is not None:
            print(file_path)


if __name__ == '__main__':
    main()
