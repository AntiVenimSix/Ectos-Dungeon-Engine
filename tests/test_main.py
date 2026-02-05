import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import main


def setup_basic_state():
    main.dungeon = []
    main.items = []
    main.enemies = []
    main.inventory = {}
    main.life = 95
    main.maxlife = 100
    main.currentRoom = 0
    main.equipped_item = None


def test_pickup_removes_item_from_room():
    setup_basic_state()
    sword = {"name": "Sword", "damage": 3, "idnum": "sword"}
    main.dungeon = [{"desc": "Start", "item": sword, "doors": [], "enemies": []}]

    main.decideAction("1")

    assert main.inventory["sword"] == sword
    assert main.dungeon[0]["item"] is None


def test_fight_removes_defeated_enemy(monkeypatch):
    setup_basic_state()
    enemy = {"name": "Slime", "mindamage": 0, "maxdamage": 0, "hp": 3}
    main.dungeon = [{"desc": "Pit", "item": None, "doors": [], "enemies": [enemy]}]

    rolls = [3, 0]

    def fake_randint(_min, _max):
        return rolls.pop(0) if rolls else 0

    monkeypatch.setattr(main.random, "randint", fake_randint)

    main.decideAction("2")

    assert main.dungeon[0]["enemies"] == []


def test_equipped_item_increases_damage(monkeypatch):
    setup_basic_state()
    dagger = {"name": "Dagger", "damage": 2, "idnum": "dagger"}
    enemy = {"name": "Rat", "mindamage": 0, "maxdamage": 0, "hp": 6}
    main.inventory = {"dagger": dagger}
    main.dungeon = [{"desc": "Hall", "item": None, "doors": [], "enemies": [enemy]}]

    monkeypatch.setattr("builtins.input", lambda _: "Dagger")
    main.decideAction("4")

    rolls = [4, 0]

    def fake_randint(_min, _max):
        return rolls.pop(0) if rolls else 0

    monkeypatch.setattr(main.random, "randint", fake_randint)

    main.decideAction("2")

    assert main.equipped_item == dagger
    assert main.dungeon[0]["enemies"] == []


def test_invalid_door_does_not_change_room(monkeypatch):
    setup_basic_state()
    main.dungeon = [{"desc": "Start", "item": None, "doors": [99], "enemies": []}]
    monkeypatch.setattr(main.random, "choice", lambda _doors: 99)

    main.decideAction("3")

    assert main.currentRoom == 0


def test_load_dungeon_success(tmp_path):
    payload = {
        "dungeon": [{"desc": "Start", "item": None, "doors": [], "enemies": []}],
        "items": [],
        "enemies": [],
    }
    path = tmp_path / "example.json"
    path.write_text(json.dumps(payload))

    dungeon, items, enemies = main.load_dungeon(path)

    assert dungeon == payload["dungeon"]
    assert items == payload["items"]
    assert enemies == payload["enemies"]
