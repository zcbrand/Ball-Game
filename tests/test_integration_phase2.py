"""
Integration test for Phase 2.

Tests the complete game flow from title to gameplay.
"""

import sys
import os
import pygame

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_full_game_flow():
    """Test complete game initialization and basic gameplay loop."""
    from src.game import Game
    from src.config import FPS

    try:
        # Use dummy video driver
        os.environ['SDL_VIDEODRIVER'] = 'dummy'

        # Create game
        game = Game()

        # Verify game starts in title state
        if game.state_manager.current_state_name != 'title':
            print(f"✗ Game should start in title state, got {game.state_manager.current_state_name}")
            pygame.quit()
            return False

        # Simulate click to transition to play
        click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1})
        game.state_manager.handle_events([click_event])

        # Should now be in play state
        if game.state_manager.current_state_name != 'play':
            print(f"✗ Should be in play state after click, got {game.state_manager.current_state_name}")
            pygame.quit()
            return False

        # Get play state
        play_state = game.state_manager.current_state

        # Record initial player position
        initial_y = play_state.player.position.y

        # Simulate a few frames of gameplay (player should fall)
        dt = 1.0 / FPS
        for _ in range(10):
            play_state.update(dt)

        # Player should have fallen (y increased)
        if play_state.player.position.y <= initial_y:
            print(f"✗ Player didn't fall: was {initial_y}, now {play_state.player.position.y}")
            pygame.quit()
            return False

        # Simulate jump
        play_state.player.jump()

        # Simulate a few more frames (player should rise)
        current_y = play_state.player.position.y
        for _ in range(5):
            play_state.update(dt)

        # Player should have risen (y decreased)
        if play_state.player.position.y >= current_y:
            print(f"✗ Player didn't rise after jump: was {current_y}, now {play_state.player.position.y}")
            pygame.quit()
            return False

        # Simulate many frames (player should eventually hit ground)
        for _ in range(200):
            play_state.update(dt)

        # Player should be at ground
        if abs(play_state.player.position.y - play_state.ground_y) > 1:
            print(f"✗ Player didn't reach ground: at {play_state.player.position.y}, ground is {play_state.ground_y}")
            pygame.quit()
            return False

        # Player should not be jumping when on ground
        if play_state.player.is_jumping:
            print("✗ Player should not be jumping when on ground")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Full game flow working correctly")
        return True

    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        return False


def run_integration_tests():
    """Run all integration tests."""
    print("=" * 50)
    print("Phase 2 - Integration Tests")
    print("=" * 50)

    tests = [
        ("Full Game Flow (Title -> Play -> Gameplay)", test_full_game_flow),
    ]

    results = []
    for name, test_func in tests:
        print(f"\n[{name}]")
        result = test_func()
        results.append((name, result))

    # Summary
    print("\n" + "=" * 50)
    print("Integration Test Summary")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {name}")

    print(f"\n{passed}/{total} integration tests passed")

    return passed == total


if __name__ == '__main__':
    success = run_integration_tests()
    sys.exit(0 if success else 1)
