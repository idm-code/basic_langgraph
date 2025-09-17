# === LangGraph: memoria + condicionales ===
# Este ejemplo muestra cómo combinar memoria (historial de conversación)
# y branching condicional en un grafo con LangGraph.
# Es ideal para tutoriales y aprendizaje.

from langgraph.graph import StateGraph, END  # Importamos las clases principales de LangGraph

# Definimos el estado compartido como un diccionario
class Estado(dict):
    """Estado que guarda historial de interacciones"""
    def __init__(self):
        super().__init__()
        self["historial"] = []
        self["ultimo_input"] = None
        self["ruta"] = None

# --- Nodo de decisión y memoria ---
def nodo_llm(state):
    """
    Nodo que añade el input al historial y decide la ruta según el input.
    """
    pregunta = state.get("ultimo_input", "")  # Recupera el input del usuario
    state.setdefault("historial", [])  # Asegura que 'historial' existe
    state["historial"].append({"rol": "usuario", "contenido": pregunta})  # Guarda el input en el historial
    # Analiza el input y decide la ruta
    if "precio" in pregunta.lower():
        respuesta = "🤖 El agente detecta que preguntas por precios. Te redirige a la ruta de 'consultas financieras'."
        state["ruta"] = "finanzas"
    elif "clima" in pregunta.lower():
        respuesta = "🤖 El agente detecta que preguntas por el clima. Te redirige a la ruta de 'consultas meteorológicas'."
        state["ruta"] = "clima"
    else:
        respuesta = "🤖 El agente no entiende bien la intención. Te responde de forma genérica."
        state["ruta"] = "general"
    print(respuesta)  # Muestra la decisión tomada
    return state  # Devuelve el estado actualizado

# --- Nodo de finanzas ---
def nodo_finanzas(state: Estado):
    # Responde si la ruta es 'finanzas'
    respuesta = "📈 Respuesta del módulo de finanzas: el precio de BTC está en 42k (ejemplo)."
    print(respuesta)
    state.setdefault("historial", [])
    state["historial"].append({"rol": "agente", "contenido": respuesta})  # Añade la respuesta al historial
    return state

# --- Nodo de clima ---
def nodo_clima(state: Estado):
    # Responde si la ruta es 'clima'
    respuesta = "🌦️ Respuesta del módulo de clima: hoy está soleado con 25°C (ejemplo)."
    print(respuesta)
    state.setdefault("historial", [])
    state["historial"].append({"rol": "agente", "contenido": respuesta})  # Añade la respuesta al historial
    return state

# --- Nodo general ---
def nodo_general(state: Estado):
    # Responde si la ruta es 'general'
    respuesta = "💬 Respuesta general: gracias por tu pregunta."
    print(respuesta)
    state.setdefault("historial", [])
    state["historial"].append({"rol": "agente", "contenido": respuesta})  # Añade la respuesta al historial
    return state

def nodo_memoria(state: Estado):
    print("\n📜 Historial de conversación:")
    for i, h in enumerate(state["historial"], 1):
        print(f"{i}. {h['rol']}: {h['contenido']}")
    return state

# --- Construcción del grafo ---
workflow = StateGraph(Estado)  # Creamos el grafo de estado
workflow.add_node("llm", nodo_llm)         # Nodo de decisión y memoria
workflow.add_node("finanzas", nodo_finanzas)  # Nodo de finanzas
workflow.add_node("clima", nodo_clima)        # Nodo de clima
workflow.add_node("general", nodo_general)    # Nodo general
workflow.set_entry_point("llm")  # El grafo empieza en el nodo de decisión
workflow.add_conditional_edges(
    "llm",  # Nodo desde el que se ramifica
    lambda state: state["ruta"],  # Función que decide la ruta según el estado
    {
        "finanzas": "finanzas",  # Si ruta es 'finanzas', va al nodo_finanzas
        "clima": "clima",        # Si ruta es 'clima', va al nodo_clima
        "general": "general",    # Si ruta es 'general', va al nodo_general
    },
)
workflow.add_edge("finanzas", END)  # Todas las ramas terminan en END
workflow.add_edge("clima", END)
workflow.add_edge("general", END)
grafo = workflow.compile()  # Compilamos el grafo para poder ejecutarlo

# --- Ejecución del grafo ---
print("=== LangGraph: memoria + condicionales ===")
# Pedimos input al usuario antes de ejecutar el grafo
user_input = input("👤 Usuario: ")  # El usuario escribe su pregunta
# Creamos el estado inicial con el input y el historial vacío
estado = Estado()
estado["ultimo_input"] = user_input
estado["historial"] = []
# Ejecutamos el grafo: él decide la ruta, responde y guarda todo en el historial
grafo.invoke(estado)
