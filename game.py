import pygame
from spaceship import Spaceship
from alien import Alien
from obstacle import Obstacle

class Game():
	def __init__(self, screen_width, screen_height):
		self.spaceship = pygame.sprite.GroupSingle()
		self.spaceship.add(Spaceship(screen_width, screen_height))
		self.obstacle_1 = Obstacle(screen_width/4 - 128,screen_height - 100)
		self.obstacle_2 = Obstacle((screen_width/4)*2 - 128,screen_height - 100)
		self.obstacle_3 = Obstacle((screen_width/4)*3 - 128,screen_height - 100)
		self.obstacle_4 = Obstacle((screen_width/4)*4 - 128,screen_height - 100)
		self.aliens = pygame.sprite.Group()
		self.alien_direction = 1
		self.screen_width = screen_width
		self.create_aliens()

	def create_aliens(self):
		for row in range(5):
			for column in range(11):
				x = 75 + column * 55
				y = 110 + row * 55

				if row == 0:
					alien_type = 3
				elif row in (1,2):
					alien_type = 2
				else:
					alien_type = 1

				alien = Alien(alien_type, x + self.offset/2, y)
				self.aliens_group.add(alien)

	def move_aliens(self):
		self.aliens_group.update(self.aliens_direction)

		alien_sprites = self.aliens_group.sprites()
		for alien in alien_sprites:
			if alien.rect.right >= self.screen_width + self.offset/2:
				self.aliens_direction = -1
				self.alien_move_down(2)
			elif alien.rect.left <= self.offset/2:
				self.aliens_direction = 1
				self.alien_move_down(2)

	def alien_move_down(self, distance):
		if self.aliens_group:
			for alien in self.aliens_group.sprites():
				alien.rect.y += distance

	def alien_shoot_laser(self):
		if self.aliens_group.sprites():
			random_alien = random.choice(self.aliens_group.sprites())
			laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height)
			self.alien_lasers_group.add(laser_sprite)

	def create_mystery_ship(self):
		self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))

	def check_for_collisions(self):
		#Spaceship
		if self.spaceship_group.sprite.lasers_group:
			for laser_sprite in self.spaceship_group.sprite.lasers_group:
				
				aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
				if aliens_hit:
					self.explosion_sound.play()
					for alien in aliens_hit:
						self.score += alien.type * 100
						self.check_for_highscore()
						laser_sprite.kill()

				if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
					self.score += 500
					self.explosion_sound.play()
					self.check_for_highscore()
					laser_sprite.kill()

				for obstacle in self.obstacles:
					if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
						laser_sprite.kill()

		#Alien Lasers
		if self.alien_lasers_group:
			for laser_sprite in self.alien_lasers_group:
				if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
					laser_sprite.kill()
					self.lives -= 1
					if self.lives == 0:
						self.game_over()

				for obstacle in self.obstacles:
					if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
						laser_sprite.kill()

		if self.aliens_group:
			for alien in self.aliens_group:
				for obstacle in self.obstacles:
					pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

				if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
					self.game_over()
