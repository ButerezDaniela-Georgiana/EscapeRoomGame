EscapeRoomGame is a 2D top-down escape room game developed in Python using the Pygame library.
Architecture
The project follows a modular design, with each system isolated in its own module. game.py orchestrates the main loop and global state management, while player.py, room.py, menu.py, ui.py, and sound_manager.py handle their respective subsystems independently. Each puzzle — electric_puzzle.py, chemistry_puzzle.py, document_puzzle.py, and wardrobe_puzzle.py — is implemented as a self-contained component.
Rendering
The rendering pipeline uses alpha-blended overlay surfaces for dynamic lighting that reacts to the room's power state, shadow projection, and a tile-based floor grid. Player animation is driven by a spritesheet system with directional frame sequences and a configurable frame rate.
Audio
Audio is managed through a dedicated SoundManager class built on pygame.mixer, supporting both triggered sound effects and looping background music with fade-in transitions.
UI & State
The UI layer provides a real-time progress tracker, contextual interaction hints, and a message box system. Game state — including power status, inventory, and puzzle completion flags — is maintained centrally in game.py and passed to all components as needed.

Want me to generate a README.md file ready for GitHub?
