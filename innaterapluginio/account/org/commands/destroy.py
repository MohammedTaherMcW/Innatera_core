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


@click.command("destroy", short_help="Destroy organization")
@click.argument("orgname")
def org_destroy_cmd(orgname):
    client = AccountClient()
    click.confirm(
        "Are you sure you want to delete the `%s` organization account?\n"
        "Warning! All linked data will be permanently removed and can not be restored."
        % orgname,
        abort=True,
    )
    client.destroy_org(orgname)
    return click.secho(
        "Organization `%s` has been destroyed." % orgname,
        fg="green",
    )
