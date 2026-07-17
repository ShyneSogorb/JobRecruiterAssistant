SKILLS
Core Unreal Engine & C++ Skills
Unreal Engine: Working with it since 2018 (age 13), so long-term, self-taught familiarity.
C++: Main programming focus since 2021, primarily within Unreal Engine.
Blueprint (Unreal's visual scripting): Used since the beginning of working with Unreal.
Blueprint Widgets: Created dynamic UI widgets for players, including main menus, options/settings screens, and widgets that generate themselves based on underlying data.
User Interaction Systems: Built systems letting players interact with the world - doors, switches, computers, etc.
Editor Tooling: Built custom tools inside the Unreal Editor to speed up other developers' workflows.
Debugging: Comfortable working with stack traces, breakpoints, values, and memory across Unreal Engine, Visual Studio, VS Code, JetBrains Rider, and CLion.
Version Control
Perforce: Used for both local version control and server-based version control (hosted on AWS).
Git: Used for smaller projects (CV generator, a batch compiler tool for Unreal projects), during studies (paired with Unity), and to host a custom game engine on GitHub.
Tooling & Automation
Pipeline Automation: Wrote scripts and small applications to speed up repetitive tasks - e.g., automatic CV generation from data, batch image resizing.
Reflection (Unreal): Used Unreal's reflection system to find and read/write exposed variables at runtime.
Python: Used to build external tools such as an image resizer, file converter, audio modifier, video-to-audio extractor, and a multi-platform Unreal build compiler.
Technical UX: Exposed variables and settings to teammates (designers/artists) so they could work more independently without needing a programmer each time.
Performance & Low-Level Programming
Optimization: Focused on avoiding unnecessary heavy operations (like reallocations and large copies) and writing code that compilers can optimize well.
Multithreading: Moved heavy computational work off the main thread to keep games running smoothly.
Memory Management: Careful handling of object lifetimes for classes and structs.
Low-Level Error Handling: Designed a custom "abort system" for a lazy-evaluation graph - variables are wrapped in handlers linked to a custom deletion stack; on error, the program uses longjmp to exit safely, then the stack unwinds and releases memory correctly (avoiding double-deletion, memory leaks, and crashes), while still respecting normal stack destruction rules.
Cache Efficiency: Experience working with arrays and chunked arrays for processing large amounts of data, plus "Structure of Arrays" (SoA) C++ templates for cache-friendly layouts.
Lock-Free Programming: Used atomic operations for multithreaded features, including atomic queues and buffers.
SIMD (Single Instruction, Multiple Data): Used to move millions of bullets in real time using an SoA data structure that takes advantage of memory alignment.
Unreal Subsystems: Built a World Subsystem acting as a bullet pool for fast spawning/despawning of projectiles.
Template Metaprogramming: Used extensively for things like dynamic type-tag templates (e.g., the SoA structure), custom allocators, wrappers, and compile-time-resolved generic behavior.
Data-Oriented Design: Building systems where content generation and behavior are driven by pre-built data rather than hard-coded logic.
System Architecture: Planned and designed robust architectures and public APIs for several major features.
Low-Level Systems Programming: Built systems that expose higher-level APIs on top of low-level features like static arrays, type reinterpretation, bit-packing, bit-flags, and bitwise logic.
Gameplay Programming
Gameplay Programming: Implemented core player mechanics - shooting, climbing, interacting with the world, etc.
Player Mechanics: Implemented player control and abilities that tie into broader gameplay systems.
Combat Systems: Built ranged and melee weapon systems with reactive hit impacts, advanced AI opponents, dismemberment effects, and traps.
AI Behavior: Created faction-based NPCs, each with unique strengths/weaknesses - melee-only enemies, long-range enemies that use cover and try to flank the player, etc.
Game Feel: Focused on how satisfying player interactions with the world, weapons, and enemies feel.
Animation Integration: Synced character/player animations with actions, and used animation events to trigger gameplay logic.
Physics Interaction: Let players interact physically with the world - doors on physics constraints, hanging lamps, grabbable boxes, heavy sliding doors.
Camera Systems: Built camera reactions to in-game events - heavy shakes, damage feedback, hit reactions, disorientation, and other screen effects.
World Interaction: Made the world feel alive and reactive - e.g., malfunctioning/swinging lights reacting to shockwaves, destructible elements.
3C Programming (Character, Camera, Controls): Gave the player a sense of physical weight while still feeling fast and agile, with realistic movement control and camera feedback.
Input Systems: Managed player input so behavior adapts to context (e.g., different controls while walking vs. using a computer vs. being grabbed).
Other Engines & Languages
Unity: Used during a specialization course; built a turn-based, top-down medieval war game as a class project, plus several smaller solo projects during an internship.
C#: Used together with Unity.
Node.js: Learned during higher vocational training; built two websites during the course - a restaurant site with login and a reservation database, and a final project for a game-company-style website with a database for users, games, in-game data, and wishlists.
React: Used for the second website mentioned above, to generate content dynamically from data.
MySQL: Taught in school and used heavily on the websites mentioned above.
MongoDB: Used within the final "game company" website project.
JavaScript: Used on both the Node.js backend and frontend - handling user actions, data validation, and content fetching.
Python: Used both personally and for external tools (a plugin compiler, an online downloader, etc.) - listed twice in the original data, reflecting its use in multiple contexts.
Java: Taught in the first year of web development studies; worked with serialization, object-oriented design, interfaces, and error handling.
Soft Skills / Work Style
Independent: Comfortable working alone - finding and solving problems independently, while still reporting progress when needed.
Strong Self-Learner: Learned more independently than in formal classes; adapts well to new tools and topics.
Calm and Patient: Even-tempered ("sin sangre" - literally "without blood/hot temper" in Spanish, meaning very calm) - the point here is being deliberate and non-impulsive rather than passive.
Visual/Artistic Skills
Particle Effects: Created close to 100 visual effects using Niagara in Unreal (not texture creation - using existing textures), including candle fire, explosions, lightning, smoke, volumetric effects, trails, and portals.
Material Effects: Created everything from realistic surface materials to visual/post-process effects in Unreal, including master materials that ~99% of other materials derive from.
Animal Care Skills (relevant for non-programming roles)
Dog Physical Care: Feeding, watering, and medicating dogs at a shelter.
Dog Mental/Behavioral Care: Knowing each dog individually - their preferences, dislikes, social compatibility with other dogs, and preferred play styles - to treat them appropriately.
Dog Training: Helping dogs better understand and communicate with humans, and showing them that some humans can be trusted and loving.
Cleaning & Disinfection: Cleaning waste from cages and yards; disinfecting himself and tools after handling sick dogs.
Creative Writing
Storytelling: Has written many short stories, and is currently working on a novel.

GENERAL KNOWLEDGE (concepts understood but not necessarily hands-on experience with)

Lock/Mutex mechanisms
Data race conditions
CPU cache lines
Memory containers: arrays, linked lists, hash sets, hash maps, queues, deques, circular arrays, stacks
GUIDs (Globally Unique Identifiers)
Frontend development (general)
Backend development (general)
Databases (general)
REST APIs
Server-side vs. client-side rendering
Low-level programming (e.g., C language)
