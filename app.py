import streamlit as st
from fpdf import FPDF
import io

# Código do Streamlit e do FPDF continua...

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
