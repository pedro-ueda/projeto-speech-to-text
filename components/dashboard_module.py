"""Componente de visualização analítica e métricas de uso da plataforma."""
import streamlit as st
from typing import List, Dict, Any

def render_dashboard_component(data: List[Dict[str, Any]]):
    """Renderiza painéis numéricos baseados na lista atual de análises salvas."""
    st.subheader("📊 Painel de Controle e Métricas Gerais")
    
    if not data:
        st.info("Nenhum dado disponível para compor o painel analítico.")
        return

    total_analises = len(data)
    total_pessoas = sum(d["quantidade_pessoas"] for d in data)
    total_rostos = sum(d["rostos"] for d in data)
    
    # Conversão explícita antes de passar para o componente visual
    pessoas_int = int(total_pessoas)
    rostos_int = int(total_rostos)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total de Imagens Analisadas", value=total_analises)
    with col2:
        st.metric(label="Total de Pessoas Detectadas", value=pessoas_int)
    with col3:
        st.metric(label="Total de Rostos Identificados", value=rostos_int)
