# Importamos las clases necesarias de LangGraph
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict

# Definimos el "estado" que compartirá el grafo usando TypedDict
# TypedDict permite a LangGraph conocer exactamente qué campos pueden existir
class Estado(TypedDict):
    mensaje: str      # Campo para almacenar el mensaje del nodo A
    respuesta: str    # Campo para almacenar la respuesta procesada del nodo B

# --- Definición de nodos ---
# Los nodos son funciones que reciben el estado y lo modifican

def nodo_a(state: Estado):
    """
    Primer nodo del grafo: genera un mensaje inicial
    - Recibe el estado actual como parámetro
    - Modifica el campo 'mensaje' del estado
    - Retorna el estado modificado
    """
    print("🟢 Nodo A ejecutado")
    state["mensaje"] = "Hola desde el nodo A"  # Asigna valor al campo 'mensaje'
    return state  # Retorna el estado para que pase al siguiente nodo

def nodo_b(state: Estado):
    """
    Segundo nodo del grafo: procesa el mensaje del nodo A
    - Recibe el estado que fue modificado por el nodo A
    - Lee el campo 'mensaje' creado por el nodo A
    - Crea un nuevo campo 'respuesta' con el mensaje procesado
    """
    print("🔵 Nodo B ejecutado")
    # Usar get() para evitar KeyError si 'mensaje' no existe (buena práctica)
    mensaje = state.get("mensaje", "")
    state["respuesta"] = f"{mensaje} → Procesado en nodo B"  # Procesa el mensaje
    return state  # Retorna el estado final con ambos campos

# --- Construcción del grafo ---
# Creamos un grafo de estado usando la clase Estado definida anteriormente
workflow = StateGraph(Estado)

# Agregamos los nodos al grafo
# Cada nodo se identifica con un nombre único ("A", "B")
workflow.add_node("A", nodo_a)  # Agrega nodo_a con identificador "A"
workflow.add_node("B", nodo_b)  # Agrega nodo_b con identificador "B"

# Definimos el flujo del grafo
workflow.set_entry_point("A")    # El grafo comenzará ejecutando el nodo "A"
workflow.add_edge("A", "B")      # Después del nodo "A", ejecutar el nodo "B"
workflow.add_edge("B", END)      # Después del nodo "B", terminar el grafo

# --- Compilación y ejecución ---
# Compilamos el workflow para crear un grafo ejecutable
grafo = workflow.compile()

print("=== Ejecutando el grafo ===")
# Ejecutamos el grafo con un estado inicial vacío
# El estado se va pasando y modificando entre nodos
final_state = grafo.invoke(Estado())
print("📌 Estado final:", final_state)
