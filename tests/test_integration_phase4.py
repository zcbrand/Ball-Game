"""
Integration test for Phase 4.

Tests complete gameplay loop from title through gameplay to game over and restart.
"""

import sys
import os
import pygame

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_complete_gameplay_loop():
    """Test the full gameplay cycle: Title → Play → GameOver → Title."""
    from src.game import Game
    from src.config import FPS
    from src.entities import Obstacle

    try:
        # Use dummy video driver
        os.environ['SDL_VIDEODRIVER'] = 'dummy'

        # Create game
        game = Game()

        # Start in title state
        if game.state_manager.current_state_name != 'title':
            print(f"✗ Should start in title state, got {game.state_manager.current_state_name}")
            pygame.quit()
            return False

        print("  ✓ Game starts in title state")

        # Transition to play
        click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1})
        game.state_manager.handle_events([click_event])

        if game.state_manager.current_state_name != 'play':
            print(f"✗ Should transition to play state")
            pygame.quit()
            return False

        print("  ✓ Transitioned to play state")

        # Get play state
        play_state = game.state_manager.current_state

        dt = 1.0 / FPS

        # Simulate some gameplay (score some points)
        play_state.obstacle_manager.spawn_obstacle_pair()

        # Move player to score a point
        if len(play_state.obstacle_manager.checkpoints) > 0:
            checkpoint = play_state.obstacle_manager.checkpoints[0]
            play_state.player.position.x = checkpoint.position.x + 10
            play_state.player.position.y = 200

            # Update to trigger score
            play_state.update(dt)

            if play_state.score < 1:
                print(f"✗ Should have scored at least 1 point")
                pygame.quit()
                return False

            print(f"  ✓ Scored {play_state.score} point(s)")

        # Force a collision (ground)
        play_state.player.position.y = 400  # Way below ground

        # Update - should trigger game over
        play_state.update(dt)

        # Check state transition happened
        game.state_manager._check_state_transition()

        if game.state_manager.current_state_name != 'gameover':
            print(f"✗ Should transition to gameover after collision, in {game.state_manager.current_state_name}")
            pygame.quit()
            return False

        print("  ✓ Game over triggered on collision")

        # Get gameover state
        gameover_state = game.state_manager.current_state

        # Check that score was passed
        final_score = play_state.score
        if gameover_state.final_score != final_score:
            print(f"✗ Score not passed correctly: expected {final_score}, got {gameover_state.final_score}")
            pygame.quit()
            return False

        print(f"  ✓ Final score passed correctly: {gameover_state.final_score}")

        # Restart game (click on game over screen)
        gameover_state.handle_events([click_event])
        game.state_manager._check_state_transition()

        if game.state_manager.current_state_name != 'title':
            print(f"✗ Should return to title state, in {game.state_manager.current_state_name}")
            pygame.quit()
            return False

        print("  ✓ Successfully returned to title state")

        # Try one more cycle to ensure it works multiple times
        game.state_manager.handle_events([click_event])

        if game.state_manager.current_state_name != 'play':
            print(f"✗ Should restart to play state")
            pygame.quit()
            return False

        print("  ✓ Game can restart successfully")

        pygame.quit()
        print("✓ Complete gameplay loop working perfectly")
        return True

    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        return False


def test_ground_collision_game_over():
    """Test that hitting the ground triggers game over."""
    from src.states import StateManager, PlayState, GameOverState
    from src.config import FPS

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        sm = StateManager()
        play_state = PlayState(sm)
        gameover_state = GameOverState(sm)

        sm.add_state('play', play_state)
        sm.add_state('gameover', gameover_state)
        sm.change_state('play')

        dt = 1.0 / FPS

        # Force player way below ground
        play_state.player.position.y = 500

        # Update (should detect ground collision)
        play_state.update(dt)
        sm._check_state_transition()

        if sm.current_state_name != 'gameover':
            print(f"✗ Should game over on ground collision")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Ground collision triggers game over")
        return True

    except Exception as e:
        print(f"✗ Ground collision test failed: {e}")
        pygame.quit()
        return False


def test_ceiling_collision_game_over():
    """Test that hitting the ceiling triggers game over."""
    from src.states import StateManager, PlayState, GameOverState
    from src.config import FPS

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        sm = StateManager()
        play_state = PlayState(sm)
        gameover_state = GameOverState(sm)

        sm.add_state('play', play_state)
        sm.add_state('gameover', gameover_state)
        sm.change_state('play')

        dt = 1.0 / FPS

        # Force player way above ceiling
        play_state.player.position.y = -10

        # Update (should detect ceiling collision)
        play_state.update(dt)
        sm._check_state_transition()

        if sm.current_state_name != 'gameover':
            print(f"✗ Should game over on ceiling collision")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Ceiling collision triggers game over")
        return True

    except Exception as e:
        print(f"✗ Ceiling collision test failed: {e}")
        pygame.quit()
        return False


def test_pipe_collision_game_over():
    """Test that hitting a pipe triggers game over."""
    from src.states import StateManager, PlayState, GameOverState
    from src.entities import Obstacle
    from src.config import FPS

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        sm = StateManager()
        play_state = PlayState(sm)
        gameover_state = GameOverState(sm)

        sm.add_state('play', play_state)
        sm.add_state('gameover', gameover_state)
        sm.change_state('play')

        dt = 1.0 / FPS

        # Position player
        play_state.player.position.x = 100
        play_state.player.position.y = 200

        # Add obstacle that overlaps player
        obstacle = Obstacle(x=90, y=190, height=100, is_top=False)
        play_state.obstacle_manager.obstacles.append(obstacle)

        # Update (should detect pipe collision)
        play_state.update(dt)
        sm._check_state_transition()

        if sm.current_state_name != 'gameover':
            print(f"✗ Should game over on pipe collision")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Pipe collision triggers game over")
        return True

    except Exception as e:
        print(f"✗ Pipe collision test failed: {e}")
        pygame.quit()
        return False


def run_integration_tests():
    """Run all Phase 4 integration tests."""
    print("=" * 50)
    print("Phase 4 - Integration Tests")
    print("=" * 50)

    tests = [
        ("Complete Gameplay Loop (Title→Play→GameOver→Title)", test_complete_gameplay_loop),
        ("Ground Collision Game Over", test_ground_collision_game_over),
        ("Ceiling Collision Game Over", test_ceiling_collision_game_over),
        ("Pipe Collision Game Over", test_pipe_collision_game_over),
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
