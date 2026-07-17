import os

DATA = """
Chimera Engine
A custom C++ game engine built from scratch using CMake, aiming for modularity.

Built as a desktop application in C++
Used Vulkan as the rendering API
Designed with interface-based abstraction so modules could be developed independently
Worked directly with low-level C APIs
Used CMake to manage the build system
Used a linker to connect modules together
Implemented SDL2 for window management
Used HLSL as the shader language
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



# def load():

#     rootPath = "C:\\Users\\user\\Documents\\"
#     path = "C:\\Users\\user\\Documents\\ChimeraEngine"


#     list = (
#         scan_dir(os.path.join(path, "Game"))
#         + scan_dir(os.path.join(path, "Engine"))
#     )

#     all = dict[str, str]()

#     root = os.path.join(path, "CMakeLists.txt")
#     with open(root) as f:
#         all[root] = f.read()
    
#     for i in list:
#         with open(i) as f:
#             all[i[len(rootPath):]] = f.read()

#     return f"""
# {DATA}

# Project:

# { "\n".join(f"File: {k}\nCode:{all[k]}" for k in all)}

# """

def load():
    return """
{
  "name": "ChimeraEngine",
  "description": "Motor de renderizado 3D en C++23 con backend Vulkan, construido como una arquitectura modular basada en 'módulos' (ChimeraCore, VulkanRenderer, SdlWindow, GenericInput, CameraModule, VulkanProvider/VulkanSdlProvider) registrados en un Engine singleton (FEngine). Usa Vulkan moderno (dynamic rendering, sincronización con VkSemaphoreSubmitInfo2/VkCommandBufferSubmitInfo2), vk-bootstrap para inicialización de instancia/dispositivo, VMA (Vulkan Memory Allocator) para gestión de memoria GPU, y fastgltf + stb_image para cargar modelos glTF/GLB con texturas y generación de mipmaps. Incluye una librería de contenedores y matemáticas propia (TArray, TMap, TVector, TMatrix, TDeque, TOptional, etc., construida sobre EASTL) como alternativa/complemento a GLM, seleccionable en tiempo de compilación mediante la macro USE_GLM. Integra ImGui para overlays de depuración (estadísticas de frame, triángulos, draw calls) y un sistema de delegados multicast propio para el manejo de input y eventos de ventana vía SDL2.",
  "achievements": [
    {
      "action": "Diseño de una arquitectura de motor basada en módulos desacoplados mediante interfaces (IModuleInterface, IRenderModuleInterface, IInputHandleModuleInterface, IWindowModuleInterface, IVulkanProviderModuleInterface) registrados y resueltos en tiempo de ejecución a través de un FEngine singleton con búsqueda por dynamic_cast.",
      "context": "El main.cpp obtiene los módulos de renderizado e input desde FEngine::Get().GetModule<T>() en lugar de instanciarlos directamente, permitiendo intercambiar implementaciones (p. ej. VulkanSdlProvider) sin tocar el bucle principal.",
      "impact": "Permite añadir o sustituir subsistemas (input genérico, cámara, proveedor de superficie Vulkan, renderer) sin modificar el código que los consume.",
      "metric": null
    },
    {
      "action": "Implementación de un pipeline de renderizado Vulkan moderno usando dynamic rendering (vkCmdBeginRendering/vkCmdEndRendering) en vez de render passes clásicos, con doble buffering de frames (FRAME_OVERLAP = 2) y sincronización explícita mediante VkFence/VkSemaphore y submits Vulkan 1.3 (vkQueueSubmit2).",
      "context": "El motor requiere Vulkan 1.3 con las features dynamicRendering y synchronization2 activadas explícitamente al seleccionar el dispositivo físico.",
      "impact": "Elimina la necesidad de VkRenderPass/VkFramebuffer explícitos y reduce el boilerplate de sincronización manual.",
      "metric": null
    },
    {
      "action": "Sistema propio de asignación de descriptor sets (FDescriptorAllocator) con pools que crecen dinámicamente y se reciclan (ReadyPools/FullPools), más un FDescriptorWriter para batch-escribir bindings de buffers e imágenes.",
      "context": null,
      "impact": "Evita crear un VkDescriptorPool nuevo cada vez que se necesitan más sets, reutilizando pools llenos tras un reset.",
      "metric": {
        "value": "MaxSetsPerPool = 4092",
        "context_note": "límite superior configurado para el crecimiento de un pool de descriptores (constante en vk_descriptors.cpp)"
      }
    },
    {
      "action": "Carga de escenas glTF/GLB (incluyendo buffers embebidos y externos) usando fastgltf, con extracción de mallas, jerarquía de nodos (TRS y matrices), materiales PBR metálico-rugoso, y texturas (desde URI, buffer vector o bufferView/GLB embebido) decodificadas con stb_image, incluyendo generación automática de mipmaps en GPU.",
      "context": "Se soportan tres rutas distintas de origen de imagen dentro de un glTF (archivo externo, vector en memoria, bufferView de GLB) mediante std::visit sobre variantes de fastgltf::sources.",
      "impact": "Si una textura falla en cargar, el sistema no aborta la carga completa sino que sustituye por una textura de error tipo 'checkerboard', permitiendo depurar visualmente qué recurso falló.",
      "metric": null
    },
    {
      "action": "Implementación de frustum culling por caja delimitadora (AABB en espacio de clip) antes de la fase de dibujo, separando superficies opacas y transparentes en listas de índices visibles.",
      "context": "IsVisible() proyecta las 8 esquinas del bounding box de cada objeto al espacio de recorte usando la matriz ViewProjection y descarta objetos fuera del volumen de vista.",
      "impact": "Reduce el número de draw calls emitidos por frame al omitir geometría no visible, y el motor registra en tiempo real cuántos triángulos y draw calls se ejecutan por frame vía ImGui.",
      "metric": null
    },
    {
      "action": "Desarrollo de una librería de matemáticas y contenedores propia en C++23 (TVector, TMatrix, TArray, TMap, TDeque, TStack, TOptional, TFunction, delegados multicast) usando 'explicit object parameters' (deducing this) para reducir duplicación de código const/no-const, construida sobre EASTL en vez de STL.",
      "context": "El código incluye una capa de abstracción (USE_GLM macro) que permite alternar en tiempo de compilación entre GLM y la implementación matemática propia (Chimera::Types::Math), incluyendo comparación experimental de resultados de rotación entre ambas (visible en Camera.cpp con los métodos PrintOne/PrintAll).",
      "impact": null,
      "metric": null
    }
  ],
  "technologies": [
    { "name": "C++", "abbreviation": null, "category": "Languages" },
    { "name": "Vulkan", "abbreviation": null, "category": "Engines" },
    { "name": "CMake", "abbreviation": null, "category": "Tools" },
    { "name": "vcpkg", "abbreviation": null, "category": "Tools" },
    { "name": "SDL2", "abbreviation": null, "category": "Tools" },
    { "name": "OpenGL Mathematics", "abbreviation": "GLM", "category": "Libraries" },
    { "name": "vk-bootstrap", "abbreviation": null, "category": "Libraries" },
    { "name": "Vulkan Memory Allocator", "abbreviation": "VMA", "category": "Libraries" },
    { "name": "fastgltf", "abbreviation": null, "category": "Libraries" },
    { "name": "fmt", "abbreviation": null, "category": "Libraries" },
    { "name": "EA Standard Template Library", "abbreviation": "EASTL", "category": "Libraries" },
    { "name": "Dear ImGui", "abbreviation": "ImGui", "category": "Libraries" },
    { "name": "stb_image", "abbreviation": null, "category": "Libraries" },
    { "name": "GLSL", "abbreviation": null, "category": "Languages" },
    { "name": "glslangValidator", "abbreviation": null, "category": "Tools" },
    { "name": "SPIR-V", "abbreviation": null, "category": "Tools" }
  ],
  "date": null
}
"""