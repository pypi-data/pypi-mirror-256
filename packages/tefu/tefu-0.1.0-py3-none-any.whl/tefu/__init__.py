from tefu.loader import load_config
from tefu.variable import CONFIG_FILE
from tabulate import tabulate


def main():
    cases = load_config(CONFIG_FILE)

    # testing all cases
    results = list(map(lambda item: item.run(), cases))

    print(
        tabulate(
            results,
            headers=["INPUT", "OUTPUT", "RESULT", "STATUS"],
            tablefmt="fancy_grid",
        )
    )

if __name__ == "__main__":
    main()
