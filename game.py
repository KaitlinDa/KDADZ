import pygame
from player import Player
from items import red_potion
from trivia_room import TriviaGame
from gamestate import GameState
from menu import Menu
from lose_screen import LoseScreen
from hud import HUD
from midplayer import MidLevel
from item_shop import ItemShop

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Trivia Roguelite Game")

        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = GameState.MENU
        self.menu = Menu(self)
        self.hud = HUD(self)
        self.mid_level = MidLevel(self)

        self.player = Player(5, 100)  # Assuming Player initialization is correct
        self.player.add_item(red_potion, 1)  # Ensure red_potion is correctly imported
        self.trivia_room_instance = None
        self.current_level = 1

        self.lose_screen = LoseScreen(self.screen)
    
        self.item_shop = ItemShop(self.screen, self.player)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # Cap the frame rate at 60 FPS

        pygame.quit()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:  # Press 'L' key to simulate losing
                    self.transition_state(GameState.LOSE)
                elif event.key == pygame.K_s:  # Press 'S' key to go to the shop
                    self.transition_state(GameState.SHOP)
                elif event.key == pygame.K_m:  # Press 'M' key to return to mid-level screen
                    self.transition_state(GameState.MID_LEVEL)
                elif event.key == pygame.K_i:  # 'i' key to open the inventory
                    self.open_inventory()
            if self.current_state == GameState.MENU:
                self.menu.handle_events(events)
            elif self.current_state == GameState.MID_LEVEL:
                self.mid_level.handle_events(events)
            elif self.current_state == GameState.TRIVIA_ROOM and self.trivia_room_instance:
                self.trivia_room_instance.handle_events(events)
            elif self.current_state == GameState.LOSE:
                self.lose_screen.handle_event(event, self.transition_state)
            elif self.current_state == GameState.SHOP:
                self.item_shop.handle_event(event)

    def update(self):
        if self.current_state == GameState.MID_LEVEL:
            self.mid_level.update()
        elif self.current_state == GameState.TRIVIA_ROOM and self.trivia_room_instance:
            self.trivia_room_instance.update()
        elif self.current_state == GameState.LOSE:
            pass  
        elif self.current_state == GameState.SHOP:
            pass  

    def render(self):
        self.screen.fill((0, 0, 0))
        
        if self.current_state == GameState.MENU:
            mouse_pos = pygame.mouse.get_pos()
            self.menu.draw(mouse_pos)
        elif self.current_state == GameState.MID_LEVEL:
            self.mid_level.draw()
        elif self.current_state == GameState.TRIVIA_ROOM and self.trivia_room_instance:
            self.trivia_room_instance.render()
        elif self.current_state == GameState.LOSE:
            mouse_pos = pygame.mouse.get_pos()
            self.lose_screen.draw(mouse_pos)
        elif self.current_state == GameState.SHOP:
            self.item_shop.draw() 
        elif self.current_state == GameState.INVENTORY:
            self.player.inventory.draw(self.screen)

        if self.current_state in [GameState.MID_LEVEL, GameState.TRIVIA_ROOM]:
            self.hud.draw()

        pygame.display.flip()
        
    def trivia_room(self, selected_category):
        if self.trivia_room_instance is None:
            self.trivia_room_instance = TriviaGame(selected_category, self, self.screen)
        else:
            self.trivia_room_instance.category = selected_category
            self.trivia_room_instance.load_new_question()
        self.transition_state(GameState.TRIVIA_ROOM)

    def open_inventory(self):
        if self.current_state != GameState.INVENTORY:
            self.previous_state = self.current_state  
            self.current_state = GameState.INVENTORY  
        else:
            self.current_state = self.previous_state  


    def transition_state(self, new_state):
        self.current_state = new_state
        pygame.mixer.music.stop()
        
        if new_state == GameState.TRIVIA_ROOM:
            self.current_state = new_state
        # Load and play background music for the trivia room
            pygame.mixer.music.load('assets\Music\\trivia_room.mp3')
            pygame.mixer.music.play(-1)  # Loop the music
        elif new_state == GameState.MID_LEVEL:
            # Load and play background music for the mid-level
            pygame.mixer.music.load('assets\Music\Mid_Level.mp3')
            pygame.mixer.music.play(-1)  # Loop the music

        elif new_state == GameState.MENU:
            # Load and play background music for the menu
            pygame.mixer.music.load('assets\Music\main_menu.mp3')
            pygame.mixer.music.play(-1)  # Loop the music

        elif new_state == GameState.LOSE:
            # Load and play background music for the lose screen
            pygame.mixer.music.load('assets\Music\lose_screen.mp3')
            pygame.mixer.music.play(-1)  # Loop the music

        elif new_state == GameState.VICTORY:
            pygame.mixer.music.load('assets\Music\victory_screen.mp3')
            pygame.mixer.music.play(-1)
            
        elif new_state == GameState.SHOPKEEPER:
            pygame.mixer.music.load('assets\Music\shop_menu.mp3')
            pygame.mixer.music.play(-1)
        elif new_state == GameState.SHOP:
            pass

    def allow_redo(self):
        pass
    
    def skip_round(self):
        pass
    
    def trivia_room_logic():
        pass
