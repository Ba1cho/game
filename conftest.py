import os
import pytest
import pygame
from pathlib import Path
from game import Game

# Use the dummy video driver so pygame can initialise without a real display.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame.init()

# Silence pygame’s mixer during tests.
pygame.mixer.init = lambda *_, **__: None
pygame.mixer.Sound = lambda *_, **__: None
pygame.mixer.music.load = lambda *_, **__: None
pygame.mixer.music.play = lambda *_, **__: None

@pytest.fixture
def game(tmp_path: Path) -> Game:
    """Return a fresh Game instance with a temporary high‑score file."""
    # Monkey‑patch the path used by Game to read/write the highscore.
    original_path = Path("highscore.txt")
    tmp_path_file = tmp_path / "highscore.txt"
    Path.touch(tmp_path_file)

    # Patch the Game class to use the temporary file.
    def _patched_load_highscore(self):
    	try:
    	    with open(tmp_path_file, "r") as file:
    	        content = file.read().strip()
    	        self.highscore = int(content) if content else 0
    	except FileNotFoundError:
    	    self.highscore = 0


    def _patched_check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open(tmp_path_file, "w") as file:
                file.write(str(self.highscore))

    # Apply patches
    Game.load_highscore = _patched_load_highscore
    Game.check_for_highscore = _patched_check_for_highscore

    return Game(screen_width=750, screen_height=700, offset=50)