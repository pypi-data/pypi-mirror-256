import pathlib
from typing import Union, List, Dict

from pykeepass import PyKeePass
from pykeepass.entry import reserved_keys
from cryptography.fernet import Fernet

reserved_keys = set(
    [i.lower() for i in reserved_keys if i not in ("History", "IconID", "Times", "otp")]
)


class KeePass(PyKeePass):
    def __init__(
        self,
        filename: pathlib.Path,
        secret: str,
        keyfile: pathlib.Path = None,
        token: pathlib.Path = None,
    ):
        if token is not None:
            with token.open("rb") as f:
                token_data = f.read()
            password = Fernet(secret.encode()).decrypt(token_data).decode()
        else:
            password = secret
        super().__init__(filename=filename, password=password, keyfile=keyfile)

    def get(self, path: Union[str, List[str]]) -> Dict[str, str]:
        """Get Entry as Dict"""
        if isinstance(path, str):
            path = path.strip("/").split("/")
        entry = self.find_entries(path=path)
        if not entry:
            raise KeyError("/".join(path))
        result = {k: getattr(entry, k) for k in reserved_keys}
        result.update(entry.custom_properties)
        return result
