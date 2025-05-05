import streamlit as st
from fpdf import FPDF
import io
import uuid

# Código de layout e outras definições...

# Formulário de entrada
with st.form("perfil_form"):
    st.markdown("### 🧠 Seu perfil digital")
    tempo_dia = st.slider("Quantas horas por dia você pode dedicar?", 0, 12, 4)
    experiencia = st.selectbox("Qual seu nível atual de experiência com internet/digital?", ["nenhuma", "baixa", "média", "alta"])
    capital_inicial = st.selectbox("Qual o capital inicial disponível?", ["nenhum", "baixo", "médio", "alto"])
    preferencias = st.multiselect("Quais atividades você tem mais interesse?", ["vídeo", "tráfego pago", "vender serviço", "ensinar", "escrever", "design"])
    
    # Aqui definimos o botão 'submit'
    submit = st.form_submit_button("🔎 Gerar Recomendação")

@st.cache_data
def recomendar_areas(tempo_dia, experiencia, capital_inicial, preferencias):
    recomendacoes = {}

    if tempo_dia < 2:
        recomendacoes["Freelancing rápido (ex: microtarefas, revisão de texto)"] = 60
        if 'escrever' in preferencias:
            recomendacoes["Copywriting para afiliados"] = 70
        if experiencia in ['média', 'alta']:
            recomendacoes["Consultoria expressa via redes sociais"] = 75

    if 2 <= tempo_dia < 5:
        if 'vídeo' in preferencias:
            recomendacoes["YouTube Shorts + Afiliados"] = 90
        if capital_inicial in ['baixo', 'médio'] and 'tráfego pago' in preferencias:
            recomendacoes["Mini-funnel com PLR e tráfego pago"] = 85
        recomendacoes["Serviços de design ou edição para Instagram/TikTok"] = 80

    if tempo_dia >= 5:
        if capital_inicial in ['médio', 'alto']:
            recomendacoes["Dropshipping com tráfego pago"] = 88
            recomendacoes["Lançamento de infoproduto 🔒"] = 90
        if experiencia == 'alta' and 'ensinar' in preferencias:
            recomendacoes["Mentoria/consultoria personalizada 🔒"] = 92
        recomendacoes["Criação de canal no YouTube com SEO e monetização"] = 89

    if capital_inicial == 'nenhum' and experiencia == 'nenhuma':
        recomendacoes["TikTok orgânico com produtos de afiliado"] = 70

    return sorted(recomendacoes.items(), key=lambda x: x[1], reverse=True)

if submit:  # Agora a variável 'submit' está definida corretamente
    recomendacoes = recomendar_areas(tempo_dia, experiencia, capital_inicial, preferencias)
    st.subheader("🔮 Áreas recomendadas para você:")
    pdf = FPDF()
    pdf.add_page()
    for area, score in recomendacoes:
        bloqueado = area in premium_bloqueado
        tag = "🔒" if bloqueado else "✅"
        st.markdown(f"### {tag} {area} — Compatibilidade: {score}%")
        if not bloqueado:
            if area in planos:
                with st.expander("📘 Ver plano passo a passo"):
                    for passo in planos[area]:
                        st.markdown(f"- {passo}")
                    pdf.add_plano(area, planos[area])
        else:
            st.markdown("<div class='premium'>🔒 Este plano é Premium. Compartilhe o app para desbloquear!</div>", unsafe_allow_html=True)

    # Gerar PDF em memória com BytesIO
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    # Disponibilizar o PDF para download
    st.download_button(
        label="📄 Baixar plano em PDF",
        data=pdf_output,
        file_name="plano_recomendado.pdf",
        mime="application/pdf"
    )

    # Link de indicação (programa de viralização)
    user_id = uuid.uuid4()
    st.markdown("---")
    st.markdown(f"🎁 **Compartilhe este app com amigos e desbloqueie novos planos!**\n\nSeu link único: `{st.request.host}/?ref={user_id}`")
