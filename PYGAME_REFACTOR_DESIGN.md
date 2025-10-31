# Ball Game - PyGame Refactor Design Document

## Executive Summary
This document outlines the design for refactoring the Ball Game from Adobe Flash/ActionScript to PyGame. The original game is a Flappy Bird-style game where a ball character navigates through pipe obstacles.

---

## Current State Analysis

### Technology Stack (Legacy)
- **Platform**: Adobe Flash/Animate (End-of-life)
- **Language**: ActionScript 3.0
- **File Format**: .fla (Flash source), .as (ActionScript)
- **Stage Size**: 550x400 pixels

### Game Mechanics Analysis

#### Core Components
1. **Player Character** - A ball with gravity-based physics
2. **Obstacles** - Pairs of pipes (top and bottom) with randomized gaps
3. **Collision Detection** - Hit testing between player and pipes/boundaries
4. **Scoring System** - Increments when player passes through pipe pairs
5. **Game States** - Title screen, playing, game over

#### Physics Constants
```actionscript
gravity: 10
jumpPowerBurst: 25
obstacleSpeed: 10
obTimeSpeed: 1500ms (obstacle spawn interval)
```

#### Game State Variables
- `gameState` - Game started flag
- `gameStart` - Game initialization flag
- `isJumping` - Jump state
- `stopObstacle` - Game over state
- `showScore` - Display score flag

#### Key Algorithms

**Gravity System**:
- Player continuously falls with gravity (10 pixels/frame)
- Jump applies burst force (25) that decays by 2 per frame
- Ground collision boundary

**Obstacle Spawning**:
- Timer-based (every 1.5 seconds)
- Random Y position for bottom pipe
- Top pipe positioned with fixed gap (4x player height)
- Invisible score checkpoint between pipes

**Collision Detection**:
- Player vs pipes (hitTestObject)
- Player vs ground/ceiling boundaries

---

## PyGame Architecture Design

### Project Structure
```
ball-game-pygame/
├── src/
│   ├── main.py              # Entry point
│   ├── game.py              # Main game class
│   ├── config.py            # Constants and configuration
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── player.py        # Player ball class
│   │   ├── obstacle.py      # Pipe obstacle class
│   │   └── sprite_base.py   # Base sprite class
│   ├── states/
│   │   ├── __init__.py
│   │   ├── state_manager.py # Game state machine
│   │   ├── title_state.py   # Title screen
│   │   ├── play_state.py    # Main gameplay
│   │   └── gameover_state.py # Game over screen
│   ├── systems/
│   │   ├── __init__.py
│   │   ├── physics.py       # Physics engine
│   │   ├── collision.py     # Collision detection
│   │   └── spawner.py       # Obstacle spawning system
│   └── utils/
│       ├── __init__.py
│       └── helpers.py       # Utility functions
├── assets/
│   ├── images/
│   │   ├── player.png
│   │   ├── pipe.png
│   │   ├── background.png
│   │   └── ground.png
│   ├── fonts/
│   │   └── game_font.ttf
│   └── sounds/          # Future: sound effects
├── tests/
│   └── test_*.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Class Diagram

```
Game (main loop, state management)
  └── StateManager
      ├── TitleState
      ├── PlayState
      │   ├── Player
      │   ├── ObstacleManager
      │   │   └── Obstacle (top/bottom pairs)
      │   ├── PhysicsSystem
      │   ├── CollisionSystem
      │   └── ScoreTracker
      └── GameOverState
```

---

## Detailed Component Design

### 1. Configuration (config.py)

```python
# Screen settings
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 400
FPS = 60

# Physics constants
GRAVITY = 10
JUMP_POWER = 25
JUMP_DECAY = 2

# Gameplay constants
OBSTACLE_SPEED = 10
OBSTACLE_SPAWN_INTERVAL = 1500  # milliseconds
PIPE_GAP_MULTIPLIER = 4  # times player height

# Colors
COLOR_SKY = (135, 206, 235)
COLOR_GROUND = (34, 139, 34)
COLOR_PIPE = (50, 205, 50)
```

### 2. Player Class (entities/player.py)

**Responsibilities**:
- Render player sprite
- Handle jump input
- Apply gravity physics
- Track position and velocity

**Key Methods**:
- `__init__(x, y, radius)`
- `jump()` - Apply jump force
- `update(dt)` - Update position with physics
- `draw(surface)` - Render to screen
- `get_rect()` - Return collision rectangle

**Attributes**:
- `position: Vector2`
- `velocity: Vector2`
- `jump_power: float`
- `is_jumping: bool`
- `radius: int`

### 3. Obstacle System (systems/spawner.py, entities/obstacle.py)

**ObstacleManager Responsibilities**:
- Spawn pipe pairs at intervals
- Move obstacles across screen
- Remove off-screen obstacles
- Track score checkpoints

**Obstacle Class**:
- `__init__(x, y, is_top=False)`
- `update(dt)` - Move horizontally
- `draw(surface)` - Render pipe
- `get_rect()` - Collision rectangle
- `is_offscreen()` - Check if can be removed

### 4. Physics System (systems/physics.py)

**Responsibilities**:
- Apply gravity to player
- Handle jump mechanics with decay
- Enforce ground/ceiling boundaries

**Key Functions**:
- `apply_gravity(entity, dt)`
- `apply_jump(entity, jump_power)`
- `clamp_to_bounds(entity, bounds)`

### 5. Collision System (systems/collision.py)

**Responsibilities**:
- Detect player-obstacle collisions
- Detect boundary collisions
- Handle collision responses

**Key Functions**:
- `check_collision(rect1, rect2)` - AABB collision
- `check_player_obstacles(player, obstacles)` - Returns collision bool
- `check_boundaries(player, ground_y, ceiling_y)` - Returns collision bool

### 6. State Manager (states/state_manager.py)

**Game States**:
1. **TITLE** - Display title and "Click to Play"
2. **PLAYING** - Active gameplay
3. **GAME_OVER** - Display score and restart option

**State Transitions**:
- TITLE → PLAYING (on mouse click)
- PLAYING → GAME_OVER (on collision)
- GAME_OVER → TITLE (on restart)

### 7. Main Game Loop (game.py)

```python
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.state_manager = StateManager()

    def run(self):
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

    def handle_events(self):
        # Process input

    def update(self, dt):
        # Update current state

    def draw(self):
        # Render current state
```

---

## Implementation Phases

### Phase 1: Foundation (Core Infrastructure)
- [ ] Set up project structure
- [ ] Create config.py with constants
- [ ] Implement Game class with main loop
- [ ] Implement StateManager base class
- [ ] Basic window rendering

**Deliverable**: Window opens, runs at 60 FPS, can close

### Phase 2: Player & Physics
- [ ] Create Player class
- [ ] Implement PhysicsSystem
- [ ] Add gravity
- [ ] Add jump mechanics (click to jump)
- [ ] Add ground collision

**Deliverable**: Controllable ball that falls and jumps

### Phase 3: Obstacles
- [ ] Create Obstacle class
- [ ] Implement ObstacleManager/Spawner
- [ ] Timer-based spawning
- [ ] Horizontal scrolling
- [ ] Randomized pipe positions
- [ ] Off-screen removal

**Deliverable**: Pipes spawn and scroll across screen

### Phase 4: Collision & Game Logic
- [ ] Implement CollisionSystem
- [ ] Player-obstacle collision detection
- [ ] Boundary collision (ceiling/ground)
- [ ] Game over on collision
- [ ] Score tracking (pass through pipes)

**Deliverable**: Functional game loop with collisions

### Phase 5: Game States & UI
- [ ] Implement TitleState (title screen)
- [ ] Implement PlayState (game logic)
- [ ] Implement GameOverState (score display)
- [ ] Add text rendering (score, titles)
- [ ] State transitions

**Deliverable**: Complete game with all screens

### Phase 6: Polish & Assets
- [ ] Create/import visual assets (sprites)
- [ ] Add background graphics
- [ ] Improve visual feedback
- [ ] Add particle effects (optional)
- [ ] Performance optimization

**Deliverable**: Polished, visually complete game

### Phase 7: Future Enhancements (from README)
- [ ] Restart function
- [ ] Enemy entities
- [ ] Player customization
- [ ] Start menu with options
- [ ] Improved hit detection
- [ ] Sound effects and music
- [ ] High score persistence

---

## Technical Considerations

### Coordinate System
- **Flash**: Origin top-left, Y increases downward
- **PyGame**: Same convention (no conversion needed)
- **Screen**: 550x400 (maintain original dimensions)

### Frame Rate Conversion
- **Flash**: Likely 24-30 FPS (implicit)
- **PyGame**: Target 60 FPS
- **Solution**: Delta-time (dt) based movement for frame-rate independence

### Physics Conversion
Original ActionScript uses frame-based physics:
```actionscript
player.y += gravity;  // Every frame
```

PyGame will use delta-time:
```python
player.y += gravity * dt * 60  # Scale to maintain same feel
```

### Collision Detection Upgrade
- **Flash**: `hitTestObject()` (basic bounding box)
- **PyGame**: `pygame.Rect.colliderect()` (equivalent)
- **Future**: Pixel-perfect collision with masks

### Asset Migration
- Flash assets (.fla) are not directly exportable
- **Options**:
  1. Recreate using PyGame shapes (simple geometric shapes)
  2. Create new sprite assets (PNG images)
  3. Use placeholder graphics initially

---

## Dependencies

### Required Python Packages
```
pygame >= 2.5.0
```

### Optional Packages
```
pytest >= 7.0.0        # Testing
pygame-gui >= 0.6.0    # Advanced UI (future)
```

---

## Testing Strategy

### Unit Tests
- `test_player.py` - Player physics and movement
- `test_obstacle.py` - Obstacle spawning and movement
- `test_collision.py` - Collision detection accuracy
- `test_physics.py` - Physics calculations

### Integration Tests
- Full game loop execution
- State transitions
- Score tracking accuracy

### Manual Testing
- Gameplay feel (jump height, obstacle speed)
- Collision detection fairness
- Visual quality and performance

---

## Migration Advantages

### Benefits of PyGame over Flash
1. **Cross-platform**: Windows, Mac, Linux
2. **Open-source**: No licensing issues
3. **Active development**: Ongoing support
4. **Modern Python**: Better tooling and libraries
5. **Web deployment**: Can use Pygame-web for browser
6. **Performance**: Better control over optimization
7. **Future-proof**: Not dependent on deprecated technology

### Challenges
1. **Asset recreation**: Need to rebuild visual assets
2. **Learning curve**: Team familiarity with PyGame
3. **Sound system**: Need to implement audio (not in original)
4. **Testing**: More comprehensive testing needed

---

## Performance Targets

- **FPS**: Stable 60 FPS
- **Memory**: < 50MB RAM
- **Startup time**: < 2 seconds
- **Input latency**: < 16ms (1 frame at 60 FPS)

---

## Code Quality Standards

- **PEP 8**: Follow Python style guide
- **Type hints**: Use for all function signatures
- **Docstrings**: Document all classes and public methods
- **Comments**: Explain complex algorithms
- **DRY principle**: Avoid code duplication
- **SOLID principles**: Especially Single Responsibility

---

## Version Control Strategy

- **Branch**: `claude/refactor-pygame-redesign-011CUfzsVMx6nEL4R9pqvcup`
- **Commits**: Atomic commits per feature/phase
- **Messages**: Clear, descriptive commit messages
- **Testing**: Test before each commit

---

## Success Criteria

The refactor is complete when:

1. ✅ All core gameplay mechanics work identically to Flash version
2. ✅ Game runs at stable 60 FPS
3. ✅ Code is well-structured and maintainable
4. ✅ All phases 1-5 are complete
5. ✅ Game is playable from start to finish
6. ✅ Score tracking works correctly
7. ✅ Collision detection is fair and accurate
8. ✅ Visual quality meets or exceeds original

---

## Timeline Estimate

- **Phase 1**: 1-2 hours
- **Phase 2**: 2-3 hours
- **Phase 3**: 2-3 hours
- **Phase 4**: 2-3 hours
- **Phase 5**: 2-3 hours
- **Phase 6**: 3-4 hours

**Total**: ~15-20 hours for phases 1-6

---

## Next Steps

**Awaiting instructions to proceed with implementation.**

Once approved, suggested approach:
1. Begin with Phase 1 (Foundation)
2. Commit and test after each phase
3. Iterate based on feedback
4. Progress through phases sequentially
