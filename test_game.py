from game import Game

def test_initialization(game: Game):
    assert game.screen_width == 750
    assert game.lives == 3
    assert game.run is True
    assert len(game.obstacles) == 4
    assert len(game.aliens_group) == 5 * 11

def test_create_aliens(game: Game):
    alien_types = [alien.type for alien in game.aliens_group]
    assert alien_types.count(3) == 11 
    assert alien_types.count(2) == 22 
    assert alien_types.count(1) == 22 

def test_move_aliens_direction_change(game: Game):
    first_positions = [alien.rect.x for alien in game.aliens_group]
    game.aliens_direction = 1
    game.move_aliens()

    assert any(p != q for p, q in zip(first_positions, [a.rect.x for a in game.aliens_group]))

    for alien in game.aliens_group:
        alien.rect.right = game.screen_width + game.offset // 2
    game.move_aliens()
    assert game.aliens_direction == -1

def test_alien_shoot_laser(game: Game):
    pre = len(game.alien_lasers_group)
    game.alien_shoot_laser()
    assert len(game.alien_lasers_group) == pre + 1
    laser = next(iter(game.alien_lasers_group))
    assert isinstance(laser, Laser)
    assert laser.speed == -6  

def test_create_mystery_ship(game: Game):
    game.create_mystery_ship()
    assert len(game.mystery_ship_group) == 1
    ship = next(iter(game.mystery_ship_group))
    assert isinstance(ship, MysteryShip)

def test_check_for_collisions_laser_hits_alien(game: Game):

    game.explosion_sound = type('MockSound', (), {'play': lambda self: None})()
    
    alien = next(iter(game.aliens_group))
    laser = Laser(alien.rect.center, 6, game.screen_height) 
    game.spaceship_group.sprite.lasers_group.add(laser)

    game.check_for_collisions()

    assert alien not in game.aliens_group
    assert laser not in game.spaceship_group.sprite.lasers_group

def test_check_for_collisions_laser_hits_mystery(game: Game):

    game.explosion_sound = type('MockSound', (), {'play': lambda self: None})()
    
    game.create_mystery_ship()
    ship = next(iter(game.mystery_ship_group))
    laser = Laser(ship.rect.center, 6, game.screen_height)  
    game.spaceship_group.sprite.lasers_group.add(laser)
    pre_score = game.score
    game.check_for_collisions()

    assert ship not in game.mystery_ship_group
    assert game.score == pre_score + 500