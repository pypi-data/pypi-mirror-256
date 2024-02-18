import glob
import json
import os
import re
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import datetime
from json import JSONEncoder
from pathlib import Path
import tempfile
from typing import Any, Tuple, Type, TypeVar
from urllib.parse import urlsplit

default_meta_file = "metadata.json"
timeformat = "%Y%m%d-%H%M%S"


# @dataclass
class MetaObj(dict):
    def __init__(self, **kwargs):
        # pass
        self.__dict__.update(kwargs)

    def __json__(self):
        ## create a json for all non private members
        obj = {k: v for k, v in self.__dict__.items() if not k.startswith("_") and not callable(k)}
        return obj

    def __str__(self):
        return str(self.__json__())


# @dataclass
class MetaUri(MetaObj):
    # uri: str

    def __init__(self, uri: str, metadata: dict = None, **kwargs):
        super().__init__(**kwargs)
        self.uri = uri
        self.metadata = metadata or {}

    def __str__(self):
        return self.uri

    def __repr__(self):
        return self.uri


C = TypeVar("C", bound="MetaUri")


def url_with_path(url):
    split_url = urlsplit(url)
    url = f"{split_url.scheme}://{split_url.netloc}{split_url.path}"
    if url.endswith("/"):
        url = url[:-1]
    return url


@dataclass
class MetaOptions:
    create_root: bool = True


@dataclass
class Meta(dict):
    """
    A class to represent the metadata of a collection of files under a given directory.
    The structure is as follows:
    - root: the directory where the files and subfolders are located
        - meta.json: a json file with the metadata for the folders and files
        - subfolder (optional): the subfolder where the files are located
            - file1
            - file2
            - ...
        - subfolder2 (optional): another subfolder where the files are located
            - file3
            - file4
            - ...
    """

    root: str = None
    meta_file: str = None
    created_at: datetime = field(default=lambda: datetime.utcnow())

    def __init__(
        self,
        initial_dict: dict = None,
        create: bool = False,
        use_timed_subfolder: bool = False,
        *args,
        **kwargs,
    ):
        kwargs.update(initial_dict or {})
        super().__init__(*args, **kwargs)
        self.__dict__ = self
        self._init(create, use_timed_subfolder, *args, **kwargs)

    def __post_init__(self):
        self._init()

    def _init(self, create: bool = False, use_timed_subfolder: bool = False, *args, **kwargs):
        if self.root and self.meta_file is None:
            self.meta_file = str(Path(os.path.join(self.root, default_meta_file)).absolute())
        if self.root:
            self.root = str(Path(self.root).absolute())

        if self.meta_file:
            if os.path.exists(self.meta_file):
                self.load()
            elif create:
                os.makedirs(self.root, exist_ok=True)
                self.save(indent=2)
        # print("INIT", self.root, self.meta_file, self.created_at)

    # def __json__(self):
    #     obj: Meta = self.copy()
    #     ## convert Path to string for any members that are Paths
    #     for k, v in obj.items():
    #         if isinstance(v, Path):
    #             obj[k] = str(v)
    #     # obj["root"] = str(obj["root"])
    #     # obj["meta_file"] = str(obj["meta_file"])
    #     return obj

    @property
    def strdate(self):
        return self.created_at.strftime()

    @staticmethod
    def create_most_recent(dir_path: str) -> "Meta":
        now = datetime.utcnow().strftime(timeformat)
        dir_path = os.path.expanduser(dir_path)
        os.makedirs(os.path.join(dir_path, now), exist_ok=True)
        rootdir = Meta.get_most_recent_folder(dir_path)
        meta = Meta(root=rootdir)
        print(meta)
        meta.save()
        return meta

    def get_subfolder_meta(self, subfolder: str) -> dict[str, Any]:
        if not "tracked_subfolders" in self:
            self["tracked_subfolders"] = defaultdict(dict)
        if not subfolder in self["tracked_subfolders"]:
            self["tracked_subfolders"][subfolder] = {}
        return self["tracked_subfolders"][subfolder]

    @staticmethod
    def get_folder_and_meta(dir_path: str) -> Tuple[str, str]:
        dir_path = os.path.expanduser(dir_path)
        rootdir = Meta.get_most_recent_folder(dir_path)
        if not os.path.exists(rootdir):
            raise FileNotFoundError(f"Could not find {rootdir}")
        meta_file = os.path.abspath(os.path.join(rootdir, "..", default_meta_file))

        if not os.path.exists(meta_file):
            meta_file = os.path.join(rootdir, default_meta_file)
            if not os.path.exists(meta_file):
                raise FileNotFoundError(f"Could not find {meta_file}")
        return rootdir, meta_file

    @staticmethod
    def get_most_recent_folder(dir_path: str) -> str:
        """
        Get the most recent folder in dir_path with the format YYYYMMDD-HHMMSS
        if no such folder exists, return dir_path

        """
        if dir_path.startswith("~"):
            dir_path = os.path.expanduser(dir_path)
        files = glob.glob(f"{dir_path}/*")
        files = sorted(files)
        files = [f for f in files if re.search(r"[0-9]{8,8}-[0-9]{6,6}", f) is not None]
        try:
            return str(files[-1])
        except IndexError:
            raise IndexError(f"Could not find a folder with the correct format in {dir_path}")

    @staticmethod
    def from_most_recent(dir_path: str, create: bool = False) -> "Meta":
        if dir_path.startswith("~"):
            dir_path = os.path.expanduser(dir_path)
        try:
            # rootdir, meta_file = Meta.get_folder_and_meta(dir_path)
            rootdir = Meta.get_most_recent_folder(dir_path)
        except IndexError:
            if create:
                os.makedirs(dir_path, exist_ok=True)
                rootdir = os.path.join(dir_path, datetime.utcnow().strftime(timeformat))
                os.makedirs(rootdir, exist_ok=True)
                meta_file = os.path.join(rootdir, default_meta_file)
                with open(meta_file, "w") as f:
                    json.dump({}, f)
            else:
                raise
        return Meta(root=rootdir)

    @staticmethod
    def from_directory(root: str, create: bool = False) -> "Meta":
        return Meta(root=root, create=create)

    def save(self, file_name: str = None, indent: int = 2, **kwargs):
        if not file_name and not self.root:
            raise ValueError("No file_name or root directory to save the metadata")
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            json.dump(self, f, indent=indent, **kwargs)
            os.rename(f.name, self.meta_file)

    # def _members_to_path(self):
    #     for k in ["root", "meta_file"]:
    #         try:
    #             if self[k] is None:
    #                 continue
    #         except:
    #             continue
    #         if isinstance(self[k], str):
    #             self[k] = Path(self[k])

    def load(self, file_name: str = None):
        if not file_name and not self.root:
            raise ValueError("No file_name or root directory to load the metadata")
        file_name = file_name or self.meta_file
        with open(file_name, "r") as f:
            self.update(json.load(f))
        # self._members_to_path()

    # def get_file(self, file_name: str, subfolder=None, cls: Type["MetaObj"] = None) -> "MetaObj":
    # def get_file(self, file_name: str, subfolder=None, cls: Type["MetaObj"] = None) -> __qualname__:
    def get_file_meta(self, file_name: str, subfolder=None, cls: Type[C] = None) -> C:
        print("GET FILE", file_name, subfolder, cls)
        if subfolder is None:
            if not "/" in file_name:
                raise ValueError(f"subfolder must be a valid path")
            subfolder, file_name = file_name.split("/", maxsplit=1)[0]

        submeta = self.get_subfolder_meta(subfolder)
        if not "uris" in submeta:
            raise FileNotFoundError(f"Could not find {file_name} in {subfolder}")
        if not cls:
            cls = MetaUri
        path = str(Path(self._path_join(subfolder, file_name)).absolute())
        if not file_name in submeta["uris"]:
            if not path in submeta["uris"]:
                raise FileNotFoundError(f"Could not find {file_name} in {subfolder}")
            file_name = path
        if not os.path.exists(path):
            raise FileNotFoundError(f"Could not find {path}")
        print("get_file", submeta["uris"][file_name])
        return cls(**submeta["uris"][file_name])
        # with open(path, "r") as f:
        #     json_data = json.load(f)
        # return cls(**json_data)

    def get_files_meta(self, subfolder: str, cls: Type[C] = None) -> list[C]:
        path = self.get_directory(subfolder)
        fs = []
        submeta = self.get_subfolder_meta(subfolder)
        uris = submeta.get("uris", {})
        if cls is None:
            cls = MetaUri
        for f in glob.glob(f"{path}/*"):
            print(f"    get_files={f}")
            if os.path.isfile(f):
                print("        is file")
                o = self.get_file_meta(f, subfolder, cls)
                print("        o=", o)
                fs.append(o)
                # if f in uris:
                #     fs.append(cls(f, metadata=uris[f]))
                # else:
                #     fs.append(cls(f))
        return fs

    def add_file_meta(self, subfolder: str, values: dict | MetaUri = None):
        if values is None:
            raise ValueError("No values to add")
        
        if isinstance(values, MetaUri):
            metauri = values
        else:
            metauri = MetaUri(**values)
        submeta = self.get_subfolder_meta(subfolder)
        if not "uris" in submeta:
            submeta["uris"] = {}

        submeta["uris"][metauri.uri] = metauri.__json__()
        self.save()

    def get_directory(self, subfolder: str = None, create: bool = False):
        if subfolder and not os.path.exists(self._path_join(subfolder)):
            if create:
                os.makedirs(self._path_join(subfolder))
        if subfolder is None:
            return self.root

        return self._path_join(subfolder)

    def _path_join(self, subfolder: str, *args):
        if subfolder is None:
            return os.path.join(self.root, *args)
        return os.path.join(self.root, subfolder, *args)

    def has_directory(self, subfolder: str = None):
        if subfolder is None:
            return os.path.exists(self.root)
        return os.path.exists(self._path_join(subfolder))
