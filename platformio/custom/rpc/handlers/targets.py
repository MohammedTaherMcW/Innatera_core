import asyncio
import subprocess
from ajsonrpc.core import JSONRPC20DispatchException
import logging


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

        completed_targets = []
        errors = []

        for target in targets:
            try:
                # Using asyncio to run subprocess in a non-blocking way
                process = await asyncio.create_subprocess_exec(
                    "pio",
                    "run",
                    "--target",
                    target,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                stdout, stderr = await process.communicate()

                if process.returncode != 0:
                    error_message = f"Error building target {target}: {stderr.decode()}"
                    logging.error(error_message)
                    errors.append(error_message)
                else:
                    completed_targets.append(target)
                    logging.info(f"Successfully built target: {target}")
            except Exception as e:
                error_message = (
                    f"Exception occurred while building target {target}: {e}"
                )
                logging.error(error_message)
                errors.append(error_message)

        if errors:
            raise JSONRPC20DispatchException(f"Errors occurred: {', '.join(errors)}")

        return completed_targets
