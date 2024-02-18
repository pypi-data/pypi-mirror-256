from tefu.runner import Case
from tomllib import load


def load_config(config_file: str):
    with open(config_file, "rb") as f:
        toml = load(f)

    return list(
        map(
            lambda item: Case(case_input=item["input"], case_output=item["output"]),
            toml["case"],
        )
    )
