# LangGraph Tutorial - Ejemplos Básicos

Este proyecto contiene tutoriales introductorios para crear grafos con LangGraph, una biblioteca para construir aplicaciones con estado usando grafos dirigidos.

## 📋 Descripción

Incluye seis ejemplos principales:

- [`01_langgraph_primer_grafo.py`](01_langgraph_primer_grafo.py): Grafo básico de dos nodos que demuestra los conceptos fundamentales de LangGraph.
- [`02_langgraph_memoria_conversacional.py`](02_langgraph_memoria_conversacional.py): Grafo con memoria conversacional que simula un chat interactivo con historial.
- [`03_langgraph_condicionales_branching.py`](03_langgraph_condicionales_branching.py): Grafo con branching condicional real gestionado por LangGraph.
- [`04_langgraph_memoria_condicionales.py`](04_langgraph_memoria_condicionales.py): Grafo que combina memoria (historial) y branching condicional.
- [`05_langgraph_memoria_largo_plazo.py`](05_langgraph_memoria_largo_plazo.py): Grafo con memoria persistente en SQLite y branching condicional.
- [`06_langgraph_memoria_hibrida.py`](06_langgraph_memoria_hibrida.py): Grafo con memoria híbrida (SQLite + FAISS) y búsqueda semántica.

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

## 3️⃣ Branching condicional (condiciones y rutas)

### Estructura

```
[llm] ──┬──> [finanzas] ──┐
        ├──> [clima]    ──┤→ [END]
        └──> [general]  ──┘
```

- **llm**: Nodo de decisión que analiza el input y decide la ruta.
- **finanzas/clima/general**: Nodos que responden según la ruta elegida.
- **END**: Fin del grafo.

### Ejecución

```bash
python 03_langgraph_condicionales_branching.py
```

#### Salida esperada

```
=== Condicionales en LangGraph ===
👤 Usuario: ¿Cuál es el precio del oro?
🤖 El agente detecta que preguntas por precios. Te redirige a la ruta de 'consultas financieras'.
📈 Respuesta del módulo de finanzas: el precio de BTC está en 42k (ejemplo).

👤 Usuario: ¿Cómo está el clima?
🤖 El agente detecta que preguntas por el clima. Te redirige a la ruta de 'consultas meteorológicas'.
🌦️ Respuesta del módulo de clima: hoy está soleado con 25°C (ejemplo).

👤 Usuario: John
🤖 El agente no entiende bien la intención. Te responde de forma genérica.
💬 Respuesta general: gracias por tu pregunta.
```

---

## 4️⃣ Memoria + Condicionales

### Estructura

```
[llm (memoria+decisión)] ──┬──> [finanzas] ──┐
                           ├──> [clima]    ──┤→ [END]
                           └──> [general]  ──┘
```

- **llm**: Nodo que añade el input al historial y decide la ruta.
- **finanzas/clima/general**: Nodos que responden según la ruta elegida y añaden la respuesta al historial.
- **END**: Fin del grafo.

### Ejecución

```bash
python 04_langgraph_memoria_condicionales.py
```

#### Salida esperada

```
=== LangGraph: memoria + condicionales ===
👤 Usuario: Mike
🤖 El agente no entiende bien la intención. Te responde de forma genérica.
💬 Respuesta general: gracias por tu pregunta.
```

El historial final contendrá tanto los mensajes del usuario como las respuestas del agente, demostrando cómo se puede mantener contexto y lógica condicional en un grafo.

---

## 5️⃣ Memoria persistente + Branching condicional (SQLite)

### Estructura

```
[llm (memoria+decisión+persistencia)] ──┬──> [finanzas] ──┐
                                        ├──> [clima]    ──┤→ [memoria] → [END]
                                        └──> [general]  ──┘
```

- **llm**: Nodo que guarda el input en la base SQLite y decide la ruta.
- **finanzas/clima/general**: Nodos que responden según la ruta elegida y guardan la respuesta en la base.
- **memoria**: Nodo que muestra el historial completo guardado en la base.
- **END**: Fin del grafo.

### Ejecución

```bash
python 05_langgraph_memoria_largo_plazo.py
```

#### Salida esperada

```
=== LangGraph: Memoria a largo plazo (SQLite) ===
👤 Usuario: John
🤖 El agente no entiende bien la intención. Te responde de forma genérica.
💬 Respuesta general: gracias por tu pregunta.
🗂️ Historial completo:
usuario: John
agente: 🤖 El agente no entiende bien la intención. Te responde de forma genérica.
agente: 💬 Respuesta general: gracias por tu pregunta.
```

La base de datos `memoria.db` almacena todo el historial de la conversación, permitiendo persistencia entre ejecuciones.

---

## 6️⃣ Memoria híbrida (SQLite + FAISS)

### Estructura

```
[input] → [llm (búsqueda semántica)] ──┬──> [finanzas] ──┐
                                      ├──> [clima]    ──┤→ [memoria] → [END]
                                      └──> [general]  ──┘
```

- **input**: Nodo que guarda el input en la base y lo indexa en FAISS.
- **llm**: Nodo que realiza búsqueda semántica en la memoria vectorial y decide la ruta.
- **finanzas/clima/general**: Nodos que responden según la ruta elegida y guardan la respuesta en la base.
- **memoria**: Nodo que muestra el historial completo guardado en la base.
- **END**: Fin del grafo.

### Ejecución

```bash
python 06_langgraph_memoria_hibrida.py
```

#### Salida esperada

```
=== LangGraph: Memoria híbrida (SQLite + FAISS) ===
👤 Usuario: John Connor
📈 Pregunta detectada: finanzas. Contexto: John Connor
📊 Precio BTC: 42k (ejemplo).

📜 Historial persistente (SQLite):
1. usuario: John Connor
2. agente: 📈 Pregunta detectada: finanzas. Contexto: John Connor
3. agente: 📊 Precio BTC: 42k (ejemplo).
```

Este ejemplo combina memoria persistente (SQLite) y memoria semántica (FAISS + Sentence Transformers) para búsquedas contextuales.

---

## 🔧 Instalación

Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

El archivo [`requirements.txt`](requirements.txt) contiene:

```
langgraph
sentence-transformers
faiss-cpu
numpy
typing-extensions
```

---

## 📚 Conceptos Clave

- **Estado compartido**: Uso de `dict` para definir el estado que fluye entre nodos.
- **Nodos**: Funciones que reciben y modifican el estado.
- **Flujo**: Definición de la secuencia de ejecución entre nodos, incluyendo ciclos, memoria, búsqueda semántica y branching condicional.
- **Persistencia**: Uso de SQLite para guardar el historial de la conversación.
- **Memoria vectorial**: Uso de FAISS y Sentence Transformers para búsquedas semánticas.

---

## 🔗 Recursos

- [Documentación oficial de LangGraph](https://python.langchain.com/docs/langgraph)
- [Repositorio de LangGraph](https://github.com/langchain-ai/langgraph)

---

## 📝 Licencia

Este proyecto es de uso educativo y se distribuye bajo licencia MIT.