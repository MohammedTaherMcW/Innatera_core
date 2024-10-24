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

import os
from urllib.parse import urlparse

import click
import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_403_FORBIDDEN

from innaterapluginio.custom.rpc.handlers.app import AppRPC
from innaterapluginio.compat import aio_get_running_loop
from innaterapluginio.custom.rpc.handlers.ide import IDERPC
from innaterapluginio.exception import PlatformioException
from innaterapluginio.custom.rpc.handlers.targets import PIOTargets
from innaterapluginio.custom.rpc.handlers.piocore import PIOCoreRPC
from innaterapluginio.custom.rpc.server import WebSocketJSONRPCServerFactory
from innaterapluginio.package.manager.core import get_core_package_dir
from innaterapluginio.proc import force_exit


class ShutdownMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and b"__shutdown__" in scope.get("query_string", ""):
            await shutdown_server()
        await self.app(scope, receive, send)


async def shutdown_server(_=None):
    aio_get_running_loop().call_later(0.5, force_exit)
    return PlainTextResponse("Server has been shutdown!")


async def protected_page(_):
    return PlainTextResponse(
        "Protected Innatera Home session", status_code=HTTP_403_FORBIDDEN
    )


def run_server(host, port, no_open, shutdown_timeout, home_url):
    contrib_dir = get_core_package_dir("contrib-piocustom")
    if not os.path.isdir(contrib_dir):
        raise PlatformioException("Invalid path to Innatera Custom Contrib")

    ws_rpc_factory = WebSocketJSONRPCServerFactory(shutdown_timeout)
    ws_rpc_factory.add_object_handler(PIOCoreRPC(), namespace="core")
    ws_rpc_factory.add_object_handler(AppRPC(), namespace="app")
    ws_rpc_factory.add_object_handler(PIOTargets(), namespace="targets")
    ws_rpc_factory.add_object_handler(IDERPC(), namespace="ide")
    path = urlparse(home_url).path
    routes = [
        WebSocketRoute(path + "wsrpc", ws_rpc_factory, name="wsrpc"),
        Route(path + "__shutdown__", shutdown_server, methods=["POST"]),
        Mount(path, StaticFiles(directory=contrib_dir, html=True), name="static"),
    ]
    if path != "/":
        routes.append(Route("/", protected_page))

    uvicorn.run(
        Starlette(
            middleware=[Middleware(ShutdownMiddleware)],
            routes=routes,
            on_startup=[
                lambda: click.echo(
                    "Innatera Home has been started. Press Ctrl+C to shutdown."
                ),
                lambda: None if no_open else click.launch(home_url),
            ],
        ),
        host=host,
        port=port,
        log_level="warning",
    )
