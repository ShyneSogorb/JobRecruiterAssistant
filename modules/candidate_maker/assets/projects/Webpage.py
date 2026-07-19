import os

DATA = """Personal Webpage
(No further details provided in the original data - this is the portfolio site linked above.)
"""

def scan_dir(p) -> list[str]:
    entries = list[str]()

    with os.scandir(p) as ents:
        for e in ents:
            if e.is_dir():
                entries += scan_dir(e.path)
            else:
                entries.append(e.path)

    return entries



def load():

    rootPath = "C:\\Users\\user\\Documents\\WebPortfolio\\"
    path = "C:\\Users\\user\\Documents\\WebPortfolio\\webpage"

    list = scan_dir(os.path.join(path, "src"))

    all = dict[str, str]()

    for i in list:
        with open(i) as f:
            try:
                all[i[len(rootPath):]] = f.read()
            except UnicodeDecodeError as e:
                raise UnicodeDecodeError(e.encoding, e.object, e.start, e.end, e.reason + " At file: " + i)





    return """
{
  "project": {
    "name": "Advanced Combat System",
    "description": "A free Unreal Engine plugin that enables the creation of complex weapons, damage events, armor systems, realistic bullets, optimized bullet spawning, visual effects, and related gameplay functionality through reusable modules exposed to Blueprints and implemented in C++.",
    "achievements": [
      {
        "context": "Provide a reusable combat framework for Unreal Engine that simplifies the creation of combat mechanics.",
        "action": "Developed a free Unreal Engine plugin with modular support for weapons, health, armor, effects, and core combat systems.",
        "impact": "Allows users to build complex combat systems more easily through a modular architecture.",
        "metric": null,
        "keywords": [
          
        ]
      },
      {
        "context": "Weapon creation should require minimal programming effort.",
        "action": "Implemented a weapon framework with a base weapon class and specialized melee and firearm subclasses, supporting Blueprint-based customization.",
        "impact": "New weapons can be created with simple Blueprint programming or without programming when using the demo bullets.",
        "metric": null,
        "keywords": [
          
        ]
      },
      {
        "context": "Projectile systems require both realism and performance.",
        "action": "Implemented a bullet pool system for low-latency projectile spawning together with detailed bullet simulation supporting ricochet and surface-based penetration.",
        "impact": "Provides optimized projectile generation while supporting realistic bullet behavior.",
        "metric": null,
        "keywords": [
          
        ]
      },
      {
        "context": "Gameplay effects should be easy to configure and adaptable.",
        "action": "Implemented an effect system with an integrated randomizer and built-in configuration settings.",
        "impact": "Effects can be adapted to different user requirements with minimal effort.",
        "metric": null,
        "keywords": [
          
        ]
      },
      {
        "context": "Performance and usability are both important for gameplay systems.",
        "action": "Implemented the plugin in C++ and exposed its functionality to Blueprints.",
        "impact": "Combines native performance with Blueprint accessibility.",
        "metric": null,
        "keywords": [
          
        ]
      }
    ],
    "technologies": [
      {
        "name": "Unreal Engine",
        "abbreviation": null,
        "category": null
      },
      {
        "name": "C++",
        "abbreviation": null,
        "category": null
      },
      {
        "name": "Blueprints",
        "abbreviation": null,
        "category": null
      }
    ],
    "date": null
  },
  "details": {
    "skills": [
      {
        "name": "Unreal Engine"
      },
      {
        "name": "C++"
      },
      {
        "name": "Blueprints"
      },
      {
        "name": "Plugin Development"
      },
      {
        "name": "Gameplay Programming"
      },
      {
        "name": "Weapon Systems"
      },
      {
        "name": "Health Systems"
      },
      {
        "name": "Armor Systems"
      },
      {
        "name": "Object Pooling"
      },
      {
        "name": "Bullet Simulation"
      },
      {
        "name": "Visual Effects Systems"
      },
      {
        "name": "Modular Architecture"
      }
    ],
    "soft_skills": [
      
    ],
    "transferable_skills": [
      {
        "name": "Modular System Design"
      },
      {
        "name": "Performance Optimization"
      },
      {
        "name": "API Design"
      },
      {
        "name": "Reusable Software Development"
      },
      {
        "name": "System Architecture"
      }
    ]
  }
}
"""
