import streamlit as st
import math

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Calc. Eletricista - Prof. Manoel", page_icon="⚡", layout="centered")

# --- ESTILO CSS PERSONALIZADO (OPCIONAL - PARA DAR DESTAQUE) ---
st.markdown("""
    <style>
    .big-font { font-size:20px !important; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

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
# MÓDULO 1: 1ª LEI DE OHM & POTÊNCIA (Melhorado)
# =========================================================
if menu == "1. Lei de Ohm & Potência (1ª Lei)":
    st.header("🔌 1ª Lei de Ohm e Potência")
    st.markdown("Preencha **dois valores** conhecidos para descobrir os outros dois.")
    
    # Layout em colunas para input
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
                # Variável para guardar qual fórmula foi usada (para mostrar ao aluno)
                formula_usada = ""
                
                # Lógica de Cálculo
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
                
                # Exibição das Fórmulas Didáticas
                st.markdown("##### 📝 Fórmulas Aplicadas:")
                st.latex(formula_usada)
                
                # Exibição dos Valores
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Tensão (V)", f"{v:.2f} V")
                c2.metric("Corrente (I)", f"{i:.2f} A")
                c3.metric("Resistência (R)", f"{r:.2f} Ω")
                c4.metric("Potência (P)", f"{p:.2f} W")

        except ZeroDivisionError: 
            st.error("Erro Matemático: Divisão por zero detectada.")

# =========================================================
# MÓDULO 2: 2ª LEI DE OHM (Melhorado)
# =========================================================
elif menu == "2. Resistividade (2ª Lei de Ohm)":
    st.header("📏 2ª Lei de Ohm (Resistência do Fio)")
    
    # Explicação didática com LaTeX
    st.markdown("""
    A resistência elétrica de um condutor depende do material ($\rho$), do comprimento ($L$) e da área da seção transversal ($A$).
    """)
    st.latex(r"R = \frac{\rho \cdot L}{A}")
    
    col_input, col_ref = st.columns([1.5, 1])
    
    with col_input:
        material = st.selectbox("Selecione o Material:", ["Cobre", "Alumínio", "Ouro", "Prata"])
        comprimento = st.number_input("Comprimento do condutor (metros):", min_value=0.0, step=1.0)
        secao = st.number_input("Seção Transversal / Bitola (mm²):", min_value=0.0, step=0.5, value=2.5)
    
    with col_ref:
        st.markdown("##### 📋 Tabela de Resistividade")
        # Dicionário expandido de materiais
        materiais = {
            "Cobre": 0.0172,
            "Alumínio": 0.0282,
            "Ouro": 0.0244,
            "Prata": 0.0159
        }
        rho = materiais[material]
        
        st.caption(f"Valor usado para **{material}**:")
        st.metric(label="Resistividade (ρ)", value=f"{rho}", delta="Ω.mm²/m", delta_color="off")
        
        with st.expander("Ver todos os valores"):
            st.write(materiais)

    if st.button("Calcular Resistência"):
        if secao > 0:
            resistencia_fio = (rho * comprimento) / secao
            
            st.markdown("---")
            st.success("✅ Cálculo Finalizado")
            
            # Resultado com destaque
            col_res1, col_res2 = st.columns(2)
            col_res1.metric("Resistência Total do Fio", f"{resistencia_fio:.4f} Ω")
            
            # Feature didática: Queda de Tensão Estimada (Bônus)
            st.info("💡 Curiosidade didática:")
            st.markdown(f"Se passar uma corrente de **10A** neste fio, você perderá **{resistencia_fio * 10:.2f} Volts** só no caminho.")
            
        else:
            st.error("A seção (bitola) não pode ser zero.")

# =========================================================
# MÓDULO 3: CABOS (Mantido e Organizado)
# =========================================================
elif menu == "3. Dimensionamento de Cabos":
    st.header("elementos 3. Dimensionamento de Condutores")
    st.caption("Critério de Capacidade de Corrente (Ampacidade) - NBR 5410 | Ref: Método B1 (Eletroduto em alvenaria), PVC, 2 condutores carregados.")
    
    corrente_projeto = st.number_input("Corrente de Projeto (A):", min_value=0.0, step=0.1)
    
    if st.button("Dimensionar Cabo"):
        # Tabela simplificada
        tabela = {1.5: 17.5, 2.5: 24.0, 4.0: 32.0, 6.0: 41.0, 10.0: 57.0, 16.0: 76.0, 25.0: 101.0, 35.0: 125.0, 50.0: 151.0}
        
        escolhido = None
        cap = 0
        
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
            st.error("⚠️ Corrente muito alta para cabos comuns (até 50mm²) nesta tabela simplificada.")

# =========================================================
# MÓDULO 4: CONTA DE LUZ (Mantido e Organizado)
# =========================================================
elif menu == "4. Simulador de Conta de Luz":
    st.header("💸 4. Simulador de Custo de Energia")
    
    c1, c2 = st.columns(2)
    with c1:
        w = st.number_input("Potência do Aparelho (Watts):", step=10.0, help="Olhe na etiqueta atrás do aparelho")
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
        
        st.caption(f"Memória de Cálculo: ({w}W x {h}h x {d}d) ÷ 1000 = {kwh} kWh")

# --- RODAPÉ ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>© 2025 - Prof. Manoel Mendes | Ferramenta Educacional</div>", unsafe_allow_html=True)
