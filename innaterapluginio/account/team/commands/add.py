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

import click

from innaterapluginio.account.client import AccountClient
from innaterapluginio.account.validate import validate_orgname_teamname


@click.command("add", short_help="Add a new member to team")
@click.argument(
    "orgname_teamname",
    metavar="ORGNAME:TEAMNAME",
    callback=lambda _, __, value: validate_orgname_teamname(value),
)
@click.argument(
    "username",
)
def team_add_cmd(orgname_teamname, username):
    orgname, teamname = orgname_teamname.split(":", 1)
    client = AccountClient()
    client.add_team_member(orgname, teamname, username)
    return click.secho(
        "The new member %s has been successfully added to the %s team."
        % (username, teamname),
        fg="green",
    )
