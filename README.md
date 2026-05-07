EscapeRoomGame is a fully playable 2D escape room game built from scratch in Python, demonstrating end-to-end game development skills — from architecture design and rendering to UI, audio, and gameplay logic.
Tech Stack
Python · Pygame · Object-Oriented Design · Spritesheet Animation · pygame.mixer
Architecture & Design Patterns
Engineered with a modular, component-based architecture where each system (player, room, ui, sound_manager) is decoupled and independently maintainable. Puzzle logic is fully encapsulated in self-contained modules, making the system trivially extensible — adding a new puzzle requires no changes to existing code.
Rendering & Graphics
Implemented a custom rendering pipeline featuring dynamic lighting via alpha-blended overlay surfaces, real-time shadow projection, and a spritesheet-driven animation system with directional frame sequences and configurable playback speed.
Audio System
Designed a reusable SoundManager abstraction over pygame.mixer supporting layered audio — simultaneous sound effects and looping background music with fade-in transitions and graceful fallback when audio hardware is unavailable.
UI & State Management
Built a reactive UI layer with a real-time progress tracker, contextual interaction hints, and a modal message system. Global game state is managed centrally and propagated to components through clean interfaces, avoiding shared mutable state anti-patterns.
