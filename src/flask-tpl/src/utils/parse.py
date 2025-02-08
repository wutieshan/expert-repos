import json
import os
import tomllib


class FileParser:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def parse_dict(self) -> dict:
        """
        try to parse the file content into a dict
        """
        ext = os.path.splitext(self.filepath)[1]
        fp = open(self.filepath, "r", encoding="utf8")
        data = {}
        match ext:
            case ".json":
                data = json.load(fp)
            case ".toml":
                data = tomllib.load(fp)
            case _:
                fp.close()
                raise NotImplementedError(f"unsupported file type: {ext}")
        fp.close()
        return data
