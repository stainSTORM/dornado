from arkitekt_next import register
import time
from dorna2 import Dorna

@register
def move_to_rest_position(speed: int = 1, timeout: int = 2) -> str:
    """
    """
    robot = Dorna()
    robot.connect("192.168.43.122")
    robot.set_motor(1)    
    robot.play(timeout=-1, cmd="jmove", rel=1, j0=10, vel=1)
    return "did it move?"

@register
def move_to_microscope(speed: int = 1, timeout: int = 2) -> str:
    """
    """
    robot = Dorna()
    robot.connect("192.168.43.122")
    robot.set_motor(1)    
    robot.play(timeout=-1, cmd="jmove", rel=1, j0=10, vel=1)
    return "did it move?"

@register
def move_to_opentrons(speed: int = 1, timeout: int = 2) -> str:
    """
    """
    robot = Dorna()
    robot.connect("192.168.43.122")
    robot.set_motor(1)    
    robot.play(timeout=-1, cmd="jmove", rel=1, j0=10, vel=1)
    return "did it move?"

@register
def move_from_microscope_to_opentrons(speed: int = 1, timeout: int = 2) -> str:
    """
    """
    robot = Dorna()
    robot.connect("192.168.43.122")
    robot.set_motor(1)    
    robot.play(timeout=-1, cmd="jmove", rel=1, j0=10, vel=1)
    return "did it move?"

@register
def move_from_microscope_to_opentrons(speed: int = 1, timeout: int = 2) -> str:
    """
    """
    robot = Dorna()
    robot.connect("192.168.43.122")
    robot.set_motor(1)    
    robot.play(timeout=-1, cmd="jmove", rel=1, j0=10, vel=1)
    return "did it move?"
