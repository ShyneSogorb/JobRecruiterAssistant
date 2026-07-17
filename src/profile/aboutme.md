PERSONAL INFORMATION
Name: Kingsley Shyne Mattis Sogorb
Email: shyne2003@gmail.com
Location: Villena, Valencian Community, Spain
Personal Webpage: https://shynesogorb.github.io/webpage/
Phone: +34 664 16 10 72
LinkedIn: https://linkedin.com/in/kingsley-shyne-mattis-sogorb-a4a898214
GitHub: https://github.com/ShyneSogorb

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


PROJECTS (personal, non-commercial work - useful to show initiative/skills, can be omitted if experience section already covers similar ground)
1. Chimera Engine
A custom C++ game engine built from scratch using CMake, aiming for modularity.

Built as a desktop application in C++
Used Vulkan as the rendering API
Designed with interface-based abstraction so modules could be developed independently
Worked directly with low-level C APIs
Used CMake to manage the build system
Used a linker to connect modules together
Implemented SDL2 for window management
Used HLSL as the shader language

2. YouTube Downloader
A tool to download YouTube videos.

Downloads any public video via link
Downloads all public videos from a public playlist

3. Audio Extractor
A Python tool to extract audio from video.

Converts MP4 video into MP3 audio
Works on a single file or an entire folder of videos
Uses multithreading to process files much faster

4. Audio Format Converter
A Python script to convert between audio formats.

Converts MP3 to WAV and vice versa
Works on a single file or an entire folder
Uses multithreading for faster processing

5. Image Downscaler
A Python tool that resizes/downscales images to a specified target size.
6. Plugin Compilation Tester
(No further details provided in the original data.)
7. Personal Webpage
(No further details provided in the original data - this is the portfolio site linked above.)
8. CV Maker
(No further details provided in the original data - likely the tool used to help generate structured CVs like this one.)

1. Dog Caretaker and Trainer
Dates: 2024 - Present
Responsibilities (these are described as day-to-day duties rather than standout achievements, but are listed for completeness):

Feeding dogs and providing clean water
Cleaning waste from cages and outdoor yards
Administering medication - pills, injections, wound cleaning, and creams - as prescribed
Monitoring dog behavior to prevent fights and separating dogs when conflicts arise
Transporting dogs to veterinary clinics
Greeting visitors, volunteers, and prospective adopters
Supporting the physical and mental well-being of the dogs as much as possible

2. Plugin Developer (Unreal Engine) - Solo Work
Dates: 2024 – Present
Company: Independent/Solo
Key achievements:

Built a data-driven UMG (Unreal UI) interface for customizing modular weapons - a data asset stores all weapon info (name, slots, modifiers per slot), with a live runtime preview and hover-based context info
Created a dropdown UI system that auto-generates as many dropdowns as a weapon has slots, populated with that slot's available modifiers
Designed and built custom Unreal Editor tooling for data-driven content creation and modular asset configuration
Built reflection-based systems and custom "details panels" so designers/artists could work with complex data more easily
Created a clean separation between editor-only and runtime data, keeping tools flexible in-editor while minimizing overhead in the final shipped game
Built workflow-focused UI and preview tools to speed up iteration and cut down manual setup
Designed a modular weapon system using node-based logic with lazy evaluation for efficient execution
Built data-driven systems that are flexible and reusable across different gameplay situations
Optimized memory usage and performance in shipping builds by separating editor and runtime data
Used reflection combined with delegate-driven updates to keep the system extensible and loosely coupled
Built reusable components that adapt to multiple gameplay contexts
Built a modular weapon system supporting multiple weapon types, attachments, and behaviors
Implemented node-based logic controlling weapon behavior for flexible configuration and fast iteration
Designed gameplay systems where designers can tweak parameters live, without needing code changes
Integrated UI for real-time weapon configuration and preview

3. Systems and Mechanics Programmer - Avtrix Games (Unreal Engine)
Dates: 2019 – 2024
Company: Avtrix Games (Indie studio; unpaid, worked alongside one designer)
Key achievements:

Built UMG-based UI elements: pause menus, death screens, options menus
Connected UI feedback to gameplay systems so it reflects real player state
Exposed gameplay data to UI systems for real-time updates based on interactions
Worked with designers to structure gameplay data in ways that made UI implementation easier
Improved UI usability through better parameter exposure and clearer interactions
Implemented a broad range of gameplay and editor-facing systems: modular interaction, weapon configuration, character-environment workflows
Built data-driven content pipelines that let non-programmers tune gameplay parameters directly
Automated repetitive production tasks using Python (e.g., batch texture resizing and filtering)
Built custom visual effects (FX) and materials, plus artist-facing tools to expose parameters
Designed modular technical systems to improve maintainability, reusability, and scalability in content-heavy features
Built core gameplay systems: AI behaviors, faction logic, interaction systems, modular combat frameworks
Implemented a high-performance ballistics (bullet/projectile) system using data-oriented design (Structure of Arrays), static object pooling, and batch processing
Designed systems that support SIMD execution and multithreading to handle heavy performance loads
Built explosion and melee systems with configurable precision, using asynchronous processing to reduce load on the main thread
Implemented modular damage systems supporting environmental effects and dynamic behavior changes
Applied optimization techniques: memory reuse, fewer allocations, cache-friendly data layouts
Built multiple AI behavior trees for different enemy types: melee enemies, ranged melee enemies, teleporting enemies, camouflaged enemies, flying drones, and jetpack-equipped enemies
Used Unreal's AI Perception system for sight, hearing, damage, and touch senses
Created Environment Query System (EQS) setups so enemies could seek cover and flank the player intelligently
Used blackboards within behavior trees and Blueprints

4. Gameplay Programmer Intern - Devilish Games (Unity)
Dates: 2023 (single year)
Company: Devilish Games (Indie studio)
Key achievements:

Built UI elements for gameplay prototypes, focused on player interaction and feedback
Developed simple, clear, and responsive UI systems for mobile gameplay
Built gameplay prototypes with custom movement and math-driven control systems for mobile projects
Implemented mechanics blending 3D/2D interaction, precision controls, and gravity-based racing concepts
Built systems for fast iteration to quickly validate mechanics and support early production decisions
Used mathematical models for precise control and behavior tuning
Developed custom gravity systems enabling dynamic multi-body interaction and traversal
Focused on building flexible systems for quick iteration and testing
Implemented parkour/traversal systems, including climbing and movement over complex geometry
Built combat systems with multiple weapon types, modifiers, and interaction behaviors
Built AI behaviors for varied enemy types: melee units, ranged soldiers, heavy units, drones, stealth units
Designed faction systems governing dynamic relationships between enemies, allies, and neutral characters
Built environmental interaction systems: doors, generators, cameras, switches, physics-based objects
Built damage systems including dismemberment, partial limb destruction, and behavior changes based on damage taken
Created environmental hazards: fire, radiation, acid, and physics-based traps

5. Game Prototype Programmer Intern - Devilish Games (Unity)
Dates: 2021 (single year)
Company: Devilish Games (Indie studio)
Key achievements:

Built experimental gameplay prototypes exploring movement, parkour, and interaction mechanics
Implemented prototype logic designed for rapid iteration and mechanics testing
Built prototypes with unique mechanics, including hybrid 2D/3D interaction systems
Implemented precision-based mobile control systems using mathematical models
Created a planetary racing prototype featuring custom gravity systems and multi-surface traversal


EDUCATION
Note: Spanish education system terms don't always have a direct international equivalent, but should still be represented. In most job applications, education is usually less important than professional experience, so achievements/events here can often be trimmed.
Specialization Course - Game Development and Virtual Reality
School: IES Poeta Paco Mollà
Highlights:

Built multiple game tests in Unity
Created a "Brick Breaker"-style game with power-ups and procedurally generated levels
Built a turn-based game with AI that intelligently chooses actions based on scored decision-making queries
Collaborated on a larger turn-based strategy game featuring different army unit types (archers, knights, spearmen, and shield-bearers)
Built tools for designers, reviewed code, fixed bugs, and suggested more efficient or reliable approaches to teammates

Higher National Diploma - Web Application Development
School: IES Hermanos Amorós
Highlights:

Built a local restaurant website with an online reservation system and capacity tracking, backed by a database for the menu
Built a local website for a fictional game company to showcase games, pulling from a database, linking out to Steam pages, supporting wishlists, and using MongoDB (No-SQL) for in-game world data
Designed and implemented several real-world database exercises - going from written requirements, to entity-relationship diagrams, to database setup, to writing queries

Intermediate Vocational Training Diploma - Microcomputer Systems and Networks
School: IES Hermanos Amorós
(No additional details provided.)

LANGUAGES
Spanish: Native
English: Fluent
Catalan/Valencian: Fluent
German: Basic
Polish: Basic


ADDITIONAL INFORMATION

Volunteer dog caretaker and trainer - reflects responsibility, patience, and teamwork
Experienced medieval swordsman - disciplined and focused
Writes fiction in his free time, with a focus on storytelling and world-building