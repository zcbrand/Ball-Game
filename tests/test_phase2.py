"""
Test suite for Phase 2 - Player & Physics.

Tests player creation, physics calculations, and gameplay state.
"""

import sys
import os
import pygame

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_imports():
    """Test that all Phase 2 modules can be imported."""
    try:
        from src.entities import SpriteBase, Player
        from src.systems import PhysicsSystem
        from src.states import PlayState
        print("✓ All Phase 2 imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_player_creation():
    """Test Player class creation and attributes."""
    from src.entities import Player
    from src.config import PLAYER_RADIUS, PLAYER_START_X, PLAYER_START_Y

    try:
        # Initialize pygame for Vector2
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        # Create player
        player = Player()

        # Check initial position
        if player.position.x != PLAYER_START_X:
            print(f"✗ Player X position wrong: expected {PLAYER_START_X}, got {player.position.x}")
            pygame.quit()
            return False

        if player.position.y != PLAYER_START_Y:
            print(f"✗ Player Y position wrong: expected {PLAYER_START_Y}, got {player.position.y}")
            pygame.quit()
            return False

        # Check radius
        if player.radius != PLAYER_RADIUS:
            print(f"✗ Player radius wrong: expected {PLAYER_RADIUS}, got {player.radius}")
            pygame.quit()
            return False

        # Check initial state
        if player.is_jumping:
            print("✗ Player should not be jumping initially")
            pygame.quit()
            return False

        if player.jump_power != 0:
            print("✗ Player jump_power should be 0 initially")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Player creation correct")
        return True

    except Exception as e:
        print(f"✗ Player creation test failed: {e}")
        pygame.quit()
        return False


def test_player_jump():
    """Test Player jump mechanics."""
    from src.entities import Player
    from src.config import JUMP_POWER

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        player = Player()

        # Execute jump
        player.jump()

        # Check jump state
        if not player.is_jumping:
            print("✗ Player should be jumping after jump() call")
            pygame.quit()
            return False

        if player.jump_power != JUMP_POWER:
            print(f"✗ Jump power wrong: expected {JUMP_POWER}, got {player.jump_power}")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Player jump mechanics working")
        return True

    except Exception as e:
        print(f"✗ Player jump test failed: {e}")
        pygame.quit()
        return False


def test_player_rect():
    """Test Player collision rectangle."""
    from src.entities import Player

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        player = Player()
        rect = player.get_rect()

        # Check rect is pygame.Rect
        if not isinstance(rect, pygame.Rect):
            print(f"✗ get_rect() should return pygame.Rect, got {type(rect)}")
            pygame.quit()
            return False

        # Check rect dimensions
        expected_width = player.radius * 2
        expected_height = player.radius * 2

        if rect.width != expected_width or rect.height != expected_height:
            print(f"✗ Rect dimensions wrong: expected {expected_width}x{expected_height}, got {rect.width}x{rect.height}")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Player collision rect correct")
        return True

    except Exception as e:
        print(f"✗ Player rect test failed: {e}")
        pygame.quit()
        return False


def test_physics_system():
    """Test PhysicsSystem creation and gravity."""
    from src.systems import PhysicsSystem
    from src.entities import Player
    from src.config import GRAVITY, FPS

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        # Create physics system
        ground_y = 350.0
        physics = PhysicsSystem(ground_y)

        # Create player above ground
        player = Player()
        player.position.y = 100.0
        initial_y = player.position.y

        # Apply gravity for one frame (dt = 1/60)
        dt = 1.0 / FPS
        physics.apply_gravity(player, dt)

        # Player should have moved down
        if player.position.y <= initial_y:
            print(f"✗ Gravity not applied: position didn't change (was {initial_y}, now {player.position.y})")
            pygame.quit()
            return False

        # Check approximate gravity amount
        expected_delta = GRAVITY * dt * FPS  # Should be close to GRAVITY
        actual_delta = player.position.y - initial_y

        if abs(actual_delta - expected_delta) > 0.1:
            print(f"✗ Gravity amount wrong: expected ~{expected_delta}, got {actual_delta}")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Physics system gravity working")
        return True

    except Exception as e:
        print(f"✗ Physics system test failed: {e}")
        pygame.quit()
        return False


def test_physics_ground_clamp():
    """Test that physics clamps player to ground."""
    from src.systems import PhysicsSystem
    from src.entities import Player

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        ground_y = 350.0
        physics = PhysicsSystem(ground_y)

        # Create player below ground
        player = Player()
        player.position.y = 400.0  # Below ground
        player.is_jumping = True

        # Clamp to ground
        physics.clamp_to_ground(player)

        # Check player is at ground
        if player.position.y != ground_y:
            print(f"✗ Player not clamped to ground: expected {ground_y}, got {player.position.y}")
            pygame.quit()
            return False

        # Check jumping state reset
        if player.is_jumping:
            print("✗ Player should not be jumping after ground clamp")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Physics ground clamp working")
        return True

    except Exception as e:
        print(f"✗ Physics ground clamp test failed: {e}")
        pygame.quit()
        return False


def test_play_state():
    """Test PlayState creation and initialization."""
    from src.states import StateManager, PlayState
    from src.entities import Player

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        # Create state manager and play state
        sm = StateManager()
        play_state = PlayState(sm)
        sm.add_state('play', play_state)

        # Enter play state
        sm.change_state('play')

        # Check that player was created
        if play_state.player is None:
            print("✗ PlayState didn't create player in on_enter")
            pygame.quit()
            return False

        if not isinstance(play_state.player, Player):
            print(f"✗ PlayState player is wrong type: {type(play_state.player)}")
            pygame.quit()
            return False

        # Check physics system created
        if play_state.physics is None:
            print("✗ PlayState didn't create physics system")
            pygame.quit()
            return False

        # Check score initialized
        if play_state.score != 0:
            print(f"✗ PlayState score should start at 0, got {play_state.score}")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ PlayState initialization correct")
        return True

    except Exception as e:
        print(f"✗ PlayState test failed: {e}")
        pygame.quit()
        return False


def test_state_transition():
    """Test Title -> Play state transition."""
    from src.states import StateManager, TitleState, PlayState

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        # Create state manager with both states
        sm = StateManager()
        title_state = TitleState(sm)
        play_state = PlayState(sm)

        sm.add_state('title', title_state)
        sm.add_state('play', play_state)

        # Start in title
        sm.change_state('title')

        if sm.current_state_name != 'title':
            print(f"✗ Should start in title state, got {sm.current_state_name}")
            pygame.quit()
            return False

        # Simulate click to transition
        click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1})
        title_state.handle_events([click_event])

        # Check for state change request
        sm._check_state_transition()

        if sm.current_state_name != 'play':
            print(f"✗ Should transition to play state, still in {sm.current_state_name}")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ State transition working")
        return True

    except Exception as e:
        print(f"✗ State transition test failed: {e}")
        pygame.quit()
        return False


def run_all_tests():
    """Run all Phase 2 tests."""
    print("=" * 50)
    print("Phase 2 - Player & Physics Tests")
    print("=" * 50)

    tests = [
        ("Module Imports", test_imports),
        ("Player Creation", test_player_creation),
        ("Player Jump", test_player_jump),
        ("Player Collision Rect", test_player_rect),
        ("Physics Gravity", test_physics_system),
        ("Physics Ground Clamp", test_physics_ground_clamp),
        ("PlayState Initialization", test_play_state),
        ("Title -> Play Transition", test_state_transition),
    ]

    results = []
    for name, test_func in tests:
        print(f"\n[{name}]")
        result = test_func()
        results.append((name, result))

    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {name}")

    print(f"\n{passed}/{total} tests passed")

    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
