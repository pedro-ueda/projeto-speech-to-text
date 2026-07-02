"""Componente visual estruturado para histórico, filtros e exportações."""
import streamlit as st
from typing import List, Dict, Any
from utils.exporters import export_to_csv, export_to_json
from pathlib import Path

def render_history_component(data: List[Dict[str, Any]], controller):
    """Renderiza a listagem de registros históricos filtrados e com ações reativas."""
    st.subheader("📋 Histórico Registrado e Auditoria")

    if not data:
        st.warning("Nenhum registro encontrado para os filtros atuais.")
        return

    # Seção de Exportações globais de dados da tabela corrente
    st.markdown("### Exportar Conjunto de Dados")
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        csv_data = export_to_csv(data)
        st.download_button(label="📥 Exportar para CSV", data=csv_data, file_name="historico_analises.csv", mime="text/csv")
    with col_exp2:
        json_data = export_to_json(data)
        st.download_button(label="📥 Exportar para JSON", data=json_data, file_name="historico_analises.json", mime="application/json")

    st.markdown("---")

    # Listagem de itens em formato card estendido
    for item in data:
        with st.container():
            col_img, col_info = st.columns([1, 2])
            
            with col_img:
                if Path(item["image_path"]).exists():
                    st.image(item["image_path"], use_container_width=True)
                else:
                    st.error("Arquivo local indisponível.")
            
            with col_info:
                st.markdown(f"**ID:** {item['id']} | **Data:** {item['created_at'].strftime('%d/%m/%Y %H:%M:%S')}")
                st.markdown(f"**Descrição:** {item['descricao']}")
                st.markdown(f"**Objetos Encontrados:** {', '.join(item['objetos']) if item['objetos'] else 'Nenhum'}")
                st.markdown(f"**Pessoas:** {item['quantidade_pessoas']} | **Rostos:** {item['rostos']}")
                st.markdown(f"**Luminosidade:** {item['luminosidade']} | **Nitidez:** {item['nitidez']}")
                
                st.info(f"💬 **Transcrição do Áudio:** {item['transcricao']}")

                # Ações contextuais por registro
                c1, c2, c3 = st.columns(3)
                with c1:
                    if Path(item["image_path"]).exists():
                        with open(item["image_path"], "rb") as file:
                            st.download_button(
                                label="💾 Baixar Foto",
                                data=file,
                                file_name=f"foto_{item['id']}.jpg",
                                mime="image/jpeg",
                                key=f"dl_{item['id']}"
                            )
                with c2:
                    # Inserção/Atualização dinâmica de notas por voz
                    new_audio = st.file_uploader("Substituir áudio:", type=["wav", "mp3"], key=f"audio_up_{item['id']}")
                    if new_audio:
                        if st.button("Confirmar Novo Áudio", key=f"btn_audio_{item['id']}"):
                            txt = controller.audio_service.transcribe(new_audio.read())
                            controller.update_transcription(item['id'], txt)
                            st.toast("Áudio atualizado com sucesso!")
                            st.rerun()
                with c3:
                    if st.button("🗑️ Excluir", key=f"del_{item['id']}", help="Remove permanentemente o registro e a imagem"):
                        controller.delete_analysis(item['id'])
                        st.toast("Análise removida com sucesso!")
                        st.rerun()
            st.markdown("---")