"""
Test suite for Phase 3 - Obstacles.

Tests obstacle creation, spawning, movement, and scoring.
"""

import sys
import os
import pygame

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_imports():
    """Test that all Phase 3 modules can be imported."""
    try:
        from src.entities import Obstacle, ScoreCheckpoint
        from src.systems import ObstacleManager
        print("✓ All Phase 3 imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_obstacle_creation():
    """Test Obstacle class creation and attributes."""
    from src.entities import Obstacle
    from src.config import OBSTACLE_WIDTH

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        # Create bottom pipe
        bottom_pipe = Obstacle(x=100, y=200, height=150, is_top=False)

        if bottom_pipe.position.x != 100:
            print(f"✗ Bottom pipe X wrong: expected 100, got {bottom_pipe.position.x}")
            pygame.quit()
            return False

        if bottom_pipe.position.y != 200:
            print(f"✗ Bottom pipe Y wrong: expected 200, got {bottom_pipe.position.y}")
            pygame.quit()
            return False

        if bottom_pipe.height != 150:
            print(f"✗ Bottom pipe height wrong: expected 150, got {bottom_pipe.height}")
            pygame.quit()
            return False

        if bottom_pipe.width != OBSTACLE_WIDTH:
            print(f"✗ Obstacle width wrong: expected {OBSTACLE_WIDTH}, got {bottom_pipe.width}")
            pygame.quit()
            return False

        # Create top pipe (should adjust Y position)
        top_pipe = Obstacle(x=100, y=200, height=150, is_top=True)

        # For top pipes, position.y should be adjusted by subtracting height
        expected_y = 200 - 150
        if top_pipe.position.y != expected_y:
            print(f"✗ Top pipe Y adjustment wrong: expected {expected_y}, got {top_pipe.position.y}")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Obstacle creation correct")
        return True

    except Exception as e:
        print(f"✗ Obstacle creation test failed: {e}")
        pygame.quit()
        return False


def test_obstacle_movement():
    """Test Obstacle scrolling movement."""
    from src.entities import Obstacle
    from src.config import OBSTACLE_SPEED, FPS

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        obstacle = Obstacle(x=300, y=100, height=100, is_top=False)
        initial_x = obstacle.position.x

        # Update for one frame
        dt = 1.0 / FPS
        obstacle.update(dt)

        # Obstacle should have moved left
        expected_delta = OBSTACLE_SPEED * dt * FPS  # Should be ~OBSTACLE_SPEED
        actual_delta = initial_x - obstacle.position.x

        if abs(actual_delta - expected_delta) > 0.1:
            print(f"✗ Obstacle movement wrong: expected ~{expected_delta}, got {actual_delta}")
            pygame.quit()
            return False

        if obstacle.position.x >= initial_x:
            print(f"✗ Obstacle didn't move left: was {initial_x}, now {obstacle.position.x}")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Obstacle movement correct")
        return True

    except Exception as e:
        print(f"✗ Obstacle movement test failed: {e}")
        pygame.quit()
        return False


def test_obstacle_offscreen():
    """Test obstacle off-screen detection."""
    from src.entities import Obstacle

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        # Create obstacle on-screen
        obstacle = Obstacle(x=100, y=100, height=100, is_top=False)

        if obstacle.is_offscreen():
            print("✗ Obstacle should not be off-screen at x=100")
            pygame.quit()
            return False

        # Move obstacle off-screen
        obstacle.position.x = -200

        if not obstacle.is_offscreen():
            print("✗ Obstacle should be off-screen at x=-200")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Obstacle off-screen detection correct")
        return True

    except Exception as e:
        print(f"✗ Obstacle off-screen test failed: {e}")
        pygame.quit()
        return False


def test_score_checkpoint():
    """Test ScoreCheckpoint creation and collision."""
    from src.entities import ScoreCheckpoint

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        checkpoint = ScoreCheckpoint(x=300)

        # Check initial state
        if checkpoint.scored:
            print("✗ Checkpoint should not be scored initially")
            pygame.quit()
            return False

        # Get collision rect
        rect = checkpoint.get_rect()

        if rect.x != 300:
            print(f"✗ Checkpoint rect X wrong: expected 300, got {rect.x}")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ ScoreCheckpoint working correctly")
        return True

    except Exception as e:
        print(f"✗ ScoreCheckpoint test failed: {e}")
        pygame.quit()
        return False


def test_obstacle_manager_creation():
    """Test ObstacleManager initialization."""
    from src.systems import ObstacleManager

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        manager = ObstacleManager()

        # Check initial state
        if len(manager.obstacles) != 0:
            print(f"✗ Manager should start with 0 obstacles, has {len(manager.obstacles)}")
            pygame.quit()
            return False

        if len(manager.checkpoints) != 0:
            print(f"✗ Manager should start with 0 checkpoints, has {len(manager.checkpoints)}")
            pygame.quit()
            return False

        if manager.spawn_timer != 0:
            print(f"✗ Spawn timer should be 0, is {manager.spawn_timer}")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ ObstacleManager initialization correct")
        return True

    except Exception as e:
        print(f"✗ ObstacleManager creation test failed: {e}")
        pygame.quit()
        return False


def test_obstacle_spawning():
    """Test obstacle spawning mechanism."""
    from src.systems import ObstacleManager

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        manager = ObstacleManager()

        # Spawn multiple times to ensure we get a full pair
        # (randomization might create short pipes that don't meet min height)
        spawned_full_pair = False

        for _ in range(10):  # Try up to 10 times
            manager.obstacles.clear()
            manager.checkpoints.clear()

            manager.spawn_obstacle_pair()

            if len(manager.obstacles) >= 2:
                spawned_full_pair = True
                break

        if not spawned_full_pair:
            print(f"✗ Never spawned 2 obstacles after 10 tries")
            pygame.quit()
            return False

        # Should always create a checkpoint
        if len(manager.checkpoints) != 1:
            print(f"✗ Should spawn 1 checkpoint, got {len(manager.checkpoints)}")
            pygame.quit()
            return False

        # At least one obstacle should be created
        if len(manager.obstacles) == 0:
            print("✗ Should spawn at least one obstacle")
            pygame.quit()
            return False

        # If we have 2 obstacles, check they have different orientations
        if len(manager.obstacles) >= 2:
            has_top = any(obs.is_top for obs in manager.obstacles)
            has_bottom = any(not obs.is_top for obs in manager.obstacles)

            if not (has_top and has_bottom):
                print("✗ Should have both top and bottom pipes when spawning pair")
                pygame.quit()
                return False

        pygame.quit()
        print("✓ Obstacle spawning correct")
        return True

    except Exception as e:
        print(f"✗ Obstacle spawning test failed: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        return False


def test_timer_based_spawning():
    """Test timer-based automatic spawning."""
    from src.systems import ObstacleManager
    from src.config import FPS

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        manager = ObstacleManager()
        dt = 1.0 / FPS

        # Simulate frames until first spawn
        # spawn_interval is 1.5 seconds, so need 90 frames at 60 FPS
        frames_needed = int(manager.spawn_interval * FPS) + 1

        for _ in range(frames_needed):
            manager.update(dt)

        # Should have spawned at least one obstacle pair
        if len(manager.obstacles) == 0:
            print(f"✗ No obstacles spawned after {frames_needed} frames")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Timer-based spawning working")
        return True

    except Exception as e:
        print(f"✗ Timer-based spawning test failed: {e}")
        pygame.quit()
        return False


def test_obstacle_cleanup():
    """Test off-screen obstacle removal."""
    from src.systems import ObstacleManager
    from src.entities import Obstacle

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        manager = ObstacleManager()

        # Add an off-screen obstacle
        offscreen_obs = Obstacle(x=-200, y=100, height=100, is_top=False)
        manager.obstacles.append(offscreen_obs)

        # Add an on-screen obstacle
        onscreen_obs = Obstacle(x=300, y=100, height=100, is_top=False)
        manager.obstacles.append(onscreen_obs)

        # Trigger cleanup
        manager._cleanup_offscreen()

        # Should have removed off-screen obstacle
        if len(manager.obstacles) != 1:
            print(f"✗ Should have 1 obstacle after cleanup, has {len(manager.obstacles)}")
            pygame.quit()
            return False

        # Remaining obstacle should be the on-screen one
        if manager.obstacles[0].position.x != 300:
            print(f"✗ Wrong obstacle removed")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Obstacle cleanup working")
        return True

    except Exception as e:
        print(f"✗ Obstacle cleanup test failed: {e}")
        pygame.quit()
        return False


def test_scoring_system():
    """Test score checkpoint collision detection."""
    from src.systems import ObstacleManager
    from src.entities import Player

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        manager = ObstacleManager()
        player = Player()

        # Spawn obstacle pair (creates checkpoint)
        manager.spawn_obstacle_pair()

        # Move player to checkpoint position
        if len(manager.checkpoints) > 0:
            checkpoint = manager.checkpoints[0]
            player.position.x = checkpoint.position.x
            player.position.y = 200

            # Check score
            score = manager.check_score(player.get_rect())

            if score != 1:
                print(f"✗ Should score 1 point, got {score}")
                pygame.quit()
                return False

            # Check again - should not score twice
            score = manager.check_score(player.get_rect())

            if score != 0:
                print(f"✗ Should not score twice, got {score}")
                pygame.quit()
                return False

        pygame.quit()
        print("✓ Scoring system working")
        return True

    except Exception as e:
        print(f"✗ Scoring system test failed: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        return False


def run_all_tests():
    """Run all Phase 3 tests."""
    print("=" * 50)
    print("Phase 3 - Obstacles Tests")
    print("=" * 50)

    tests = [
        ("Module Imports", test_imports),
        ("Obstacle Creation", test_obstacle_creation),
        ("Obstacle Movement", test_obstacle_movement),
        ("Obstacle Off-screen Detection", test_obstacle_offscreen),
        ("Score Checkpoint", test_score_checkpoint),
        ("ObstacleManager Creation", test_obstacle_manager_creation),
        ("Obstacle Spawning", test_obstacle_spawning),
        ("Timer-based Spawning", test_timer_based_spawning),
        ("Obstacle Cleanup", test_obstacle_cleanup),
        ("Scoring System", test_scoring_system),
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
