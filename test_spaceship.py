# tests/test_spaceship.py
import pygame
from laser import Laser

def test_movement_limits(game: object):
    spaceship = game.spaceship_group.sprite
    spaceship.rect.right = spaceship.screen_width + 200
    spaceship.constrain_movement()
    assert spaceship.rect.right <= spaceship.screen_width

    spaceship.rect.left = -200
    spaceship.constrain_movement()
    assert spaceship.rect.left >= spaceship.offset

def test_laser_creation_and_recharge(game: object):
    spaceship = game.spaceship_group.sprite
    assert spaceship.laser_ready is True

    # Create a laser manually to test the functionality
    laser = Laser(spaceship.rect.center, 6, spaceship.screen_height)
    spaceship.lasers_group.add(laser)
    assert len(spaceship.lasers_group) == 1
    
    # Test laser recharge
    spaceship.laser_ready = False
    spaceship.laser_time = pygame.time.get_ticks() - spaceship.laser_delay - 10
    spaceship.recharge_laser()
    assert spaceship.laser_ready is True

def test_laser_update_kills_offscreen(game: object):
    laser = Laser((100, 100), 10, game.screen_height)
    
    # Move laser off screen
    while laser.rect.y > -20:  # Move beyond top of screen
        laser.update()
    
    assert not laser.alive()