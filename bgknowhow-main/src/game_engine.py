import json
import random
import pygame
import os
from copy import deepcopy
from src.models import Minion, Player

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "minions.json")

class GameEngine:
    def __init__(self):
        self.player = Player()
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                self.minion_pool = json.load(f)
        except FileNotFoundError:
            raise RuntimeError(f"minions.json not found!\nExpected at: {DATA_PATH}")

        self.refresh_shop(free=True)

    def start_next_turn(self):
        self.player.turn += 1
        self.player.max_gold = min(10, 2 + self.player.turn)
        self.player.gold = self.player.max_gold

        if self.player.upgrade_cost > 2:
            self.player.upgrade_cost -= 1

        self.refresh_shop(free=True)

    def refresh_shop(self, free=False):
        if not free:
            if self.player.gold < 1:
                print("Not enough gold to refresh!")
                return
            self.player.gold -= 1

        shop_size = 3 + (self.player.tavern_tier // 2)
        frozen_cards = [m for m in self.player.shop if m.is_frozen]
        slots_to_fill = shop_size - len(frozen_cards)

        available = self.minion_pool.get(f"tier{self.player.tavern_tier}", self.minion_pool.get("tier1", []))
        new_shop = []
        for _ in range(slots_to_fill):
            minion = Minion(deepcopy(random.choice(available)))
            minion.rect = pygame.Rect(100 + len(new_shop + frozen_cards) * 130, 120, 110, 150)
            new_shop.append(minion)

        self.player.shop = frozen_cards + new_shop
        self._update_shop_positions()

    def toggle_freeze(self, minion):
        minion.is_frozen = not minion.is_frozen

    def upgrade_tavern(self):
        if self.player.gold >= self.player.upgrade_cost and self.player.tavern_tier < 6:
            self.player.gold -= self.player.upgrade_cost
            self.player.tavern_tier += 1
            self.player.upgrade_cost = 5 + self.player.tavern_tier

    def buy_minion(self, minion):
        if self.player.gold < minion.cost:
            print(f"Not enough gold to buy {minion.name}!")
            return
        if len(self.player.hand) >= 10:
            print("Hand is full!")
            return

        self.player.gold -= minion.cost
        if minion in self.player.shop:
            self.player.shop.remove(minion)
        self.player.hand.append(minion)

        self.check_triple(minion)
        self._update_hand_positions()
        self._update_shop_positions()

    def check_triple(self, bought_minion):
        """چک کردن Triple و ایجاد Golden + Discover"""
        name = bought_minion.name
        same_cards = [m for m in self.player.hand if m.name == name]
        if len(same_cards) == 3:
            # حذف کارت‌های عادی
            for m in same_cards:
                self.player.hand.remove(m)
            # ایجاد Golden
            golden = deepcopy(same_cards[0])
            golden.is_golden = True
            golden.attack *= 2
            golden.health *= 2
            self.player.hand.append(golden)
            print(f"Triple! {name} becomes Golden!")

            
            self.player.discover_queue.append(self.generate_discover_options())

    def generate_discover_options(self):
        """سه کارت تصادفی Tier بالاتر برای Discover"""
        tier_next = min(6, self.player.tavern_tier + 1)
        options = deepcopy(self.minion_pool.get(f"tier{tier_next}", []))
        return random.sample(options, min(3, len(options)))

    def resolve_discover_choice(self, choice_index):
        """پس از انتخاب کارت توسط کاربر"""
        if not self.player.discover_queue:
            return
        options = self.player.discover_queue.pop(0)
        selected = Minion(options[choice_index])
        self.player.hand.append(selected)
        self._update_hand_positions()

    def play_minion(self, minion):
        if len(self.player.board) >= 7:
            print("Board is full!")
            return
        if minion in self.player.hand:
            self.player.hand.remove(minion)
        self.player.board.append(minion)
        self._update_hand_positions()
        self._update_board_positions()

    def _update_hand_positions(self):
        for i, m in enumerate(self.player.hand):
            m.rect.topleft = (100 + i * 130, 320)

    def _update_board_positions(self):
        for i, m in enumerate(self.player.board):
            m.rect.topleft = (100 + i * 130, 520)

    def _update_shop_positions(self):
        for i, m in enumerate(self.player.shop):
            m.rect.topleft = (100 + i * 130, 120)
