# 📊 Sistema de Reportes Automáticos VcM — UTEM 2026-I

**Curso:** INFB6093 Procesamiento de Lenguaje Natural  
**Docente:** Jaime Jiménez Ruiz  
**Socio Comunitario:** Claudia Urrutia — Dirección de Vinculación con el Medio (VcM)  
**Hito Actual:** Avance S13 (24 de junio de 2026) — Checkpoint Formativo  
**Equipo (Grupo 3):** Yenderi Albayay · Christian Pérez · Pablo Ibáñez  

---

## 1. Declaración del Problema Institucional

El equipo de analistas de la Dirección de VcM de la UTEM redacta manualmente los informes de gestión y los reportes de evidencias al cierre de cada semestre[cite: 2]. Con un volumen aproximado de ~300 iniciativas al año, este proceso consume días enteros de trabajo operativo (particularmente en el mes de enero), genera formatos inconsistentes entre analistas y duplica contenido estructurado que ya reside en la base de datos de SISAV2[cite: 2]. La falta de un pipeline automatizado imposibilita la entrega oportuna de métricas e historias institucionales clave para los procesos de acreditación ante la CNA y el seguimiento del PDI[cite: 2].

---

## 2. Solución Propuesta y Filosofía de Diseño

Construir un **pipeline automatizado de generación documental** que consuma los datos transaccionales de SISAV2 y los inyecte en plantillas estructuradas utilizando el stack obligatorio de la asignatura[cite: 2, 3].

> 💡 **Filosofía de diseño:** El reporte automático es un borrador de alta calidad, no un reporte final[cite: 2, 3]. El sistema elimina el trabajo operativo repetitivo, pero el analista mantiene siempre el control profesional, pudiendo revisar, editar y regenerar los componentes narrativos antes de exportar el documento definitivo[cite: 2].

### Árbol de Decisión: ¿Por qué no Fine-Tuning?
Descartamos el uso de Fine-Tuning/PEFT debido a la inexistencia de un dataset masivo de entrenamiento histórico entrada-salida y porque la capacidad semántica base de los LLM actuales (Claude/Gemini) es idónea para tareas de síntesis[cite: 2]. Optamos por una arquitectura de **Prompting + Structured Output** balanceada con lógica determinística tradicional[cite: 2].

---

## 3. Arquitectura del Pipeline Técnico

El flujo de procesamiento diseñado para el proyecto se compone de 5 etapas[cite: 2]: