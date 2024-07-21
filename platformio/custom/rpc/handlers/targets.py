import os
import shutil
import subprocess
import semantic_version
from ajsonrpc.core import JSONRPC20DispatchException
from platformio import app, exception, fs
from platformio.custom.rpc.handlers.base import BaseRPCHandler
import click

class PIOTargets():
    @staticmethod
    async def fetch( targets):
        if not targets:
            return []        
        targets = targets.split(",")
        for target in targets:
            subprocess.check_call(["pio", "run", "--target", target])
        return targets
