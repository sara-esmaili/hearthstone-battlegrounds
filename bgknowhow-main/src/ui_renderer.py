import pygame

WHITE = (240,240,240); GRAY = (180,180,180); BLACK = (20,20,20); GOLD = (255,215,0)

class UIRenderer:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets

    def draw_card(self, m):
        color = GOLD if getattr(m, "is_golden", False) else GRAY
        pygame.draw.rect(self.screen, color, m.rect, border_radius=8)
        pygame.draw.rect(self.screen, BLACK, m.rect, 2, border_radius=8)
        self.screen.blit(self.assets.font_small.render(m.name[:12], True, BLACK), (m.rect.x+6, m.rect.y+8))
        self.screen.blit(self.assets.font_small.render(f"{m.attack}/{m.health}", True, BLACK), (m.rect.x+10, m.rect.y+120))

        
        keywords_text = ",".join(getattr(m, "keywords", []))
        if keywords_text:
            self.screen.blit(self.assets.font_small.render(keywords_text, True, (50,50,200)), (m.rect.x+6, m.rect.y+30))

        
        if getattr(m, "auras", []):
            aura_text = ",".join(m.auras)
            self.screen.blit(self.assets.font_small.render(aura_text, True, (200,50,50)), (m.rect.x+6, m.rect.y+45))

    def draw_game(self, player, buttons):
        self.screen.fill(WHITE)
        info = f"Turn {player.turn} | Gold {player.gold}/{player.max_gold} | Tavern {player.tavern_tier}"
        self.screen.blit(self.assets.font_big.render(info, True, BLACK), (20,10))

        for b in buttons.values():
            pygame.draw.rect(self.screen, b['color'], b['rect'], border_radius=8)
            self.screen.blit(self.assets.font_small.render(b['text'], True, BLACK), (b['rect'].x+10, b['rect'].y+15))

        for m in player.shop + player.hand + player.board:
            self.draw_card(m)

    def draw_discover_popup(self, options):
        """نمایش Discover با Pause بازی"""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        self.screen.blit(overlay, (0,0))
        for i, m_data in enumerate(options):
            rect = pygame.Rect(300 + i*200, 300, 150, 200)
            pygame.draw.rect(self.screen, (200,200,50), rect, border_radius=8)
            pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=8)
            name = m_data.get("name", "???")
            pygame.draw.rect(self.screen, (200,200,50), rect)
            self.screen.blit(self.assets.font_small.render(name, True, BLACK), (rect.x+10, rect.y+10))
        pygame.display.flip()
