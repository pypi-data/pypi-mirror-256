
from dataclasses import dataclass
from .remote_host import RegMLRemoteHost
import asyncio
from regml_core.lib.interfaces.run_task_thunk import RegMLRunTaskThunk

# @dataclass
# class RegMLConfigArgs:
#     remote_hosts: list[RegMLRemoteHost]
#     # To get us up and running, we've opted for a minimal set of required arguments.
#     # The other arguments here should be added at a later date.
#     # security_policies: RegMLCoreDataSecurityPolicy
#     # providers: Optional[TLocalProviders] = None
#     # callbacks: Optional[RegMLCallbackHandler] = None
#     # custom_instance_id: Optional[str] = None

class RegML(object):
    def __init__(self, remote_hosts: list[RegMLRemoteHost]):
        self.remote_hosts = remote_hosts

    async def run_task(self, task_thunk: RegMLRunTaskThunk):
        # Get the first remote host
        remote_host = self.remote_hosts[0]

        # Call the get_spec method on the remote host
        host_spec = await remote_host.get_spec()

        return await remote_host.run_task(task_thunk)
