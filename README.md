# cryptsearch

cryptsearch is a utility to aid with searching ansible vault-encrypted files.

## Installation

### Prerequisites

#### Ansible

In order to use cryptsearch, you must have installed
[Ansible](https://www.ansible.com/) which comes with `ansible-vault`.

```
pip install ansible
```

You must also be able to decrypt your ansible vault-encrypted files either by
providing the passphrase used to encrypt them or by being in posession of a GPG
key capable of derypting the files.

#### PATH

First create a `$HOME/bin` directory if you don't have one already and add it
to your `$PATH`.

```
mkdir $HOME/bin
```

Add to `$HOME/.bashrc` or `$HOME/.zshrc`:

```
PATH=$PATH:$HOME/bin
```

### Direct With Curl

```
curl https://raw.githubusercontent.com/arcrose/cryptsearch/master/cryptsearch.py > ~/bin/cryptsearch.py
chmod +x ~/bin/cryptsearch.py
```

### With Git

```
git clone https://github.com/arcrose/cryptsearch.git
cp cryptsearch/cryptsearch.py ~/bin
chmod +x ~/bin/cryptsearch.py
```

## Updating

### Using Curl

To update with `curl` just repeat the [curl installation](#direct-with-curl).

### Using Git

Using git, first pull the recent changes.

```
cd cryptsearch
git pull origin master
```

Then complete the installation by replacing the old copy.

```
cp cryptsearch/cryptsearch.py ~/bin
chmod +x ~/bin/cryptsearch.py
```

## Usage

You can view a help message explaining how to use cryptsearch by running

```
cryptsearch,.py -h
```

The most common usage is to run cryptsearch from the current directory,
searching for a string or [regular expression](https://docs.python.org/2/library/re.html).

```
cryptsearch.py <regex>
```

By default, cryptsearch performs a **case-sensitive** match and recurses into
all sub-directories.  Searches can be made **case-insensitive** by adding the
`-i` flag and searching sub-directories can be turned off with `-n`.

To begin searching in a directory other than the current directory, specify it
with `-d <directory>`.

As cryptsearch decrypts files using `ansible-vault`, it will print the paths to
any files it finds containing the regular expression / string provided.
