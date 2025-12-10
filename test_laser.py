import pygame
from laser import Laser

def test_laser_update_kill():
    laser = Laser(position=(0, 0), speed=5, screen_height=700)

    for _ in range(200):
        laser.update()
    assert not laser.alive()  