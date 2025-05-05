# Este código deve ser executado em um ambiente com Streamlit instalado (ex: localmente ou Streamlit Cloud).
# Para rodar localmente: instale com `pip install streamlit` e execute com `streamlit run nome_do_arquivo.py`

import streamlit as st
from streamlit_extras.colored_header import colored_header
from fpdf import FPDF
import uuid
from io import BytesIO

st.set_page_config(page_title="Recomendador de Áreas Lucrativas", layout="wide")

st.markdown("""
    <style>
        .main {
            background-color: #f9f9fb;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
        }
        .stSlider>div>div {
            color: #4CAF50;
        }
        .premium {
            color: #e53935;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

colored_header("🔍 Recomendador de Áreas Lucrativas na Internet", description="Receba planos personalizados para lucrar R$10.000+ por mês.", color_name="green-70")

# Lead capture
st.markdown("💌 **Quer receber seu plano em PDF por e-mail?**")
with st.form("email_form"):
    email = st.text_input("Seu melhor e-mail:")
    nome = st.text_input("Primeiro nome:")
    enviar_email = st.form_submit_button("Quero receber por e-mail")
    if enviar_email:
        st.success("Plano será enviado assim que for gerado!")

# Formulário de entrada
with st.form("perfil_form"):
    st.markdown("### 🧠 Seu perfil digital")
    tempo_dia = st.slider("Quantas horas por dia você pode dedicar?", 0, 12, 4)
    experiencia = st.selectbox("Qual seu nível atual de experiência com internet/digital?", ["nenhuma", "baixa", "média", "alta"])
    capital_inicial = st.selectbox("Qual o capital inicial disponível?", ["nenhum", "baixo", "médio", "alto"])
    preferencias = st.multiselect("Quais atividades você tem mais interesse?", ["vídeo", "tráfego pago", "vender serviço", "ensinar", "escrever", "design"])
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

planos = {
    "YouTube Shorts + Afiliados": [
        "1. Escolha um nicho lucrativo (ex: finanças, emagrecimento, produtividade).",
        "2. Crie uma conta no YouTube e personalize seu canal.",
        "3. Encontre produtos digitais em Hotmart, Eduzz, Amazon Afiliados.",
        "4. Crie vídeos curtos com ganchos fortes e chamadas para ação.",
        "5. Use CapCut ou Canva para edição.",
        "6. Poste diariamente com títulos otimizados.",
        "7. Inclua o link de afiliado na descrição.",
        "8. Aplique copywriting para melhorar os CTAs.",
        "9. Monitore os vídeos que mais convertem."
    ],
    "Mini-funnel com PLR e tráfego pago": [
        "1. Escolha um nicho validado.",
        "2. Compre um produto PLR (IDPLR.com).",
        "3. Crie uma landing page (Systeme.io, Notion).",
        "4. Configure um domínio personalizado.",
        "5. Crie anúncios para Facebook, Instagram ou TikTok Ads.",
        "6. Comece com orçamento pequeno (R$10–30/dia).",
        "7. Otimize com base em CTR, conversão e ROI.",
        "8. Reinvista os lucros em tráfego e lista de emails.",
        "9. Automatize com funis e email marketing."
    ]
}

premium_bloqueado = ["Lançamento de infoproduto 🔒", "Mentoria/consultoria personalizada 🔒"]

# PDF export
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Plano Personalizado de Renda Online", ln=True, align="C")

    def add_plano(self, area, passos):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"\n{area}", ln=True)
        self.set_font("Arial", size=11)
        for p in passos:
            self.multi_cell(0, 8, f"- {p}")

if submit:
    recomendacoes = recomendar_areas(tempo_dia, experiencia, capital_inicial, preferencias)
    st.subheader("🔮 Áreas recomendadas para você:")
    pdf = PDF()
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

    # Exportar PDF em memória para download
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    st.download_button("📄 Baixar plano em PDF", buffer, file_name="plano_recomendado.pdf")

    # Link de indicação (programa de viralização)
    user_id = uuid.uuid4()
    st.markdown("---")
    st.markdown(f"🎁 **Compartilhe este app com amigos e desbloqueie novos planos!**\n\nSeu link único: `{st.request.host}/?ref={user_id}`")
