import mimetypes
import socket

import click

from platformio.compat import IS_WINDOWS
from platformio.custom.run import run_server
from platformio.package.manager.core import get_core_package_dir


@click.command("custom", short_help="GUI to manage Innatera")
@click.option("--port", type=int, default=8008, help="HTTP port, default=8008")
@click.option(
    "--host",
    default="127.0.0.2",
    help=(
        "HTTP host, default=127.0.0.2. You can open PIO Custom for inbound "
        "connections with --host=0.0.0.0"
    ),
)
@click.option("--no-open", is_flag=True)
@click.option(
    "--shutdown-timeout",
    default=0,
    type=int,
    help=(
        "Automatically shutdown server on timeout (in seconds) when no clients "
        "are connected. Default is 0 which means never auto shutdown"
    ),
)
@click.option(
    "--session-id",
    help=(
        "A unique session identifier to keep PIO Custom isolated from other instances "
        "and protect from 3rd party access"
    ),
)
def cli(port, host, no_open, shutdown_timeout, session_id):
    # hook for `platformio-node-helpers`
    if host == "__do_not_start__":
        # download all dependent packages
        get_core_package_dir("contrib-piocustom")
        return
    # Ensure PIO Custom mimetypes are known
    mimetypes.add_type("text/html", ".html")
    mimetypes.add_type("text/css", ".css")
    mimetypes.add_type("application/javascript", ".js")    

    custom_url = "http://%s:%d%s" % (
        host,
        port,
        ("/session/%s/" % session_id) if session_id else "/",
    )
    click.echo(
        "\n".join(
            [
                "",
                "  ___I_",
                " /\\-_--\\   Innatera Home",
                "/  \\_-__\\",
                "|[]| [] |  %s" % custom_url,
                "|__|____|__%s" % ("_" * len(custom_url)),
            ]
        )
    )
    click.echo("")
    click.echo("Open Innatera custom in your browser by this URL => %s" % custom_url)

    if is_port_used(host, port):
        click.secho(
            "Innatera Custom server is already started in another process.",
            fg="yellow",
        )
        if not no_open:
            click.launch(custom_url)
        return

    run_server(
        host=host,
        port=port,
        no_open=no_open,
        shutdown_timeout=shutdown_timeout,
        home_url=custom_url,
    )


def is_port_used(host, port):
    socket.setdefaulttimeout(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if IS_WINDOWS:
        try:
            s.bind((host, port))
            s.close()
            return False
        except (OSError, socket.error):
            pass
    else:
        try:
            s.connect((host, port))
            s.close()
        except socket.error:
            return False

    return True
