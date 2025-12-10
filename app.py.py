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
                    <p style="color: #4CAF50; font-size: 20px; margin-bottom: 5px;"><b>Resistência Total do Fio (R)</b></p>
                    <p style="color: #2E7D32; font-size: 50px; font-weight: bold; margin: 0;">{resistencia_fio:.4f} Ω</p>
                </div>
            """, unsafe_allow_html=True)
            st.write("")
            st.info(f"💡 Se passar 10A neste fio, perderá **{resistencia_fio * 10:.2f} Volts** no caminho.")
        else:
            st.error("A seção (bitola) não pode ser zero.")

# =========================================================
# MÓDULO 3: CABOS (AMPACIDADE)
# =========================================================
elif menu == "3. Dimensionamento por Corrente (Ampacidade)":
    st.header("🔥 3. Dimensionamento por Corrente")
    st.caption("Critério de Capacidade de Corrente - NBR 5410 | Ref: Método B1, PVC.")
    
    corrente_projeto = st.number_input("Corrente de Projeto (A):", min_value=0.0, step=0.1)
    
    if st.button("Buscar Cabo"):
        tabela = {1.5: 17.5, 2.5: 24.0, 4.0: 32.0, 6.0: 41.0, 10.0: 57.0, 16.0: 76.0, 25.0: 101.0, 35.0: 125.0, 50.0: 151.0}
        escolhido, cap = None, 0
        for s, a in tabela.items():
            if a >= corrente_projeto:
                escolhido, cap = s, a
                break
        st.divider()
        if escolhido:
            c1, c2 = st.columns(2)
            c1.success(f"✅ Cabo Mínimo: **{escolhido} mm²**")
            c2.info(f"Suporta até: **{cap} A**")
        else:
            st.error("⚠️ Corrente muito alta para cabos comuns (até 50mm²).")

# =========================================================
# MÓDULO 4: QUEDA DE TENSÃO (CALCULA O CONDUTOR)
# =========================================================
elif menu == "4. Dimensionamento por Queda de Tensão":
    st.header("📉 4. Dimensionamento por Distância")
    st.markdown("O sistema buscará o cabo mais fino que mantém a queda de tensão abaixo do limite (geralmente 4%).")
    
    c1, c2 = st.columns(2)
    with c1:
        sistema = st.radio("Sistema:", ["Monofásico (Fase+Neutro)", "Trifásico"])
        tensao = st.selectbox("Tensão Nominal (V):", [127, 220, 380, 440])
        distancia = st.number_input("Distância (metros):", min_value=1.0, step=1.0)
    
    with c2:
        corrente_carga = st.number_input("Corrente da Carga (A):", min_value=0.1, step=0.1)
        limite_queda = st.number_input("Limite Máximo de Queda (%):", value=4.0, step=0.5)
        mat = st.selectbox("Material:", ["Cobre", "Alumínio"])

    if st.button("Calcular Cabo Ideal", type="primary"):
        # Definição de constantes
        rho = 0.0172 if mat == "Cobre" else 0.0282
        fator = 2 if "Monofásico" in sistema else 1.73205
        
        # Lista de cabos comerciais para testar (mm²)
        cabos_comerciais = [1.5, 2.5, 4.0, 6.0, 10.0, 16.0, 25.0, 35.0, 50.0, 70.0, 95.0, 120.0]
        
        cabo_ideal = None
        queda_final_perc = 0
        tensao_final_carga = 0
        
        # --- LOOP DE DIMENSIONAMENTO ---
        # Testa cada cabo, do menor para o maior, até achar um que sirva
        for secao in cabos_comerciais:
            # Fórmula: Queda(V) = (Fator * Rho * L * I) / S
            queda_volts = (fator * rho * distancia * corrente_carga) / secao
            queda_perc = (queda_volts / tensao) * 100
            
            if queda_perc <= limite_queda:
                cabo_ideal = secao
                queda_final_perc = queda_perc
                tensao_final_carga = tensao - queda_volts
                break # Encontrou! Para o loop.
        
        st.markdown("---")
        
        if cabo_ideal:
            st.success(f"✅ Cabo Recomendado pela Distância: **{cabo_ideal} mm²**")
            
            col_res1, col_res2 = st.columns(2)
            col_res1.metric("Queda Calculada", f"{queda_final_perc:.2f} %")
            col_res2.metric("Tensão na Carga", f"{tensao_final_carga:.2f} V")
            
            if queda_final_perc > 3.0:
                st.warning("⚠️ Nota: O cabo está no limite. Considere usar um tamanho acima se houver previsão de aumento de carga.")
        else:
            st.error("❌ A distância é muito grande! Mesmo um cabo de 120mm² não atende ao limite estipulado.")

# =========================================================
# MÓDULO 5: CONTA DE LUZ
# =========================================================
elif menu == "5. Simulador de Conta de Luz":
    st.header("💸 5. Simulador de Custo de Energia")
    
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
