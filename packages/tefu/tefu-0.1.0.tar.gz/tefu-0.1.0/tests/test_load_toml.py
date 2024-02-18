# from src.tefu.loader import load_config
from tefu.loader import load_config
from tefu.runner import Case


def test_load_config():
    expect = [
        Case(case_input="1\n2 3\ntest\n", case_output="6\ntest\n"),
        Case(case_input="72\n128 256\nmyonmyon\n", case_output="456\nmyonmyon\n"),
    ]

    actual = load_config("./tests/tefu.toml")

    assert expect == actual
