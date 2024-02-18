import invoke


@invoke.task
def cov(ctx):
    invoke.run("rye run pytest --cov=src/ tests/")


@invoke.task
def test(ctx):
    invoke.run("rye run pytest")


@invoke.task
def fmt(ctx):
    invoke.run("rye run black ./**/*.py")
