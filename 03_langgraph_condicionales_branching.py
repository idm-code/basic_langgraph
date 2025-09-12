# === Ejemplo de branching condicional con LangGraph ===
# Este script muestra cómo usar LangGraph para crear un grafo con rutas condicionales (branching)
# según el input del usuario. Es ideal para tutoriales y aprendizaje.

from langgraph.graph import StateGraph, END  # Importamos las clases principales de LangGraph

# Definimos el estado compartido como un diccionario (puede ser TypedDict en proyectos grandes)
class Estado(dict):
    pass  # Aquí se almacenarán los datos que pasan entre nodos

# --- Definición de nodos ---
# Nodo de decisión: analiza el input y decide la ruta

def nodo_llm(state: Estado):
    """
    Nodo que decide la ruta según el input del usuario.
    El input debe estar en state['ultimo_input'].
    """
    pregunta = state.get("ultimo_input", "")  # Recupera el input del usuario
    # Analiza el input y decide la ruta
    if "precio" in pregunta.lower():
        respuesta = "🤖 El agente detecta que preguntas por precios. Te redirige a la ruta de 'consultas financieras'."
        state["ruta"] = "finanzas"  # Marca la ruta a seguir
    elif "clima" in pregunta.lower():
        respuesta = "🤖 El agente detecta que preguntas por el clima. Te redirige a la ruta de 'consultas meteorológicas'."
        state["ruta"] = "clima"
    else:
        respuesta = "🤖 El agente no entiende bien la intención. Te responde de forma genérica."
        state["ruta"] = "general"
    print(respuesta)  # Muestra la decisión tomada
    return state  # Devuelve el estado actualizado

# Nodo de finanzas: responde si la ruta es 'finanzas'
def nodo_finanzas(state: Estado):
    print("📈 Respuesta del módulo de finanzas: el precio de BTC está en 42k (ejemplo).")
    return state

# Nodo de clima: responde si la ruta es 'clima'
def nodo_clima(state: Estado):
    print("🌦️ Respuesta del módulo de clima: hoy está soleado con 25°C (ejemplo).")
    return state

# Nodo general: responde si la ruta es 'general'
def nodo_general(state: Estado):
    print("💬 Respuesta general: gracias por tu pregunta.")
    return state

# --- Construcción del grafo ---
workflow = StateGraph(Estado)  # Creamos el grafo de estado

# Añadimos los nodos al grafo
workflow.add_node("llm", nodo_llm)         # Nodo de decisión
workflow.add_node("finanzas", nodo_finanzas)  # Nodo de finanzas
workflow.add_node("clima", nodo_clima)        # Nodo de clima
workflow.add_node("general", nodo_general)    # Nodo general

# Definimos el punto de entrada del grafo (primer nodo a ejecutar)
workflow.set_entry_point("llm")

# Añadimos las ramas condicionales: según el valor de state['ruta'], el grafo sigue una ruta
workflow.add_conditional_edges(
    "llm",  # Nodo desde el que se ramifica
    lambda state: state["ruta"],  # Función que decide la ruta según el estado
    {
        "finanzas": "finanzas",  # Si ruta es 'finanzas', va al nodo_finanzas
        "clima": "clima",        # Si ruta es 'clima', va al nodo_clima
        "general": "general",    # Si ruta es 'general', va al nodo_general
    },
)

# Todas las ramas terminan en END (fin del grafo)
workflow.add_edge("finanzas", END)
workflow.add_edge("clima", END)
workflow.add_edge("general", END)

# Compilamos el grafo para poder ejecutarlo
grafo = workflow.compile()

# --- Ejecución del grafo ---
print("=== Condicionales en LangGraph ===")
# Pedimos input al usuario antes de ejecutar el grafo
user_input = input("👤 Usuario: ")  # El usuario escribe su pregunta
# Creamos el estado inicial con el input del usuario
estado = Estado(ultimo_input=user_input)
# Ejecutamos el grafo: él decide la ruta y ejecuta el nodo correspondiente
grafo.invoke(estado)
