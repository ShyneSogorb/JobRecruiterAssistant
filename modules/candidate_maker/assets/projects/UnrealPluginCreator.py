def load():
  return """
{
  "project": {
    "name": "Advanced Weapon System (WAS)",
    "description": "An Unreal Engine plugin providing a modular weapon assembly system built around a custom reflection-based visual node graph (similar in spirit to Unreal's Material Editor), split into a WASRuntime module and a WASEditor module. Designers assemble weapons from a node graph that reads and writes arbitrary UFunction/FProperty members via reflection, while a GameplayTag-driven modification-slot system drives which meshes, materials, and components get built. The runtime module also implements full weapon mechanics (trigger modes, ammo/magazine handling, jamming, reloading), and the editor module provides a dedicated graph editor, a live 3D preview viewport, and custom detail-panel UI for editing tag-based modifications and project-wide ammo type settings.",
    "achievements": [
      {
        "context": "Building a weapon-assembly tool meant exposing arbitrary gameplay properties and functions to a visual graph without hand-writing a node class for every possible property or function.",
        "action": "Built a reflection-based node system (UWeaponPropertyRuntimeNode, UWeaponCustomFunctionRuntimeNode, UWeaponObjectFunctionNode) that reads FProperty/UFunction metadata at runtime to get/set arbitrary numeric, object, struct, and array properties and to invoke arbitrary UFUNCTIONs, including dynamically-typed object-bound function calls.",
        "impact": "Any BlueprintCallable function or exposed property on the weapon's Characteristics class (or on an object flowing through the graph) automatically becomes usable as a graph node, without additional per-property/per-function C++ node code.",
        "metric": null,
        "keywords": []
      },
      {
        "context": "Changing a property through the graph needed to notify other systems listening for that property's change (e.g. UI or gameplay code bound to delegates), without manually wiring each node to call the right delegate.",
        "action": "Implemented an automatic delegate-broadcast convention where a property named X pairs with a delegate named On{X}Changed, resolved via reflection, and only broadcasts when the new value actually differs from the previous one.",
        "impact": "Property-modifying nodes transparently notify existing gameplay delegates without any manual node-to-delegate wiring, and avoid redundant broadcasts when values are unchanged.",
        "metric": null,
        "keywords": []
      },
      {
        "context": "Graph execution needed a way to abort cleanly mid-execution (e.g. on invalid data) from deep inside nested node calls without unwinding C++ exceptions, while still releasing any temporary stack-allocated resources.",
        "action": "Implemented a setjmp/longjmp-based abort mechanism for graph execution paired with a custom FDestructionStack that manually registers and flushes destructors for stack-allocated temporaries, ensuring cleanup runs even when execution is aborted mid-way.",
        "impact": "Nodes can abort the whole graph run from any depth with a formatted error reason while guaranteeing temporary objects created during execution are still destructed.",
        "metric": null,
        "keywords": []
      },
      {
        "context": "The original weapon-modification system used per-project enums and a UPrimaryDataAsset (UWeaponArchitecture/FModificationArchitecture) to define modification slots, which was rigid and is now marked deprecated throughout the codebase.",
        "action": "Replaced the enum/data-asset modification architecture with a GameplayTag-hierarchy-based system (FWeaponModifications) where weapon, slot, and modification are represented as parent/child tags, with slot lookup done via tag-children queries.",
        "impact": "Modification slots and options are now defined and extended through the project's GameplayTag hierarchy instead of enums and dedicated data assets, and the corresponding editor UI (property customizations) auto-syncs to the live tag tree.",
        "metric": null,
        "keywords": []
      },
      {
        "context": "UWeaponComponent needed to support both a simple ammo counter and more advanced setups (external ammo pools, belt-fed weapons, magazines) without duplicating logic for each case.",
        "action": "Implemented a custom type-erased integer pointer (FIntegerPtr) that can either own an inline integer value or point to an external variable of unknown size/signedness (including Blueprint variables and map values via custom thunk functions SetAmmoSource/SetAmmoSourceFromMap), with generic arithmetic and comparison operators dispatched at runtime by size and signedness.",
        "impact": "The weapon component can bind its ammo source to any integer-like Blueprint variable (int8/16/32/64, byte, or a map entry) at runtime, letting ammo be tracked directly on an arbitrary external counter instead of only an internal field.",
        "metric": null,
        "keywords": []
      },
      {
        "context": "Weapon firing needed to support single, burst, and fully-automatic trigger modes plus ammo consumption, jamming, and reload logic all interacting correctly (e.g. burst count resetting, cooldown timers, ammo-insufficient failure).",
        "action": "Implemented UWeaponComponent's trigger/reload/jam state machine covering trigger-mode-specific repeat logic, ammo sufficiency checks (including 'trigger if ammo less than required'), magazine-vs-source ammo resolution, probabilistic jamming, and magazine-swap vs iterative reload strategies.",
        "impact": "A single component handles the full range of configurable firing behaviors (single/burst/auto, magazine reload styles, jam probability) driven by overridable Characteristics values, exposed as Blueprint events for each state transition (trigger, cooldown, reload, jam, unjam).",
        "metric": null,
        "keywords": []
      },
      {
        "context": "The editor needed a way to let designers add graph nodes for arbitrary gameplay properties/functions without maintaining a manual list of them per weapon class.",
        "action": "Implemented UWeaponGraphSchema::GetGraphContextActions to reflect over the weapon's Characteristics class (its properties and BlueprintCallable functions) and, when dragging from an object-typed pin, over that object's own class functions, generating context-menu 'add node' actions dynamically.",
        "impact": "The graph's right-click 'add node' menu automatically reflects whatever properties and callable functions exist on the weapon's characteristics class or on any connected object type, without hardcoding per-class node lists.",
        "metric": null,
        "keywords": []
      },
      {
        "context": "The custom graph editor needed full parity with Unreal's built-in graph editors for node manipulation (copy/paste across the OS clipboard, duplication, comment boxes) plus bidirectional sync between the editor-only graph representation and the runtime graph asset.",
        "action": "Implemented FWeaponAssetEditorApp's node copy/paste (via FEdGraphUtilities and the system clipboard), node duplication with pin/connection remapping, comment-node creation, and the SaveGraphToAsset/LoadAssetToGraph pair that converts between UEdGraphNode-based editor nodes and UWeaponRuntimeNode-based runtime nodes (including comments and pin connections) using GUID-keyed pin maps.",
        "impact": "The weapon graph supports standard graph-editor workflows (copy, paste, duplicate, comment) and persists that graph faithfully into the runtime asset used at gameplay time.",
        "metric": null,
        "keywords": []
      },
      {
        "context": "Designers needed to preview the assembled weapon in 3D while editing its graph and modification settings, similar to how Unreal's Material or Persona editors provide live previews.",
        "action": "Built a dedicated preview scene and viewport (FWeaponPreviewScene, SWeaponPreviewViewport, FWeaponViewportClient) with its own lit sky sphere, directional light, and isolated preview world, wired to rebuild the previewed weapon's components whenever the graph or its properties change.",
        "impact": "Changes to the weapon graph or its characteristics are reflected immediately in a live, lit 3D preview inside the custom asset editor.",
        "metric": null,
        "keywords": []
      },
      {
        "context": "Editing tag-based weapon modification data (names, descriptions, per-slot options) directly as raw arrays/maps in the details panel would be error-prone and wouldn't stay in sync with the project's GameplayTag hierarchy as it changes.",
        "action": "Implemented several IPropertyTypeCustomization/IDetailCustomization classes (FWeaponModificationDescriptionCustomization, FWeaponModificationsAppliedCustomization, FSelectByModCustomization, FWeaponModificatorCustomization) that auto-add/remove array or map entries to match the live GameplayTag children of a root tag, and render nested detail-panel groups and combo-box slot selectors reflecting that tag tree.",
        "impact": "The modification-description and modification-selection UI in the details panel always mirrors the current GameplayTag hierarchy, automatically fixing up stale or missing entries and presenting them in a nested, readable group layout instead of raw map editing.",
        "metric": "Supports up to 254 ammo type slots (256 minus 2 reserved values) and up to 62 nameable custom ammo types via UWeaponSystemSettings.",
        "keywords": []
      }
    ],
    "technologies": [
      { "name": "C++", "abbreviation": null, "category": "Languages" },
      { "name": "Unreal Engine", "abbreviation": "UE", "category": "Engines" },
      { "name": "Unreal Engine Reflection System", "abbreviation": null, "category": "Engines" },
      { "name": "GameplayTags", "abbreviation": null, "category": "Modules" },
      { "name": "Slate", "abbreviation": null, "category": "UI Framework" },
      { "name": "UMG", "abbreviation": null, "category": "UI Framework" },
      { "name": "Niagara", "abbreviation": null, "category": "Engines" },
      { "name": "Blueprint Graph", "abbreviation": null, "category": "Modules" },
      { "name": "Kismet Compiler", "abbreviation": null, "category": "Modules" },
      { "name": "GraphEditor", "abbreviation": null, "category": "Modules" },
      { "name": "AssetTools", "abbreviation": null, "category": "Modules" },
      { "name": "UnrealEd", "abbreviation": null, "category": "Modules" },
      { "name": "PropertyEditor", "abbreviation": null, "category": "Modules" },
      { "name": "StructUtils", "abbreviation": null, "category": "Modules" },
      { "name": "Developer Settings", "abbreviation": null, "category": "Modules" },
      { "name": "Python", "abbreviation": null, "category": "Build Tooling" },
      { "name": "Unreal Build Tool", "abbreviation": "UBT", "category": "Build Tooling" }
    ],
    "date": null
  },
  "details": {
    "skills": [
      { "name": "C++ template metaprogramming", "abbreviation": null, "category": null },
      { "name": "Unreal Engine reflection system (UProperty/UFunction introspection)", "abbreviation": null, "category": null },
      { "name": "Custom Slate widget development", "abbreviation": null, "category": null },
      { "name": "Unreal Engine editor extension (IDetailCustomization / IPropertyTypeCustomization)", "abbreviation": null, "category": null },
      { "name": "Custom EdGraph/EdGraphSchema node editors", "abbreviation": null, "category": null },
      { "name": "GameplayTag-driven data modeling", "abbreviation": null, "category": null },
      { "name": "Blueprint custom thunk functions", "abbreviation": null, "category": null },
      { "name": "Low-level memory management and type erasure in C++", "abbreviation": null, "category": null },
      { "name": "setjmp/longjmp-based control flow", "abbreviation": null, "category": null },
      { "name": "Unreal Engine module and plugin architecture", "abbreviation": null, "category": null },
      { "name": "3D preview scene and viewport implementation", "abbreviation": null, "category": null },
      { "name": "Serialization between editor and runtime data representations", "abbreviation": null, "category": null }
    ],
    "soft_skills": [
      { "name": "Iterative, self-directed engineering (visible through repeated refactors and deprecation of the enum-based modification system in favor of GameplayTags)", "abbreviation": null, "category": null },
      { "name": "Attention to backward compatibility (engine-version conditional code paths, e.g. ENGINE_MINOR_VERSION checks)", "abbreviation": null, "category": null },
      { "name": "Documentation habit (extensive Doxygen-style comments across headers)", "abbreviation": null, "category": null }
    ],
    "transferable_skills": [
      { "name": "Designing extensible plugin architectures for content-creation tools", "abbreviation": null, "category": null },
      { "name": "Building visual/node-based scripting systems", "abbreviation": null, "category": null },
      { "name": "Reflection-driven UI generation from live data models", "abbreviation": null, "category": null },
      { "name": "State-machine design for real-time interactive systems (weapon firing/reload/jam logic)", "abbreviation": null, "category": null }
    ]
  }
}
"""
