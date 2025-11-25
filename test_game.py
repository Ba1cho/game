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

def test_create_mystery_ship(game: Game):
    game.create_mystery_ship()
    assert len(game.mystery_ship_group) == 1
    ship = next(iter(game.mystery_ship_group))
    assert isinstance(ship, MysteryShip)