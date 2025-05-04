from arkitekt_next import register, easy, progress
from koil.vars import check_cancelled

import time
import os
from pathlib import Path
from dorna2 import Dorna

# -----------------------------------------------------------------------------
# Robot controller
# -----------------------------------------------------------------------------

class DornaController:
    """Light‑weight wrapper around the Dorna2 SDK that plays text‑based motion
    scripts stored in ./paths. You only need to edit or add *.txt files inside
    that folder to teach new positions/motions – no code changes required.
    """

    def __init__(self, ip: str = "192.168.43.122"):
        self.ip = ip
        self.robot = Dorna()
        self.paths_dir = Path(__file__).resolve().parent / "paths"

    # ---------------------------------------------------------------------
    # connection helpers
    # ---------------------------------------------------------------------

    def connect(self):
        self.robot.connect(self.ip)
        self.robot.set_alarm(0)  # clear any previous alarm
        self.set_motor(1)        # enable motors

    def disconnect(self):
        self.robot.close()

    # ---------------------------------------------------------------------
    # low‑level helpers
    # ---------------------------------------------------------------------

    def set_motor(self, state: int):
        self.robot.set_motor(state)

    def halt(self):
        self.robot.halt()

    def is_busy(self) -> bool:
        # stat == 2 → idle, everything else → busy (per dorna2 docs)
        stat = self.robot.track_cmd()["union"].get("stat", -1)
        return stat != 2

    def play_script(self, filename: str):
        script_path = self.paths_dir / filename
        if not script_path.exists():
            raise FileNotFoundError(script_path)
        self.robot.play_script(str(script_path))

    # ---------------------------------------------------------------------
    # high‑level convenience wrappers (1:1 with register functions below)
    # ---------------------------------------------------------------------

    def move_to_rest_position(self):
        self.play_script("rest_position.txt")

    def move_to_microscope(self):
        self.play_script("move_to_microscope.txt")

    def move_to_opentrons(self):
        self.play_script("move_to_opentrons.txt")

    def move_from_microscope_to_opentrons(self):
        self.play_script("microscope_to_opentrons.txt")

    def move_from_opentrons_to_microscope(self):
        self.play_script("opentrons_to_microscope.txt")


# -----------------------------------------------------------------------------
# instantiate controller and connect once at module import
# -----------------------------------------------------------------------------
mRobotIP = "192.168.43.122"
controller = DornaController(mRobotIP)
controller.connect()


# -----------------------------------------------------------------------------
# Arkitekt exposed functions – simply drop/replace *.txt files in ./paths
# -----------------------------------------------------------------------------


def _execute(move_fn, description: str, timeout: int):
    """Shared helper that executes *move_fn* and waits until the robot is idle
    or *timeout* seconds have elapsed. Cancels cleanly if requested from the
    outside (e.g. via Arkitekt STOP button)."""

    start = time.time()
    move_fn()

    while controller.is_busy():
        check_cancelled()
        if time.time() - start > timeout:
            controller.halt()
            raise TimeoutError(f"{description} timed out after {timeout}s")
        time.sleep(0.05)

    return f"Finished: {description}"


@register
def move_to_rest_position(speed: int = 1, timeout: int = 10) -> str:  # speed kept for API symmetry
    """Move plate/arm into its park/rest position."""
    return _execute(controller.move_to_rest_position, "rest position", timeout)


@register
def move_to_microscope(speed: int = 1, timeout: int = 10) -> str:
    """Move plate from incubator (or current location) onto the microscope stage."""
    return _execute(controller.move_to_microscope, "microscope", timeout)


@register
def move_to_opentrons(speed: int = 1, timeout: int = 10) -> str:
    """Move plate into the Opentrons deck."""
    return _execute(controller.move_to_opentrons, "opentrons", timeout)


@register
def move_from_microscope_to_opentrons(speed: int = 1, timeout: int = 15) -> str:
    return _execute(controller.move_from_microscope_to_opentrons, "microscope→opentrons", timeout)


@register
def move_from_opentrons_to_microscope(speed: int = 1, timeout: int = 15) -> str:
    return _execute(controller.move_from_opentrons_to_microscope, "opentrons→microscope", timeout)


# -----------------------------------------------------------------------------
# Arkitekt entry‑point
# -----------------------------------------------------------------------------

with easy("dornado", url="go.arkitekt.live") as e:
    e.run()
