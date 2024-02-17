import asyncio
import logging


logger = logging.getLogger(__name__)


LOCKS = {
    'bluetooth':    None,       # global bluetooth lock
    'gpio':         None,       # global gpio lock (future)
}


async def init_locks():
    """
    Initialize locks required for shared asyncio access to resources

    args: none
    returns: none
    """

    logger.debug("Initializing asyncio locks")

    if LOCKS['bluetooth'] is None:
        LOCKS['bluetooth'] = asyncio.Lock()

    if LOCKS['gpio'] is None:
        LOCKS['gpio'] = asyncio.Lock()
