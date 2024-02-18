from regml_core.lib.remote_host import RegMLHttpRemoteConnector, RegMLRemoteHost, RegMLRemoteHostConfigArgs
from regml_core.lib.regml import RegML
import asyncio
from regml_core.lib.interfaces import RegMLRunTaskThunk
from regml_task_registry_hardcoded import LLMChat_V0_1_0_InputSchema
from regml_llmchat_task_helpers import llmchat 

if __name__ == "__main__":
    async def main(regml):
        resp = await llmchat(
            regml,
            LLMChat_V0_1_0_InputSchema.parse_obj({ 
                'messages': [
                    {
                        'role': 'system',
                        'content': 'Print only the exact words in the quotes. Do not include the quotes: "HELLO WORLD"'
                    }
                ],
                "functions": [{
                    "name": "outputHelloWorld",
                    "description": "Output hello world",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "output": {
                                "type": "string"
                            }
                        }
                    }
                }],
                "functionCall": {
                    "name": "outputHelloWorld"
                },
            })
        )

        print('OUTPUT', resp)


        resp = await llmchat(
            regml,
            { 
                'messages': [
                    {
                        'role': 'system',
                        'content': 'Print only the exact words in the quotes. Do not include the quotes: "HELLO WORLD"'
                    }
                ],
                "functions": [{
                    "name": "outputHelloWorld",
                    "description": "Output hello world",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "output": {
                                "type": "string"
                            }
                        }
                    }
                }],
                "functionCall": {
                    "name": "outputHelloWorld"
                },
            }
        )

        print('OUTPUT', resp)

    regml = RegML(remote_hosts=[
        RegMLRemoteHost(
            connector=RegMLHttpRemoteConnector("https://regml.regscale.io/regml/api/examples/generic"),
        )
    ])

    asyncio.run(main(regml))