import os
import tempfile
from pathlib import Path


class StorageBackend:
    """Minimal storage contract so object storage can replace local files."""

    def save(self, key, data):
        raise NotImplementedError

    def open(self, path):
        raise NotImplementedError

    def delete(self, path):
        raise NotImplementedError


class FileStorage(StorageBackend):
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, key, data):
        # Keys are generated internally, but keeping the storage boundary
        # explicit prevents a future caller from turning this into traversal.
        safe_key = Path(str(key)).name
        if safe_key != str(key) or not safe_key:
            raise ValueError("invalid storage key")
        path = self.root / (safe_key + ".pdf")
        fd, temporary = tempfile.mkstemp(prefix=".pdf-", dir=str(self.root))
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
        finally:
            try:
                Path(temporary).unlink()
            except FileNotFoundError:
                pass
        return str(path)

    def open(self, path):
        candidate = Path(path).resolve()
        root = self.root.resolve()
        if candidate.parent != root:
            raise ValueError("invalid storage path")
        return candidate.read_bytes()

    def delete(self, path):
        candidate = Path(path).resolve()
        if candidate.parent != self.root.resolve():
            raise ValueError("invalid storage path")
        try:
            candidate.unlink()
        except FileNotFoundError:
            pass
