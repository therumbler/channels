import asyncio
import logging
import sys

logger = logging.getLogger(__name__)


def setup_logging(level=logging.INFO):
    logging.basicConfig(stream=sys.stdout, level=level)


async def run_command(cmd, loop=None):
    """Run command in subprocess

    Example from:
        http://asyncio.readthedocs.io/en/latest/subprocess.html
    """
    # print(loop)
    # asyncio.set_event_loop(loop)
    # Create subprocess
    logger.debug("running %s...", cmd)
    process = await asyncio.create_subprocess_exec(
        *cmd,
        # stdout must be a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE
        # loop=loop
    )
    logger.debug("proc created...")
    # Status
    logger.debug("Started: %s (pid = %d)", cmd, process.pid)

    # Wait for the subprocess to finish
    try:
        stdout, stderr = await process.communicate()
    except asyncio.CancelledError:
        logger.info("got CancellerError")
        process.kill()
        logger.info("sent kill")
        raise
    # Progress
    if process.returncode == 0:
        logger.debug("Done: %s (pid=%d)", cmd, process.pid)
    else:
        logger.error("Failed: %s (pid = %s)", cmd, process.pid)

    # Result
    result = stdout.decode().strip()

    # Return stdout
    return result
