Shadow Runner

Shadow Runner is a simple 2D endless runner game built in Python using Pygame. The player automatically runs across the screen while avoiding obstacles, collecting coins, and staying ahead of a shadow that constantly chases from behind. As the game continues, the speed gradually increases, making it harder to survive and achieve a higher score.

I created this project to get more experience with Python and object-oriented programming while also learning how real-time game loops and game mechanics work. The goal was to build a complete game from scratch that was both fun to play and helped me improve as a programmer.

Features

- Endless side-scrolling gameplay
- Jumping system with gravity-based physics
- Randomly generated obstacles and collectible coins
- Shadow enemy that follows the player throughout the game
- Three difficulty settings (Easy, Normal, and Hard)
- Pause and help menus
- High score system that saves locally between sessions
- Increasing game speed over time to make the game progressively more difficult

Controls

| Key | Action |
|------|--------|
| Space / Up Arrow | Jump |
| P | Pause or Resume |
| Enter | Start or Restart |
| 1 / 2 / 3 | Select Difficulty |
| B | Return from Help Menu |
| Q | Quit from Game Over Screen |

Running the Game

Requirements:
- Python 3
- Pygame

Install Pygame:

```bash
pip install pygame
```

Run the game:

```bash
python3 shadow_runner.py
```

What I Learned

Building this project helped me become more comfortable with:
- Object-oriented programming and designing classes.
- Creating and managing a real-time game loop.
- Handling keyboard input and event-driven programming.
- Implementing collision detection using `pygame.Rect`.
- Simulating simple physics like gravity and jumping.
- Working with random object generation and difficulty scaling.
- Reading from and writing to local files for persistent high scores.
- Organizing a larger Python project into manageable components.

Future Improvements

Some features I would like to add in the future include:
- Animated sprites instead of simple shapes.
- Sound effects and background music.
- Parallax scrolling backgrounds.
- New obstacle and enemy types.
- Power-ups or temporary abilities.
- Online leaderboards.
- Additional game modes and maps.

Technologies Used

- Python 3
- Pygame
- Object-Oriented Programming (OOP)

This project was built as a personal learning experience to strengthen my Python programming skills and gain hands-on experience developing an interactive application from start to finish.
