from typing import Text, Any
from abc import ABC, abstractclassmethod
from enum import Enum
from argparse import ArgumentParser

import yaml
import json
import requests

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class SyncType(Enum):
    YAML = 'yaml'
    JSON = 'json'


class Sync(ABC):
    @classmethod
    def download(cls, url: Text) -> Any:
        pass

    @classmethod
    @abstractclassmethod
    def read(cls, file_path: Text) -> Any:
        pass

    @classmethod
    @abstractclassmethod
    def write(cls, file_path: Text, content: Any) -> None:
        pass


class TextSync(Sync):
    @classmethod
    def download(cls, url: Text) -> Any:
        response = requests.get(url, verify=False)
        response.encoding = 'utf-8'
        return response.text


class YamlSync(TextSync):
    @classmethod
    def download(cls, url: Text) -> Any:
        text = super().download(url)
        return yaml.load(text, Loader=Loader)

    @classmethod
    def read(cls, file_path: Text) -> Any:
        with open(file_path, 'r') as f:
            content = yaml.load(f, Loader=Loader)
        return content

    @classmethod
    def write(cls, file_path: Text, content: Any) -> None:
        with open(file_path, 'w') as f:
            yaml.dump(content, f, Dumper=Dumper)
        return


class JsonSync(TextSync):
    @classmethod
    def download(cls, url: Text) -> Any:
        text = super().download(url)
        return json.loads(text)

    @classmethod
    def read(cls, file_path: Text) -> Any:
        with open(file_path, 'r') as f:
            content = json.load(f)
        return content

    @classmethod
    def write(cls, file_path: Text, content: Any) -> None:
        with open(file_path, 'w') as f:
            json.dump(content, f)
        return


def get_sync(sync_type: SyncType) -> Sync:
    sync_mapping = {
        SyncType.YAML: YamlSync,
        SyncType.JSON: JsonSync,
    }
    assert sync_type in sync_mapping, 'unknow sync type: {}'.format(sync_type)
    return sync_mapping[sync_type]


def download(sync_type: SyncType, url: Text) -> Any:
    return get_sync(sync_type).download(url)


def read_file(sync_type: SyncType, file_path: Text) -> Any:
    return get_sync(sync_type).read(file_path)


def write_file(sync_type: SyncType, file_path: Text, content: Any) -> None:
    get_sync(sync_type).write(file_path, content)


def merge_content(a: Any, b: Any) -> None:
    if (b is None):
        return a
    if (not isinstance(a, dict)) or (not isinstance(b, dict)):
        return b
    for key, value in b.items():
        a[key] = merge_content(a[key], value) if key in a else value
    return a


def sync(file_type: SyncType, source: Text, dest: Text, private: Text=None) -> None:
    content = download(file_type, source)
    if private is not None:
        merge_content(content, read_file(file_type, private))
    write_file(file_type, dest, content)


def sfsync() -> None:
    parser = ArgumentParser(description='Download a single file and merge private changes.')
    parser.add_argument(
        '-c', dest='config', type=str, required=True,
        help="Path to the config file."
    )
    args = parser.parse_args()

    config_path = args.config
    with open(config_path, 'r') as f:
        config = json.load(f)
    sync_type = SyncType(config['type'])
    sync(sync_type, config['source'], config['dest'], config['private'])


if __name__ == '__main__':
    sfsync()
