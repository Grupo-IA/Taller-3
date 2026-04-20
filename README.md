# 🕵️‍♂️ Taller 3: Investigación Criminalística con Lógica

**Universidad de los Andes** **Facultad de Ingeniería - Departamento de Ingeniería de Sistemas y Computación** **Curso:** ISIS-1611 Inteligencia Artificial (Semestre 2026-10)

---

## 👥 Equipo de Detectives (Grupo 8)
* **Karen Fuentes** - 202122467
* **Sofia Sarasty** - 202511871
* **Juan Pablo Camacho Peña** - 202110977

---

## 📝 Descripción del Proyecto
Este repositorio contiene la implementación de un motor de inferencia lógica diseñado para resolver crímenes. El proyecto abarca dos grandes paradigmas de la lógica formal:

1. **Lógica Proposicional:** Implementación de algoritmos de Model Checking y transformaciones de fórmulas lógicas a Forma Normal Conjuntiva (CNF).
2. **Lógica de Predicados:** Modelado de bases de conocimiento usando Cláusulas de Horn y motores de encadenamiento hacia adelante (*forward chaining*) y hacia atrás (*backward chaining*) para deducir culpables en cinco casos criminales distintos.

---

## 📂 Estructura del Repositorio

El proyecto está organizado de la siguiente manera:

* `src/`: Contiene el núcleo del motor lógico (`model_checking.py`, `cnf_transform.py`, `resolution.py`, etc.).
* `crimes/`: Archivos donde se definen los hechos y reglas (Knowledge Base) de los 5 casos criminales.
* `tests/`: Pruebas unitarias para verificar la correctitud de los algoritmos de lógica proposicional y de predicados.
* `notebooks/`: Guías interactivas proporcionadas para entender el modelado lógico.
* `main.py`: Punto de entrada principal y terminal interactiva de usuario (TUI).

---

## 🚀 Instalación y Ejecución

El proyecto utiliza `uv` como gestor de paquetes y dependencias de Python. Asegúrese de tenerlo instalado antes de ejecutar el código.

### 1. Ejecución interactiva
Para explorar los casos criminales como un verdadero detective usando la interfaz de terminal, ejecute:
```bash
uv run main.py
