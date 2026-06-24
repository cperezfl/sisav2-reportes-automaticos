import streamlit as st
import json
from pipeline import ReporteSlots, construir_documento_docx

st.set_page_config(page_title="G3 - Reportes VcM", page_icon="📊", layout="centered")

st.title("📊 Sistema de Reportes Automáticos VcM")
st.subheader("Fase de Avance S13 — Grupo 3")

st.markdown("""
Este prototipo demuestra la arquitectura técnica acordada:
1. **Ingesta:** Lectura de datos estructurados de iniciativas en formato JSON.
2. **Validación de Esquema:** Uso de **Pydantic v2** para garantizar tipos de datos estrictos.
3. **Control de Calidad:** Simulación del pipeline de evaluación automatizada con **RAGAS**.
""")

# Cargar el JSON mock original
with open("iniciativa_2606.json", "r", encoding="utf-8") as f:
    datos_json = json.load(f)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📥 1. Entrada desde SISAV2")
    st.json(datos_json)

with col2:
    st.markdown("### 🔧 2. Parámetros del LLM & RAGAS")
    score_ragas = st.slider("Faithfulness del LLM (Simulado)", 0.0, 1.0, 0.89, step=0.05)
    
    # Simulación de los campos narrativos que procesará el modelo
    resumen = st.text_area("Slot Generativo: Resumen Ejecutivo", "Este proyecto implementa un pipeline automatizado para estructurar datos dispersos de iniciativas socio-comunitarias, reduciendo el trabajo operativo de la Dirección de Vinculación con el Medio...")
    conclusiones = st.text_area("Slot Generativo: Conclusiones", "La automatización elimina el trabajo repetitivo sin comprometer el criterio profesional del analista institucional de la universidad.")

if st.button("🚀 Procesar en Pipeline y Generar Borrador .docx"):
    payload = {
        "id_iniciativa": datos_json["metadata"]["id_iniciativa"],
        "titulo": datos_json["datos_deterministicos"]["titulo"],
        "facultad": datos_json["datos_deterministicos"]["facultad"],
        "carrera": datos_json["datos_deterministicos"]["carrera"],
        "resumen_ejecutivo": resumen,
        "conclusiones_vcm": conclusiones,
        "ragas_faithfulness": score_ragas
    }
    
    try:
        # Validación en tiempo de ejecución con Pydantic
        datos_validados = ReporteSlots(**payload)
        st.success("✅ Validación Pydantic Correcta. RAGAS Faithfulness por sobre el umbral mínimo (0.75).")
        
        # Generar el documento real en memoria
        docx_buffer = construir_documento_docx(datos_validados)
        
        st.download_button(
            label="📥 Descargar Borrador Oficial (.docx)",
            data=docx_buffer,
            file_name=f"Borrador_Iniciativa_{datos_validados.id_iniciativa}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"❌ Error de Validación del Pipeline: {e}")
        st.warning("⚠️ El pipeline bloqueó la exportación. El borrador presenta baja fidelidad con los datos de origen o fallas en el formato.")