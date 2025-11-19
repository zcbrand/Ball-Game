"""
Test suite for Phase 4 - Collision & Game Logic.

Tests collision detection, game over logic, and complete gameplay loop.
"""

import sys
import os
import pygame

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_imports():
    """Test that all Phase 4 modules can be imported."""
    try:
        from src.systems import CollisionSystem
        from src.states import GameOverState
        print("✓ All Phase 4 imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_collision_system_creation():
    """Test CollisionSystem initialization."""
    from src.systems import CollisionSystem

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        collision = CollisionSystem(ceiling_y=0, ground_y=350)

        if collision.ceiling_y != 0:
            print(f"✗ Ceiling Y wrong: expected 0, got {collision.ceiling_y}")
            pygame.quit()
            return False

        if collision.ground_y != 350:
            print(f"✗ Ground Y wrong: expected 350, got {collision.ground_y}")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ CollisionSystem creation correct")
        return True

    except Exception as e:
        print(f"✗ CollisionSystem creation test failed: {e}")
        pygame.quit()
        return False


def test_obstacle_collision_detection():
    """Test player-obstacle collision detection."""
    from src.systems import CollisionSystem
    from src.entities import Player, Obstacle

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        collision = CollisionSystem()
        player = Player()
        player.position.x = 100
        player.position.y = 200

        # Create obstacle that doesn't collide
        obstacle1 = Obstacle(x=300, y=100, height=100, is_top=False)

        if collision.check_obstacle_collision(player, [obstacle1]):
            print("✗ Should not detect collision when far apart")
            pygame.quit()
            return False

        # Create obstacle that overlaps player
        obstacle2 = Obstacle(x=90, y=190, height=100, is_top=False)

        if not collision.check_obstacle_collision(player, [obstacle2]):
            print("✗ Should detect collision when overlapping")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Obstacle collision detection working")
        return True

    except Exception as e:
        print(f"✗ Obstacle collision test failed: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        return False


def test_boundary_collision_detection():
    """Test ceiling and ground boundary collision detection."""
    from src.systems import CollisionSystem
    from src.entities import Player

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        collision = CollisionSystem(ceiling_y=0, ground_y=350)
        player = Player()

        # Player in safe zone
        player.position.y = 200

        if collision.check_boundary_collision(player):
            print("✗ Should not detect collision in safe zone")
            pygame.quit()
            return False

        # Player hits ceiling
        player.position.y = 10  # Player radius is 20, so this hits ceiling

        if not collision.check_boundary_collision(player):
            print("✗ Should detect ceiling collision")
            pygame.quit()
            return False

        # Player hits ground
        player.position.y = 340  # Just above ground

        if not collision.check_boundary_collision(player):
            print("✗ Should detect ground collision")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Boundary collision detection working")
        return True

    except Exception as e:
        print(f"✗ Boundary collision test failed: {e}")
        pygame.quit()
        return False


def test_check_all_collisions():
    """Test combined collision checking."""
    from src.systems import CollisionSystem
    from src.entities import Player, Obstacle

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        collision = CollisionSystem(ceiling_y=0, ground_y=350)
        player = Player()

        # Safe position
        player.position.x = 100
        player.position.y = 200

        if collision.check_all_collisions(player, []):
            print("✗ Should not detect collision in safe zone with no obstacles")
            pygame.quit()
            return False

        # Add obstacle collision
        obstacle = Obstacle(x=90, y=190, height=100, is_top=False)

        if not collision.check_all_collisions(player, [obstacle]):
            print("✗ Should detect obstacle collision")
            pygame.quit()
            return False

        # Test boundary collision (no obstacles)
        player.position.y = 10

        if not collision.check_all_collisions(player, []):
            print("✗ Should detect boundary collision")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ Combined collision detection working")
        return True

    except Exception as e:
        print(f"✗ Combined collision test failed: {e}")
        pygame.quit()
        return False


def test_gameover_state_creation():
    """Test GameOverState initialization."""
    from src.states import StateManager, GameOverState

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        sm = StateManager()
        gameover_state = GameOverState(sm)

        if gameover_state.final_score != 0:
            print(f"✗ Initial score should be 0, got {gameover_state.final_score}")
            pygame.quit()
            return False

        # Test set_score
        gameover_state.set_score(42)

        if gameover_state.final_score != 42:
            print(f"✗ Score should be 42, got {gameover_state.final_score}")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ GameOverState creation correct")
        return True

    except Exception as e:
        print(f"✗ GameOverState creation test failed: {e}")
        pygame.quit()
        return False


def test_gameover_state_transition():
    """Test GameOverState restart functionality."""
    from src.states import StateManager, TitleState, GameOverState

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        sm = StateManager()
        title_state = TitleState(sm)
        gameover_state = GameOverState(sm)

        sm.add_state('title', title_state)
        sm.add_state('gameover', gameover_state)

        # Start in game over
        sm.change_state('gameover')

        if sm.current_state_name != 'gameover':
            print(f"✗ Should be in gameover state")
            pygame.quit()
            return False

        # Simulate click to restart
        click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1})
        gameover_state.handle_events([click_event])

        # Check for state change request
        sm._check_state_transition()

        if sm.current_state_name != 'title':
            print(f"✗ Should transition to title state, in {sm.current_state_name}")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ GameOver restart working")
        return True

    except Exception as e:
        print(f"✗ GameOver restart test failed: {e}")
        pygame.quit()
        return False


def test_playstate_collision_integration():
    """Test that PlayState correctly handles collisions."""
    from src.states import StateManager, PlayState, GameOverState
    from src.entities import Obstacle

    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()

        sm = StateManager()
        play_state = PlayState(sm)
        gameover_state = GameOverState(sm)

        sm.add_state('play', play_state)
        sm.add_state('gameover', gameover_state)

        sm.change_state('play')

        # Position player to collide with obstacle
        play_state.player.position.x = 100
        play_state.player.position.y = 200

        # Add obstacle that will collide
        obstacle = Obstacle(x=90, y=190, height=100, is_top=False)
        play_state.obstacle_manager.obstacles.append(obstacle)

        # Update game (should trigger collision)
        play_state.update(0.016)  # One frame

        # Should have transitioned to game over
        sm._check_state_transition()

        if sm.current_state_name != 'gameover':
            print(f"✗ Should transition to gameover after collision, in {sm.current_state_name}")
            pygame.quit()
            return False

        # Check that score was passed
        if gameover_state.final_score != play_state.score:
            print(f"✗ Score not passed to gameover: play={play_state.score}, gameover={gameover_state.final_score}")
            pygame.quit()
            return False

        pygame.quit()
        print("✓ PlayState collision integration working")
        return True

    except Exception as e:
        print(f"✗ PlayState collision integration test failed: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        return False


def run_all_tests():
    """Run all Phase 4 tests."""
    print("=" * 50)
    print("Phase 4 - Collision & Game Logic Tests")
    print("=" * 50)

    tests = [
        ("Module Imports", test_imports),
        ("CollisionSystem Creation", test_collision_system_creation),
        ("Obstacle Collision Detection", test_obstacle_collision_detection),
        ("Boundary Collision Detection", test_boundary_collision_detection),
        ("Combined Collision Detection", test_check_all_collisions),
        ("GameOverState Creation", test_gameover_state_creation),
        ("GameOver Restart", test_gameover_state_transition),
        ("PlayState Collision Integration", test_playstate_collision_integration),
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
