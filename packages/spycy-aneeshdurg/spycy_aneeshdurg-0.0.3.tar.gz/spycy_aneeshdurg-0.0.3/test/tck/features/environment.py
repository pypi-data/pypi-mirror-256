from spycy.spycy import CypherExecutor


def before_scenario(context, scenario):
    context.executor = CypherExecutor()
