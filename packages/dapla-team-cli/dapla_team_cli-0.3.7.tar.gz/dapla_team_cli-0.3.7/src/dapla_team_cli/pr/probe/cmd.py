"""Commands for probing readiness."""
import sys

import typer

from dapla_team_cli.pr.probe.probe_atlantis_apply import probe_atlantis_apply
from dapla_team_cli.pr.probe.probe_workflows import probe_workflows
from dapla_team_cli.pr.state.state_utils import state_object_handler


app = typer.Typer(name="probe", help="Validate pull requests", no_args_is_help=True)


@app.command("plan")
def plan() -> None:
    """Probes whether plans and checks were successful.

    Updates statefile accordingly.
    """
    if state := state_object_handler.get_user_state():
        probe_workflows(state)
    else:
        sys.exit(1)


@app.command("apply")
def apply() -> None:
    """Probes atlantis apply was successful.

    Updates statefile accordingly.
    """
    if state := state_object_handler.get_user_state():
        probe_atlantis_apply(state)
    else:
        sys.exit(1)
