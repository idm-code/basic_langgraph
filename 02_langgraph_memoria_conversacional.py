from langgraph.graph import StateGraph, END

# Definimos el "estado" compartido como un diccionario
# Aquí podrías usar TypedDict para mayor robustez, pero para este ejemplo usamos dict
class Estado(dict):
    pass  # El estado guardará el historial de la conversación y el último input

# --- Nodos ---
# Nodo encargado de recibir el input del usuario y actualizar el historial
def nodo_input(state: Estado):
    user_input = input("👤 Usuario: ")  # Solicita entrada al usuario
    # Si no existe el historial, lo crea como lista vacía
    state.setdefault("historial", [])
    # Añade el mensaje del usuario al historial
    state["historial"].append({"role": "user", "content": user_input})
    # Guarda el último input para poder controlar la salida del bucle
    state["ultimo_input"] = user_input
    return state  # Devuelve el estado actualizado

# Nodo que simula la respuesta de un modelo LLM usando el historial
def nodo_llm(state: Estado):
    # Obtiene el historial de la conversación
    historial = state.get("historial", [])
    # Toma la última pregunta del usuario (si existe)
    ult_pregunta = historial[-1]["content"] if historial else ""
    # Genera una respuesta simulada usando la última pregunta y el tamaño del historial
    respuesta = f"🤖 LLM responde a: '{ult_pregunta}' teniendo en cuenta el historial ({len(historial)} turnos)."
    # Añade la respuesta del asistente al historial
    historial.append({"role": "assistant", "content": respuesta})
    state["historial"] = historial  # Actualiza el historial en el estado
    print(respuesta)  # Muestra la respuesta por pantalla
    return state  # Devuelve el estado actualizado

# --- Grafo ---
workflow = StateGraph(Estado)

workflow.add_node("input", nodo_input)
workflow.add_node("llm", nodo_llm)

workflow.set_entry_point("input")
workflow.add_edge("input", "llm")
workflow.add_edge("llm", "input")  # bucle para conversación
workflow.add_edge("input", END)    # permite salir si se corta

# Compilamos el grafo (aunque en este ejemplo ejecutamos los nodos manualmente)
grafo = workflow.compile()

# --- Ejecución principal del chat ---
print("=== Chat con memoria (LangGraph) ===")
# Inicializamos el estado con un historial vacío
estado = Estado(historial=[])
print("(Escribe 'exit' para salir)")
while True:
    # 1. Pedimos input al usuario y lo guardamos en el historial
    estado = nodo_input(estado)
    # 2. Si el usuario escribe 'exit', terminamos la conversación
    if estado.get("ultimo_input", "").strip().lower() == "exit":
        print("👋 Conversación finalizada.")
        break
    # 3. El "modelo" responde usando el historial actualizado
    estado = nodo_llm(estado)

print("📌 Historial final:", estado["historial"])
