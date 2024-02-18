
from dataclasses import dataclass
from dataclasses import asdict
import inflection

@dataclass
class RegMLTaskArgs:
    base: dict
    provider: dict

@dataclass
class RegMLRunTaskThunk:
    task_name: str
    task_version: str
    task_args: RegMLTaskArgs

    def to_api_json_dict(self):
        """
        Convert the object to a JSON-serializable dictionary.

        This uses camelCase for the keys, as required by the RegML API.
        """

        # Convert self to dict.
        self_dict = asdict(self)

        # Recursively convert keys to camelCase.
        def convert_keys_to_camel_case(d: dict):
            return {
                inflection.camelize(k, False): convert_keys_to_camel_case(v) if isinstance(v, dict) else v
                for k, v in d.items()
            }
        
        converted_self_dict = convert_keys_to_camel_case(self_dict)

        return {
            "typeName": "RegMLRunTaskThunk",
            **converted_self_dict
        }