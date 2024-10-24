# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=unused-import,no-name-in-module

import importlib.util
import inspect
import locale
import os
import shlex
import sys

from innaterapluginio.exception import UserSideException

if sys.version_info >= (3, 7):
    from asyncio import create_task as aio_create_task
    from asyncio import get_running_loop as aio_get_running_loop
else:
    from asyncio import ensure_future as aio_create_task
    from asyncio import get_event_loop as aio_get_running_loop


if sys.version_info >= (3, 8):
    from shlex import join as shlex_join
else:

    def shlex_join(split_command):
        return " ".join(shlex.quote(arg) for arg in split_command)


if sys.version_info >= (3, 9):
    from asyncio import to_thread as aio_to_thread
else:
    try:
        from starlette.concurrency import run_in_threadpool as aio_to_thread
    except ImportError:
        pass


PY2 = sys.version_info[0] == 2  # DO NOT REMOVE IT. ESP8266/ESP32 depend on it
PY36 = sys.version_info[0:2] == (3, 6)
IS_CYGWIN = sys.platform.startswith("cygwin")
IS_WINDOWS = WINDOWS = sys.platform.startswith("win")
IS_MACOS = sys.platform.startswith("darwin")
MISSING = object()
string_types = (str,)


def is_bytes(x):
    return isinstance(x, (bytes, memoryview, bytearray))


def isascii(text):
    if sys.version_info >= (3, 7):
        return text.isascii()
    for c in text or "":
        if ord(c) > 127:
            return False
    return True


def is_terminal():
    try:
        return sys.stdout.isatty()
    except Exception:  # pylint: disable=broad-except
        return False


def ci_strings_are_equal(a, b):
    if a == b:
        return True
    if not a or not b:
        return False
    return a.strip().lower() == b.strip().lower()


def hashlib_encode_data(data):
    if is_bytes(data):
        return data
    if not isinstance(data, string_types):
        data = str(data)
    return data.encode()


def load_python_module(name, pathname):
    spec = importlib.util.spec_from_file_location(name, pathname)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_filesystem_encoding():
    return sys.getfilesystemencoding() or sys.getdefaultencoding()


def get_locale_encoding():
    return locale.getpreferredencoding()


def get_object_members(obj, ignore_private=True):
    members = inspect.getmembers(obj, lambda a: not inspect.isroutine(a))
    if not ignore_private:
        return members
    return {
        item[0]: item[1]
        for item in members
        if not (item[0].startswith("__") and item[0].endswith("__"))
    }


def ensure_python3(raise_exception=True):
    compatible = sys.version_info >= (3, 6)
    if not raise_exception or compatible:
        return compatible
    raise UserSideException(
        "Python 3.6 or later is required for this operation. \n"
        "Please check a migration guide:\n"
    )


def path_to_unicode(path):
    """
    Deprecated: Compatibility with dev-platforms,
    and custom device monitor filters
    """
    return path


def is_proxy_set(socks=False):
    for var in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
        value = os.getenv(var, os.getenv(var.lower()))
        if not value or (socks and not value.startswith("socks5://")):
            continue
        return True
    return False
