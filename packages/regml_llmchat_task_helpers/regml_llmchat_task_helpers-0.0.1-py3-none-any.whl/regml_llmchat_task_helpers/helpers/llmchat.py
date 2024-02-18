
from regml_core.lib.regml import RegML, RegMLRunTaskThunk
from regml_core.lib.remote_host import RegMLHttpRemoteConnector, RegMLRemoteHost, RegMLRemoteHostConfigArgs
import asyncio
from typing import Union
from regml_task_registry_hardcoded.tasks.llmchat.registry import LLMChat_V0_1_0_InputSchema


async def llmchat(regml, task_args: Union[LLMChat_V0_1_0_InputSchema, dict]):
    task_args_base = LLMChat_V0_1_0_InputSchema.parse_obj(task_args) if isinstance(task_args, dict) else task_args
    
    using_dict = task_args_base.dict()

    return await regml.run_task(RegMLRunTaskThunk(
        task_name="LLMChat",
        task_version="0.1.0",
        task_args={
            "base": using_dict,
            "provider": {}
        }
    ))


