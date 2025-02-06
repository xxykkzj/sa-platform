"""Shows percentage upload"""
import os
import threading


# pylint: disable=too-few-public-methods

class S3ProgressPercentage():
    """S3 upload progress"""

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        """Call method"""
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = round((self._seen_so_far / self._size) * 100, 2)
            print(
                f"{self._filename}  {self._seen_so_far} / {self._size}  {percentage}")

# pylint: disable=too-few-public-methods
