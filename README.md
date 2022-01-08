# Single File Sync

A simple tool to automatically download a single file and merge private changes.

## How does it work

1. Download a file from the given source.
2. Merge private changes from a local file.
3. Write the merged content to the given destination.

## Dependency

- Python 3.7.11+
- [Requests](https://docs.python-requests.org/en/latest/) 2.26.0+
- [PyYAML](https://pyyaml.org/) 6.0+

## Usage

```
sfsync -c CONFIG_FILE
```

`CONFIG_FILE` should be a JSON file in the following format:

```
{
    "type": TYPE,
    "source": SOURCE,
    "private": PRIVATE,
    "dest": DEST
}
```

- `TYPE`: type name from **File type support**.
- `SOURCE`: URL to the file to download.
- `PRIVATE`: path to a file containing private changes to merge.
- `DEST`: destination to write the result.


## File type support

- YAML: `yaml`
- JSON: `json`
