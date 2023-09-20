## Description
This repository contains a collection of intermediate games (made with classes, OOP concepts and sprites) created using Python and the Pygame library.
These games serve as educational projects that helped me further improve myself with the Pygame library and Object Oriented Programming with the help of an online tutorial. 

## Installation
Clone or download the repository to your local machine.

## Dependencies
The game requires the following dependencies:

- Python 3
- Pygame (for graphics and sound)

You can install Pygame using pip:

```bash
pip install pygame
```

## Running the Games
To start playing, first navigate into the folder of the game that you want to play. Then run the following command, replacing the "game" with the name of the game you want to play:

```bash
python game.py
```

# Game Controls and Rules

## Monster Wrangler

### Controls
- Use the arrow keys or W, A, S, D to move around the screen.
- Use the SPACE bar to warp to the bottom of the screen.

### Rules
- At the top of the game window, the new target enemy is displayed. Your objective is to enter the arena and only catch the monster that is the current target.
- If you collide with the target, the monster dies, and a new target is selected.
- If you collide with enemies that are not currently the target, you will lose a health and teleport back to your starting position.
- If you are cornered by enemies, you can warp to safety with SPACE bar.

## Space Invaders

### Controls
- Use the arrow keys ( <- and -> ) or A and D to move horizontally across the screen.
- Use the SPACE bar to shoot lasers.

### Rules
- Alien ships descend from the top of the screen, and you need to shoot all of them down to move on to the next round.
- If aliens hit you with their lasers or breach your line of defenses at the bottom of the game window, you lose a life.

## Zombie Knight

### Controls
- Use the arrow keys ( <- and -> ) or A and D to move horizontally across the screen.
- Use the arrow key ↑ or W to slash with your sword.
- Use the SPACE bar to jump.

### Rules
- Zombies descend from the sky at regular intervals, and you need to last 30 seconds each round to survive the night.
- Once you successfully kill a zombie with your slash attack, you need to go up to the body to "stomp" on it and fully kill it. If you don't manage to stomp the zombie in time, it will rise from the dead!
- Once you permanently kill a zombie, a ruby will fall from the sky and start moving. If you catch the ruby, you will gain a bonus point and health, but if a zombie catches the ruby, another zombie will spawn.
- If you collide with an alive zombie, you will lose health.
- There are four portals at each corner of the map that the player, a zombie, and a ruby can use to teleport between them.

    
