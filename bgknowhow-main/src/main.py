import pygame
import sys
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.game_engine import GameEngine
from src.asset_loader import AssetManager
from src.ui_renderer import UIRenderer


RED = (200, 50, 50)
GREEN = (50, 200, 50)
PURPLE_TIER = (150, 50, 200)
YELLOW_COMBAT = (200, 200, 50)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sylvanas Battlegrounds - Recruit Phase")
    clock = pygame.time.Clock()

    
    engine = GameEngine()
    assets = AssetManager()
    renderer = UIRenderer(screen, assets)

    
    buttons = {
        "upgrade": {"rect": pygame.Rect(600, 5, 150, 50), "color": PURPLE_TIER},
        "refresh": {"rect": pygame.Rect(760, 5, 150, 50), "color": GREEN},
        "end_turn": {"rect": pygame.Rect(920, 5, 150, 50), "color": RED},
    }

    running = True
    while running:
        
        buttons["upgrade"]["text"] = f"Upgrade ({engine.player.upgrade_cost}g)"
        buttons["refresh"]["text"] = "Refresh (1g)"
        buttons["end_turn"]["text"] = "End Turn"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                
                if buttons["upgrade"]["rect"].collidepoint(pos):
                    engine.upgrade_tavern()
                elif buttons["refresh"]["rect"].collidepoint(pos):
                    engine.refresh_shop()
                elif buttons["end_turn"]["rect"].collidepoint(pos):
                    engine.start_next_turn()

                
                for card in engine.player.shop[:]:
                    if card.rect.collidepoint(pos):
                        engine.buy_minion(card)

                
                for card in engine.player.hand[:]:
                    if card.rect.collidepoint(pos):
                        engine.play_minion(card)

                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                for card in engine.player.shop:
                    if card.rect.collidepoint(pos):
                        engine.toggle_freeze(card)

        
        while engine.player.discover_queue:
            options = engine.player.discover_queue[0]
            renderer.draw_discover_popup(options)
            waiting_choice = True
            while waiting_choice:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                        click_pos = ev.pos
                        for i in range(len(options)):
                            rect = pygame.Rect(300 + i*200, 300, 150, 200)
                            if rect.collidepoint(click_pos):
                                engine.resolve_discover_choice(i)
                                waiting_choice = False

        
        renderer.draw_game(engine.player, buttons)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
