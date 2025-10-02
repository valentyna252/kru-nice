# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_pdf import PdfPages

# -----------------------------
# 1. Body na kružnici
# -----------------------------
def generate_circle_points(center, radius, n_points):
    angles = np.linspace(0, 2 * np.pi, n_points, endpoint=False)
    xs = center[0] + radius * np.cos(angles)
    ys = center[1] + radius * np.sin(angles)
    return xs, ys

# -----------------------------
# 2. Vykreslení grafu s osami a jednotkou
# -----------------------------
def plot_circle(center, radius, xs, ys, color, unit):
    fig, ax = plt.subplots(figsize=(6,6))
    # kružnice
    theta = np.linspace(0, 2*np.pi, 400)
    ax.plot(center[0] + radius*np.cos(theta), 
            center[1] + radius*np.sin(theta), 'k-', lw=1)
    # body
    ax.scatter(xs, ys, c=color, s=50)
    ax.scatter([center[0]], [center[1]], c="black", s=30, label="střed")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(f"x [{unit}]")
    ax.set_ylabel(f"y [{unit}]")
    ax.grid(True, linestyle=":")
    return fig

# -----------------------------
# 3. PDF export
# -----------------------------
def create_pdf(fig, params_text):
    buf = io.BytesIO()
    with PdfPages(buf) as pdf:
        # stránka 1: graf
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        # stránka 2: text s parametry
        fig2, ax2 = plt.subplots(figsize=(8.27, 11.69))  # A4
        ax2.axis("off")
        ax2.text(0.05, 0.95, params_text, va="top", fontsize=11, family="monospace")
        pdf.savefig(fig2, bbox_inches="tight")
        plt.close(fig2)

    buf.seek(0)
    return buf

# -----------------------------
# Streamlit aplikace
# -----------------------------
st.title("Body na kružnici")

# vstupy
st.subheader("Parametry kružnice")
cx = st.number_input("Střed x", value=0.0)
cy = st.number_input("Střed y", value=0.0)
radius = st.number_input("Poloměr", value=1.0, min_value=0.0)
n_points = st.slider("Počet bodů", 1, 100, 10)
color = st.color_picker("Barva bodů", "#ff0000")
unit = st.text_input("Jednotka", "m")

center = (cx, cy)
xs, ys = generate_circle_points(center, radius, n_points)

# vykreslení
fig = plot_circle(center, radius, xs, ys, color, unit)
st.pyplot(fig)

# -----------------------------
# 4. Informace o autorovi
# -----------------------------
AUTHOR_NAME = "Valentýna Čížová"
AUTHOR_CONTACT = {
    "email": "277735@vutbr.cz"
}

st.subheader("Informace o autorovi")
cols = st.columns([1, 3])

with cols[0]:
    st.write("🧑‍💻")

with cols[1]:
    st.markdown(f"### {AUTHOR_NAME}")
    st.markdown(f"- **E-mail:** {AUTHOR_CONTACT['email']}")

# -----------------------------
# 5. Použité technologie
# -----------------------------
st.markdown("---")
st.subheader("Použité technologie")
st.write(
    """
    - **Streamlit**  
    - **Python**  
    - **Matplotlib**  
    """
)

# -----------------------------
# 6. Export do PDF
# -----------------------------
st.subheader("Export do PDF")
params_text = (
    f"Body na kružnici\n\n"
    f"Střed: {center}\n"
    f"Poloměr: {radius} {unit}\n"
    f"Počet bodů: {n_points}\n"
    f"Barva: {color}\n\n"
    f"Autor: {AUTHOR_NAME}\n"
    f"Kontakt: {AUTHOR_CONTACT['email']}\n"
)
pdf_bytes = create_pdf(plot_circle(center, radius, xs, ys, color, unit), params_text)

st.download_button("📄 Stáhnout PDF", data=pdf_bytes, file_name="kruznice.pdf", mime="application/pdf")
