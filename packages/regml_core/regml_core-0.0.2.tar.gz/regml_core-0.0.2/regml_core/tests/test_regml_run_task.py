from regml_core.lib.remote_host import RegMLHttpRemoteConnector, RegMLRemoteHost, RegMLRemoteHostConfigArgs
from regml_core.lib.regml import RegML
import asyncio
from regml_core.lib.interfaces import RegMLRunTaskThunk

if __name__ == "__main__":
    async def main():
        regml = RegML(remote_hosts=[
            RegMLRemoteHost(
                connector=RegMLHttpRemoteConnector("https://regml.regscale.io/regml/api/examples/generic"),
            )
        ])
        

        spec = await regml.run_task(
            RegMLRunTaskThunk(
                task_name="LLMChat",
                task_version="0.0.0",
                task_args={
                    "base": {
                        "messages": [
                            {
                                "role": "system",
                                "content": "Print only the exact words in the quotes. Do not include the quotes: \"HELLO WORLD\""
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
                        "function_call": {
                            "name": "outputHelloWorld"
                        },
                    },
                    "provider": {}
                }
            )
        )

        print(spec)
    
    asyncio.run(main())