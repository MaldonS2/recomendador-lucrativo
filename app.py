import streamlit as st

st.set_page_config(page_title="Recomendador de Áreas Lucrativas", layout="wide")

st.title("🔍 Recomendador de Áreas Lucrativas na Internet")
st.markdown("Responda às perguntas abaixo para receber recomendações de áreas com potencial de lucro acima de R$10.000/mês.")

# Formulário de entrada
with st.form("perfil_form"):
    tempo_dia = st.slider("Quantas horas por dia você pode dedicar?", 0, 12, 4)
    experiencia = st.selectbox("Qual seu nível atual de experiência com internet/digital?", ["nenhuma", "baixa", "média", "alta"])
    capital_inicial = st.selectbox("Qual o capital inicial disponível?", ["nenhum", "baixo", "médio", "alto"])
    preferencias = st.multiselect("Quais atividades você tem mais interesse?", ["vídeo", "tráfego pago", "vender serviço", "ensinar", "escrever", "design"])
    submit = st.form_submit_button("Gerar Recomendação")

# Função de recomendação
@st.cache_data
def recomendar_areas(tempo_dia, experiencia, capital_inicial, preferencias):
    recomendacoes = []

    if tempo_dia < 2:
        recomendacoes.append("Freelancing rápido (ex: microtarefas, revisão de texto)")
        if 'escrever' in preferencias:
            recomendacoes.append("Copywriting para afiliados")
        if experiencia in ['média', 'alta']:
            recomendacoes.append("Consultoria expressa via redes sociais")

    if 2 <= tempo_dia < 5:
        if 'vídeo' in preferencias:
            recomendacoes.append("YouTube Shorts + Afiliados")
        if capital_inicial in ['baixo', 'médio'] and 'tráfego pago' in preferencias:
            recomendacoes.append("Mini-funnel com PLR e tráfego pago")
        recomendacoes.append("Serviços de design ou edição para Instagram/TikTok")

    if tempo_dia >= 5:
        if capital_inicial in ['médio', 'alto']:
            recomendacoes.append("Dropshipping com tráfego pago")
            recomendacoes.append("Lançamento de infoproduto")
        if experiencia == 'alta' and 'ensinar' in preferencias:
            recomendacoes.append("Mentoria/consultoria personalizada")
        recomendacoes.append("Criação de canal no YouTube com SEO e monetização")

    if capital_inicial == 'nenhum' and experiencia == 'nenhuma':
        recomendacoes.append("TikTok orgânico com produtos de afiliado")

    return list(set(recomendacoes))

# Detalhamento dos planos
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

# Resultado
if submit:
    recomendacoes = recomendar_areas(tempo_dia, experiencia, capital_inicial, preferencias)
    st.subheader("🔮 Áreas recomendadas para você:")
    for area in recomendacoes:
        st.markdown(f"### ✅ {area}")
        if area in planos:
            with st.expander("Ver plano passo a passo"):
                for passo in planos[area]:
                    st.markdown(f"- {passo}")
