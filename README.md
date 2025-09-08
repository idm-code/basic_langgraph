# LangGraph Tutorial - Primer Grafo

Este proyecto contiene un tutorial introductorio para crear grafos con LangGraph, una biblioteca para construir aplicaciones con estado usando grafos dirigidos.

## 📋 Descripción

El archivo [01_langgraph_primer_grafo.py](01_langgraph_primer_grafo.py) implementa un grafo básico de dos nodos que demuestra los conceptos fundamentales de LangGraph:

- **Estado compartido**: Uso de `TypedDict` para definir el estado que fluye entre nodos
- **Nodos**: Funciones que reciben y modifican el estado
- **Flujo**: Definición de la secuencia de ejecución entre nodos

## 🏗️ Estructura del Grafo

```
[Nodo A] → [Nodo B] → [END]
```

1. **Nodo A**: Genera un mensaje inicial y lo almacena en el estado
2. **Nodo B**: Procesa el mensaje del Nodo A y genera una respuesta
3. **END**: Termina la ejecución del grafo

## 🔧 Instalación

Instala las dependencias necesarias:

```bash
pip install langgraph typing-extensions
```

## 🚀 Ejecución

Ejecuta el script principal:

```bash
python 01_langgraph_primer_grafo.py
```

### Salida esperada:

```
=== Ejecutando el grafo ===
🟢 Nodo A ejecutado
🔵 Nodo B ejecutado
📌 Estado final: {'mensaje': 'Hola desde el nodo A', 'respuesta': 'Hola desde el nodo A → Procesado en nodo B'}
```

## 📚 Conceptos Clave

### Estado (TypedDict)
```python
class Estado(TypedDict):
    mensaje: str      # Campo para almacenar el mensaje del nodo A
    respuesta: str    # Campo para almacenar la respuesta procesada del nodo B
```

### Nodos
Los nodos son funciones que:
- Reciben el estado actual como parámetro
- Modifican el estado según su lógica
- Retornan el estado modificado

### Construcción del Grafo
```python
workflow = StateGraph(Estado)
workflow.add_node("A", nodo_a)
workflow.add_node("B", nodo_b)
workflow.set_entry_point("A")
workflow.add_edge("A", "B")
workflow.add_edge("B", END)
```

## 🎯 Objetivos de Aprendizaje

Este ejemplo enseña:
- ✅ Cómo definir un estado tipado con `TypedDict`
- ✅ Cómo crear nodos que modifiquen el estado
- ✅ Cómo construir un flujo secuencial básico
- ✅ Cómo compilar y ejecutar un grafo

## 🔗 Recursos

- [Documentación oficial de LangGraph](https://python.langchain.com/docs/langgraph)
- [Repositorio de LangGraph](https://github.com/idm-code/basic_langgraph)

## 📝 Licencia

Este proyecto es de uso educativo y se distribuye bajo licencia MIT.