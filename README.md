# 📊 Sistema de Reportes Automáticos VcM — UTEM 2026-I

**Curso:** INFB6093 Procesamiento de Lenguaje Natural  
**Docente:** Jaime Jiménez Ruiz  
**Socio Comunitario:** Claudia Urrutia — Dirección de Vinculación con el Medio (VcM)  
**Hito Actual:** Avance S13 (24 de junio de 2026) — Checkpoint Formativo  
**Equipo (Grupo 3):** Yenderi Albayay · Christian Pérez · Pablo Ibáñez  

---

## 1. Declaración del Problema Institucional

El equipo de analistas de la Dirección de VcM de la UTEM redacta manualmente los informes de gestión y los reportes de evidencias al cierre de cada semestre. Con un volumen aproximado de ~300 iniciativas al año, este proceso consume días enteros de trabajo operativo (particularmente en el mes de enero), genera formatos inconsistentes entre analistas y duplica contenido estructurado que ya reside en la base de datos de SISAV2. La falta de un pipeline automatizado imposibilita la entrega oportuna de métricas e historias institucionales clave para los procesos de acreditación ante la CNA y el seguimiento del PDI.

---

## 2. Solución Propuesta y Filosofía de Diseño

Construir un **pipeline automatizado de generación documental** que consuma los datos transaccionales de SISAV2 y los inyecte en plantillas estructuradas utilizando el stack obligatorio de la asignatura.

> 💡 **Filosofía de diseño:** El reporte automático es un borrador de alta calidad, no un reporte final. El sistema elimina el trabajo operativo repetitivo, pero el analista mantiene siempre el control profesional, pudiendo revisar, editar y regenerar los componentes narrativos antes de exportar el documento definitivo.

### Árbol de Decisión: ¿Por qué no Fine-Tuning?
Descartamos el uso de Fine-Tuning/PEFT debido a la inexistencia de un dataset masivo de entrenamiento histórico entrada-salida y porque la capacidad semántica base de los LLM actuales (Claude/Gemini) es idónea para tareas de síntesis. Optamos por una arquitectura de **Prompting + Structured Output** balanceada con lógica determinística tradicional.

---

## 3. Arquitectura del Pipeline Técnico


El flujo de procesamiento diseñado para el proyecto está automatizado mediante el siguiente pipeline de componentes:

```
graph TD
    A[SISAV2 JSON] --> B[Ingesta/Validación <br> Pydantic v2]
    B --> C{Mapping Determinístico <br> python-docx}
    C -->|Campos Fijos <br> Sin LLM| D[Slots Directos: <br> IDs, Carreras, Asistencia]
    C -->|Campos Narrativos <br> LLM + Few-Shot| E[Slots Generativos: <br> Resumen, Lecciones]
    E --> F[Validación RAGAS <br> Faithfulness >= 0.75]
    D --> G[Interfaz de Revisión <br> Streamlit]
    F --> G
    G --> H[.docx Final Editable]
```

1. **Ingesta y Validación Estricta:** Entrada de datos transaccionales validados mediante esquemas de **Pydantic v2** para mitigar fallas por campos corruptos o vacíos provenientes de SISAV2.
2. **Mapping Determinístico:** Transferencia directa mediante código Python de variables duras cuantitativas (IDs, nombres de asignaturas, facultades, carreras y totales de asistencia). El LLM tiene estrictamente prohibido alterar o procesar números para salvaguardar los KPIs institucionales.
3. **Generación con LLM Controlado:** Procesamiento mediante prompts estructurados de las áreas de texto libre (resúmenes, conclusiones y lecciones aprendidas).
4. **Control de Calidad (RAGAS Framework):** Evaluación automatizada post-generación de la fidelidad (*Faithfulness*) del texto del LLM contra el JSON de entrada, utilizando un umbral crítico de **0.75**.
5. **Override Humano (UI Streamlit):** Interfaz web que presenta el estado del borrador, calcula las métricas y permite la edición manual antes de la descarga en formato editable `.docx`.

---

## 4. Análisis Empírico de Iniciativas (Fundamento de Ingeniería)

Nuestra arquitectura y reglas de validación en el código nacen de la auditoría estructural de los casos de estudio reales provistos por la universidad:

* **La Referencia de Éxito (Iniciativa 2606 - Tronconoble en Villarrica):** Actúa como nuestra *Golden Truth*. Presenta una consistencia temporal e institucional impecable, sirviendo como la base para el diseño visual de las plantillas en `python-docx` y aportando los fragmentos de texto formal utilizados en nuestros **Few-Shot Prompts** de estilo.
* **Detección de Fallas (Iniciativas Malas 2690, 2724, 2788):** 
  * En la **2690**, detectamos un quiebre de consistencia en fechas de ejecución y vacíos en las evidencias fotográficas.
  * En la **2724**, se evidenció un ingreso retroactivo que causó inconsistencias numéricas graves (la descripción declara 4 estudiantes pero el acta manuscrita solo tiene 2 firmas físicas válidas).
  * En la **2788**, el docente ingresó un socio comunitario inexistente en la postulación ("Liceo SFF") y omitió especificaciones de honorarios.
  
Estos quiebres reales justifican por qué nuestro pipeline incluye un cortafuegos en Pydantic para longitudes de texto deficientes y una alerta restrictiva controlada por el score de RAGAS.

---

## 5. Estado Actual del Repositorio (MVP S13)

Este repositorio contiene el Prototipo Inicial Mínimo Viable (MVP) que demuestra la viabilidad técnica de la arquitectura diseñada:
* `iniciativa_2606.json`: Estructura base de datos simulada a partir de los expedientes reales de VcM.
* `pipeline.py`: Módulo que concentra el esquema de validación estructural mediante **Pydantic v2** y el motor de construcción visual del borrador usando **python-docx**.
* `app.py`: Interfaz de usuario interactiva montada sobre **Streamlit** que simula el procesamiento del pipeline y expone el botón de descarga del borrador abierto editable.

---

## 6. Instrucciones de Ejecución Local

### Prerrequisitos
Asegúrese de contar con Python 3.9 o superior e instalar las dependencias del stack obligatorio del proyecto:

```
pip install streamlit python-docx pydantic
