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
            "3. Dimensionamento de Cabos", 
            "4. Simulador de Conta de Luz"
        ]
    )
    st.markdown("---")
    st.info("Ferramenta didática para auxílio em projetos elétricos e aulas.")

# =========================================================
# MÓDULO 1: 1ª LEI DE OHM & POTÊNCIA
# =========================================================
if menu == "1. Lei de Ohm & Potência (1ª Lei)":
    st.header(" 1ª Lei de Ohm e Potência")
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
                st.markdown("##### 📝 Fórmulas Aplicadas:")
                st.latex(formula_usada)
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Tensão (V)", f"{v:.2f} V")
                c2.metric("Corrente (I)", f"{i:.2f} A")
                c3.metric("Resistência (R)", f"{r:.2f} Ω")
                c4.metric("Potência (P)", f"{p:.2f} W")

        except ZeroDivisionError: 
            st.error("Erro Matemático: Divisão por zero detectada.")

# =========================================================
# MÓDULO 2: 2ª LEI DE OHM (VISUAL NOVO)
# =========================================================
elif menu == "2. Resistividade (2ª Lei de Ohm)":
    st.header("📏 2ª Lei de Ohm (Resistência do Fio)")
    
    st.markdown("""
    A resistência elétrica de um condutor depende do material ($ρ rô$), do comprimento ($L$) e da área da seção transversal ($A$).
    """)
    st.latex(r"R = \frac{\rho \cdot L}{A}")
    
    col_input, col_ref = st.columns([1.5, 1])
    
    with col_input:
        material = st.selectbox("Selecione o Material:", ["Cobre", "Alumínio", "Ouro", "Prata"])
        comprimento = st.number_input("Comprimento do condutor (metros):", min_value=0.0, step=1.0)
        secao = st.number_input("Seção Transversal / Bitola (mm²):", min_value=0.0, step=0.5, value=2.5)
    
    with col_ref:
        st.markdown("##### 📋 Resistividade (ρ)")
        materiais = {"Cobre": 0.0172, "Alumínio": 0.0282, "Ouro": 0.0244, "Prata": 0.0159}
        rho = materiais[material]
        
        st.info(f"Usando **{material}**:\n\n **{rho}** Ω.mm²/m")

    if st.button("Calcular Resistência", type="primary"):
        if secao > 0:
            resistencia_fio = (rho * comprimento) / secao
            
            st.markdown("---")
            
            # --- AQUI ESTÁ A MUDANÇA VISUAL ---
            # Cria um box visual com HTML para destacar o número
            st.markdown(f"""
                <div style="text-align: center; border: 2px solid #4CAF50; padding: 20px; border-radius: 10px; background-color: #f9fff9;">
                    <p style="color: #4CAF50; font-size: 20px; margin-bottom: 5px;"><b>Resistência Total do Fio (R)</b></p>
                    <p style="color: #2E7D32; font-size: 50px; font-weight: bold; margin: 0;">{resistencia_fio:.4f} Ω</p>
                </div>
            """, unsafe_allow_html=True)
            # ----------------------------------
            
            st.write("") # Espaço vazio
            st.info(f"💡 **Análise:** Se passar 10A neste fio, a queda de tensão será de **{resistencia_fio * 10:.2f} Volts**.")
            
        else:
            st.error("A seção (bitola) não pode ser zero.")

# =========================================================
# MÓDULO 3: CABOS
# =========================================================
elif menu == "3. Dimensionamento de Cabos":
    st.header("elementos 3. Dimensionamento de Condutores")
    st.caption("Critério de Capacidade de Corrente - NBR 5410 | Ref: Método B1, PVC.")
    
    corrente_projeto = st.number_input("Corrente de Projeto (A):", min_value=0.0, step=0.1)
    
    if st.button("Dimensionar Cabo"):
        tabela = {1.5: 17.5, 2.5: 24.0, 4.0: 32.0, 6.0: 41.0, 10.0: 57.0, 16.0: 76.0, 25.0: 101.0, 35.0: 125.0, 50.0: 151.0}
        escolhido, cap = None, 0
        
        for s, a in tabela.items():
            if a >= corrente_projeto:
                escolhido, cap = s, a
                break
        
        st.divider()
        if escolhido:
            c1, c2 = st.columns(2)
            c1.success(f"✅ Cabo Ideal: **{escolhido} mm²**")
            c2.info(f"Capacidade Máxima: **{cap} A**")
        else:
            st.error("⚠️ Corrente muito alta para cabos comuns nesta tabela.")

# =========================================================
# MÓDULO 4: CONTA DE LUZ
# =========================================================
elif menu == "4. Simulador de Conta de Luz":
    st.header("💸 4. Simulador de Custo de Energia")
    
    c1, c2 = st.columns(2)
    with c1:
        w = st.number_input("Potência do Aparelho (Watts):", step=10.0)
        h = st.number_input("Horas de uso por dia:", step=0.5, max_value=24.0)
    with c2:
        d = st.number_input("Dias de uso por mês:", value=30, max_value=31)
        rs = st.number_input("Preço do kWh (R$):", value=0.85, step=0.01)

    if st.button("Calcular Custo Mensal"):
        kwh = (w * h * d) / 1000
        total = kwh * rs
        
        st.divider()
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Consumo (kWh)", f"{kwh:.2f} kWh")
        col_m2.metric("Custo Estimado", f"R$ {total:.2f}")
        
        st.caption(f"Cálculo: ({w}W x {h}h x {d}d) ÷ 1000 = {kwh} kWh")

# --- RODAPÉ ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>© 2025 - Prof. Manoel Mendes</div>", unsafe_allow_html=True)


