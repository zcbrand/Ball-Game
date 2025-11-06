"""
Integration test for Phase 3.

Tests complete gameplay with obstacles, scoring, and player interaction.
"""

import sys
import os
import pygame

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_full_gameplay_with_obstacles():
    """Test complete gameplay with obstacles and scoring."""
    from src.game import Game
    from src.config import FPS

    try:
        # Use dummy video driver
        os.environ['SDL_VIDEODRIVER'] = 'dummy'

        # Create game
        game = Game()

        # Transition to play state
        click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1})
        game.state_manager.handle_events([click_event])

        # Get play state
        play_state = game.state_manager.current_state

        # Simulate gameplay frames
        dt = 1.0 / FPS

        # Simulate enough frames for obstacles to spawn
        # Spawn interval is 1.5 seconds, so need ~90 frames
        for _ in range(100):
            play_state.update(dt)

        # Should have spawned obstacles
        obstacle_count = len(play_state.obstacle_manager.obstacles)
        if obstacle_count == 0:
            print(f"✗ No obstacles spawned after 100 frames")
            pygame.quit()
            return False

        print(f"  Spawned {obstacle_count} obstacles ✓")

        # Obstacles should be moving (scrolling left)
        if obstacle_count > 0:
            initial_x = play_state.obstacle_manager.obstacles[0].position.x

            # Simulate a few more frames
            for _ in range(10):
                play_state.update(dt)

            new_x = play_state.obstacle_manager.obstacles[0].position.x

            if new_x >= initial_x:
                print(f"✗ Obstacles not scrolling: x was {initial_x}, now {new_x}")
                pygame.quit()
                return False

            print(f"  Obstacles scrolling ✓")

        # Simulate many frames to test cleanup
        initial_count = len(play_state.obstacle_manager.obstacles)

        for _ in range(500):
            play_state.update(dt)

        # Old obstacles should have been cleaned up
        # (not accumulating infinitely)
        current_count = len(play_state.obstacle_manager.obstacles)

        if current_count > initial_count + 10:  # Allow some accumulation
            print(f"✗ Obstacles not being cleaned up: started with {initial_count}, now {current_count}")
            pygame.quit()
            return False

        print(f"  Obstacle cleanup working ✓")

        pygame.quit()
        print("✓ Full gameplay with obstacles working")
        return True

    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        return False


def test_scoring_integration():
    """Test scoring system in gameplay."""
    from src.states import PlayState, StateManager
    from src.config import FPS

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        # Create play state
        sm = StateManager()
        play_state = PlayState(sm)
        sm.add_state('play', play_state)
        sm.change_state('play')

        dt = 1.0 / FPS
        initial_score = play_state.score

        # Spawn an obstacle pair
        play_state.obstacle_manager.spawn_obstacle_pair()

        # Verify checkpoint created
        if len(play_state.obstacle_manager.checkpoints) == 0:
            print("✗ No checkpoint created with obstacle")
            pygame.quit()
            return False

        # Move player to checkpoint position
        checkpoint = play_state.obstacle_manager.checkpoints[0]
        play_state.player.position.x = checkpoint.position.x + 10
        play_state.player.position.y = 200

        # Update game (should trigger score check)
        play_state.update(dt)

        # Score should have increased
        if play_state.score != initial_score + 1:
            print(f"✗ Score didn't increase: was {initial_score}, now {play_state.score}")
            pygame.quit()
            return False

        # Update again - score shouldn't increase twice for same checkpoint
        prev_score = play_state.score
        play_state.update(dt)

        if play_state.score != prev_score:
            print(f"✗ Score increased twice for same checkpoint")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Scoring integration working")
        return True

    except Exception as e:
        print(f"✗ Scoring integration test failed: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        return False


def test_obstacle_gap_playable():
    """Test that obstacle gaps are large enough to be playable."""
    from src.systems import ObstacleManager
    from src.config import PLAYER_RADIUS

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        manager = ObstacleManager()

        # Spawn multiple obstacle pairs and check gaps
        for _ in range(20):
            manager.obstacles.clear()
            manager.spawn_obstacle_pair()

            if len(manager.obstacles) >= 2:
                # Find top and bottom pipes
                top_pipe = next((obs for obs in manager.obstacles if obs.is_top), None)
                bottom_pipe = next((obs for obs in manager.obstacles if not obs.is_top), None)

                if top_pipe and bottom_pipe:
                    # Calculate gap size
                    # Top pipe: bottom edge is at position.y + height
                    # Bottom pipe: top edge is at position.y
                    gap_size = bottom_pipe.position.y - (top_pipe.position.y + top_pipe.height)

                    # Gap should be at least player diameter * 4 (from config PIPE_GAP_MULTIPLIER)
                    min_gap = PLAYER_RADIUS * 2 * 4

                    if gap_size < min_gap:
                        print(f"✗ Gap too small: {gap_size} < {min_gap}")
                        pygame.quit()
                        return False

        pygame.quit()
        print("✓ Obstacle gaps are playable")
        return True

    except Exception as e:
        print(f"✗ Gap playability test failed: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        return False


def run_integration_tests():
    """Run all Phase 3 integration tests."""
    print("=" * 50)
    print("Phase 3 - Integration Tests")
    print("=" * 50)

    tests = [
        ("Full Gameplay with Obstacles", test_full_gameplay_with_obstacles),
        ("Scoring Integration", test_scoring_integration),
        ("Obstacle Gap Playability", test_obstacle_gap_playable),
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
