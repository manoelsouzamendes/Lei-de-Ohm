import streamlit as st
import math

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Calc. Eletricista - Prof. Manoel", page_icon="⚡", layout="centered")

# --- CABEÇALHO ---
st.title("⚡ Calculadora do Eletricista")
st.subheader("Desenvolvido por Prof. Manoel Mendes")
st.markdown("---") 

# --- MENU LATERAL ---
with st.sidebar:
    st.header("Menu de Ferramentas")
    menu = st.selectbox(
        "Selecione o módulo:",
        [
            "1. Lei de Ohm & Potência (1ª Lei)", 
            "2. Resistividade (2ª Lei de Ohm)", 
            "3. Dimensionamento por Corrente (Ampacidade)", 
            "4. Dimensionamento por Queda de Tensão",  # NOME ATUALIZADO
            "5. Simulador de Conta de Luz"
        ]
    )
    st.markdown("---")
    st.info("Ferramenta didática para auxílio em projetos elétricos e aulas.")

# =========================================================
# MÓDULO 1: 1ª LEI DE OHM & POTÊNCIA
# =========================================================
if menu == "1. Lei de Ohm & Potência (1ª Lei)":
    st.header("🔌 1ª Lei de Ohm e Potência")
    st.markdown("Preencha **dois valores** conhecidos para descobrir os outros dois.")
    
    col1, col2 = st.columns(2)
    with col1:
        v = st.number_input("Tensão - Volts (V)", min_value=0.0, step=0.1, format="%.2f")
        i = st.number_input("Corrente - Amperes (A)", min_value=0.0, step=0.1, format="%.2f")
    with col2:
        r = st.number_input("Resistência - Ohms (Ω)", min_value=0.0, step=0.1, format="%.2f")
        p = st.number_input("Potência - Watts (W)", min_value=0.0, step=0.1, format="%.2f")

    if st.button("Calcular Grandezas", type="primary"):
        st.markdown("---")
        try:
            inputs = [v > 0, i > 0, r > 0, p > 0]
            if sum(inputs) != 2:
                 st.warning("⚠️ Por favor, preencha exatamente dois campos.")
            else:
                formula_usada = ""
                if v and i: 
                    r, p = v/i, v*i
                    formula_usada = r"R = \frac{V}{I} \quad e \quad P = V \cdot I"
                elif v and r: 
                    i, p = v/r, (v**2)/r
                    formula_usada = r"I = \frac{V}{R} \quad e \quad P = \frac{V^2}{R}"
                elif v and p: 
                    i, r = p/v, (v**2)/p
                    formula_usada = r"I = \frac{P}{V} \quad e \quad R = \frac{V^2}{P}"
                elif i and r: 
                    v, p = r*i, r*(i**2)
                    formula_usada = r"V = R \cdot I \quad e \quad P = R \cdot I^2"
                elif i and p: 
                    v, r = p/i, p/(i**2)
                    formula_usada = r"V = \frac{P}{I} \quad e \quad R = \frac{P}{I^2}"
                elif r and p: 
                    v, i = math.sqrt(p*r), math.sqrt(p/r)
                    formula_usada = r"V = \sqrt{P \cdot R} \quad e \quad I = \sqrt{\frac{P}{R}}"
                
                st.success("✅ Resultados Encontrados!")
                st.latex(formula_usada)
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Tensão (V)", f"{v:.2f} V")
                c2.metric("Corrente (I)", f"{i:.2f} A")
                c3.metric("Resistência (R)", f"{r:.2f} Ω")
                c4.metric("Potência (P)", f"{p:.2f} W")

        except ZeroDivisionError: 
            st.error("Erro Matemático: Divisão por zero.")

# =========================================================
# MÓDULO 2: 2ª LEI DE OHM
# =========================================================
elif menu == "2. Resistividade (2ª Lei de Ohm)":
    st.header("📏 2ª Lei de Ohm (Resistência do Fio)")
    st.latex(r"R = \frac{\rho \cdot L}{A}")
    
    col_input, col_ref = st.columns([1.5, 1])
    with col_input:
        material = st.selectbox("Selecione o Material:", ["Cobre", "Alumínio", "Ouro"])
        comprimento = st.number_input("Comprimento do condutor (metros):", min_value=0.0, step=1.0)
        secao = st.number_input("Seção Transversal / Bitola (mm²):", min_value=0.0, step=0.5, value=2.5)
    with col_ref:
        st.markdown("##### 📋 Resistividade (ρ)")
        materiais = {"Cobre": 0.0172, "Alumínio": 0.0282, "Ouro": 0.0244}
        rho = materiais[material]
        st.info(f"Usando **{material}**:\n\n **{rho}** Ω.mm²/m")

    if st.button("Calcular Resistência", type="primary"):
        if secao > 0:
            resistencia_fio = (rho * comprimento) / secao
            st.markdown("---")
            st.markdown(f"""
                <div style="text-align: center; border: 2px solid #4CAF50; padding: 20px; border-radius: 10px; background-color: #f9fff9;">
                    <p style="color: #4CAF50; font
