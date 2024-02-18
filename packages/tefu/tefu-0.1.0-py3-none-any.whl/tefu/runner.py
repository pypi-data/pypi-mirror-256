from dataclasses import dataclass
from tefu.status import Status
from toolz import curry
from tefu.variable import TARGET_FILE
import subprocess


@dataclass
class Case:
    case_input: str
    case_output: str

    def run(self):
        proc = subprocess.Popen(
            ["python", TARGET_FILE], stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )

        output = proc.communicate(self.case_input.encode().lstrip())
        decoded = output[0].decode()

        @curry
        def create_result(case_input, case_output, status):
            return (
                self.case_input,
                self.case_output,
                decoded,
                status,
            )

        create_in_out = create_result(self.case_input, self.case_output)

        if self.case_output.strip() == decoded.strip():
            return create_in_out(Status.PA.value)
        else:
            return create_in_out(Status.WA.value)
