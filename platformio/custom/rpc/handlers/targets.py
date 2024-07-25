import asyncio
import subprocess
from ajsonrpc.core import JSONRPC20DispatchException
import logging
import os


class PIOTargets:
    @staticmethod
    async def fetch(targets):
        if not targets:
            return []

        # Ensure targets is a list
        if isinstance(targets, str):
            targets = [
                target.strip() for target in targets.split(",") if target.strip()
            ]

        if not targets:
            raise JSONRPC20DispatchException("No valid targets specified.")

        pio = os.path.expanduser("~") + "/.platformio/penv/bin/pio"
        for target in targets:
            result = subprocess.call(
                [
                    pio,
                    "run",
                    "--target",
                    target,
                ]
            )
            if result != 0:
                logging.error("Failed to run target %s" % target)
        return targets
