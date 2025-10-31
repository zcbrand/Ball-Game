"""
Test suite for Phase 1 - Foundation.

Tests that all core infrastructure is set up correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_imports():
    """Test that all Phase 1 modules can be imported."""
    try:
        from src import config
        from src.states import State, StateManager, TitleState
        from src import game
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_config_constants():
    """Test that config has all required constants."""
    from src import config

    required_constants = [
        'SCREEN_WIDTH', 'SCREEN_HEIGHT', 'FPS',
        'GRAVITY', 'JUMP_POWER', 'OBSTACLE_SPEED',
        'PLAYER_RADIUS', 'COLOR_SKY', 'COLOR_PLAYER'
    ]

    missing = []
    for const in required_constants:
        if not hasattr(config, const):
            missing.append(const)

    if missing:
        print(f"✗ Missing config constants: {', '.join(missing)}")
        return False

    print(f"✓ All {len(required_constants)} config constants present")
    return True


def test_state_manager():
    """Test StateManager functionality."""
    import pygame
    from src.states import StateManager, TitleState

    try:
        # Initialize pygame (needed for fonts)
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        # Create state manager
        sm = StateManager()

        # Create and add a state
        title = TitleState(sm)
        sm.add_state('title', title)

        # Change to title state
        sm.change_state('title')

        if sm.current_state_name != 'title':
            print(f"✗ State change failed: expected 'title', got '{sm.current_state_name}'")
            pygame.quit()
            return False

        print("✓ StateManager working correctly")
        pygame.quit()
        return True

    except Exception as e:
        print(f"✗ StateManager test failed: {e}")
        pygame.quit()
        return False


def test_game_class():
    """Test that Game class can be instantiated (without running the loop)."""
    import pygame
    from src.game import Game

    try:
        # Set SDL to use dummy video driver (no actual window)
        os.environ['SDL_VIDEODRIVER'] = 'dummy'

        # Create game instance
        game = Game()

        # Check that game is set up
        if not game.running:
            print("✗ Game not in running state after init")
            return False

        if game.state_manager.current_state_name != 'title':
            print("✗ Game not starting in title state")
            return False

        # Clean up
        pygame.quit()

        print("✓ Game class initializes correctly")
        return True

    except Exception as e:
        print(f"✗ Game class test failed: {e}")
        pygame.quit()
        return False


def run_all_tests():
    """Run all Phase 1 tests."""
    print("=" * 50)
    print("Phase 1 - Foundation Tests")
    print("=" * 50)

    tests = [
        ("Module Imports", test_imports),
        ("Config Constants", test_config_constants),
        ("StateManager", test_state_manager),
        ("Game Class", test_game_class),
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
