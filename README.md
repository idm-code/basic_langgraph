# LangGraph Tutorial - Ejemplos Básicos

Este proyecto contiene tutoriales introductorios para crear grafos con LangGraph, una biblioteca para construir aplicaciones con estado usando grafos dirigidos.

## 📋 Descripción

Incluye dos ejemplos principales:

- [`01_langgraph_primer_grafo.py`](01_langgraph_primer_grafo.py): Grafo básico de dos nodos que demuestra los conceptos fundamentales de LangGraph.
- [`02_langgraph_memoria_conversacional.py`](02_langgraph_memoria_conversacional.py): Grafo con memoria conversacional que simula un chat interactivo con historial.

---

## 1️⃣ Primer Grafo

### Estructura

```
[Nodo A] → [Nodo B] → [END]
```

- **Nodo A**: Genera un mensaje inicial y lo almacena en el estado.
- **Nodo B**: Procesa el mensaje del Nodo A y genera una respuesta.
- **END**: Termina la ejecución del grafo.

### Ejecución

```bash
python 01_langgraph_primer_grafo.py
```

#### Salida esperada

```
=== Ejecutando el grafo ===
🟢 Nodo A ejecutado
🔵 Nodo B ejecutado
📌 Estado final: {'mensaje': 'Hola desde el nodo A', 'respuesta': 'Hola desde el nodo A → Procesado en nodo B'}
```

---

## 2️⃣ Memoria Conversacional

### Estructura

```
[input] ⟶ [llm]
   ↑         |
   └─────────┘
```

- **input**: Recibe el mensaje del usuario y lo añade al historial.
- **llm**: Simula la respuesta de un modelo LLM y la añade al historial.
- El flujo es cíclico hasta que el usuario escribe `exit`.

### Ejecución

```bash
python 02_langgraph_memoria_conversacional.py
```

#### Salida esperada

```
=== Chat con memoria (LangGraph) ===
(Escribe 'exit' para salir)
👤 Usuario: hola
🤖 LLM responde a: 'hola' teniendo en cuenta el historial (1 turnos).
👤 Usuario: ¿cómo estás?
🤖 LLM responde a: '¿cómo estás?' teniendo en cuenta el historial (3 turnos).
...
👤 Usuario: exit
👋 Conversación finalizada.
📌 Historial final: [...]
```

---

## 🔧 Instalación

Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

El archivo [`requirements.txt`](requirements.txt) contiene:

```
langgraph
```

Si usas tipado fuerte en Python <3.8, instala también `typing-extensions`:

```bash
pip install typing-extensions
```

---

## 📚 Conceptos Clave

- **Estado compartido**: Uso de `TypedDict` o `dict` para definir el estado que fluye entre nodos.
- **Nodos**: Funciones que reciben y modifican el estado.
- **Flujo**: Definición de la secuencia de ejecución entre nodos, incluyendo ciclos para conversación.

---

## 🔗 Recursos

- [Documentación oficial de LangGraph](https://python.langchain.com/docs/langgraph)
- [Repositorio de LangGraph](https://github.com/langchain-ai/langgraph)

---

## 📝 Licencia

Este proyecto es de uso educativo y se distribuye bajo licencia MIT.