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


class PlatformioException(Exception):
    MESSAGE = None

    def __str__(self):  # pragma: no cover
        if self.MESSAGE:
            # pylint: disable=not-an-iterable
            return self.MESSAGE.format(*self.args)

        return super().__str__()


class ReturnErrorCode(PlatformioException):
    MESSAGE = "{0}"


class UserSideException(PlatformioException):
    pass


class AbortedByUser(UserSideException):
    MESSAGE = "Aborted by user"


#
# UDEV Rules
#


class InvalidUdevRules(UserSideException):
    pass


class MissedUdevRules(InvalidUdevRules):
    MESSAGE = (
        "Warning! Please install `99-platformio-udev.rules`. \nMore details: "
    )


class OutdatedUdevRules(InvalidUdevRules):
    MESSAGE = (
        "Warning! Your `{0}` are outdated. Please update or reinstall them."
        "\nMore details: "
    )


#
# Misc
#


class GetSerialPortsError(PlatformioException):
    MESSAGE = "No implementation for your platform ('{0}') available"


class GetLatestVersionError(PlatformioException):
    MESSAGE = "Can not retrieve the latest PlatformIO version"


class InvalidSettingName(UserSideException):
    MESSAGE = "Invalid setting with the name '{0}'"


class InvalidSettingValue(UserSideException):
    MESSAGE = "Invalid value '{0}' for the setting '{1}'"


class InvalidJSONFile(ValueError, UserSideException):
    MESSAGE = "Could not load broken JSON: {0}"


class CIBuildEnvsEmpty(UserSideException):
    MESSAGE = (
        "Can't find Innatera build environments.\n"
        "Please specify `--board` or path to `innaterapluginio.ini` with "
        "predefined environments using `--project-conf` option"
    )


class HomeDirPermissionsError(UserSideException):
    MESSAGE = (
        "The directory `{0}` or its parent directory is not owned by the "
        "current user and Innatera can not store configuration data.\n"
        "Please check the permissions and owner of that directory.\n"
        "Otherwise, please remove manually `{0}` directory and Innatera "
        "will create new from the current user."
    )


class CygwinEnvDetected(PlatformioException):
    MESSAGE = (
        "Innatera does not work within Cygwin environment. "
        "Use native Terminal instead."
    )
