import argparse

parser = argparse.ArgumentParser(
    prog="SEREVR",
    description="provides demo api's for Gaiuth auth",
    epilog="""...""",
)
__execution_types__ = ("isolated", "combined")
parser.add_argument(
    "-exec",
    "--execute",
    required=False,
    default="isolated",
    type=str,
    help="specify the type of execution you require",
    choices=__execution_types__,
)
