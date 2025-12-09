import streamlit as st
import math

# Configuração da Página
st.set_page_config(page_title="Calculadora Elétrica Pro", page_icon="⚡")

st.title("⚡ Sistema de Cálculo Elétrico")
st.write("Selecione a ferramenta desejada no menu lateral.")

# --- BARRA LATERAL (MENU) ---
menu = st.sidebar.selectbox(
    "Escolha a Ferramenta",
    ["Lei de Ohm & Potência", "Dimensionamento de Cabos"]
)

# --- MÓDULO 1: LEI DE OHM ---
if menu == "Lei de Ohm & Potência":
    st.header("1. Lei de Ohm e Potência")
    st.info("Deixe 0 nos valores que você NÃO tem. Preencha apenas dois campos.")

    col1, col2 = st.columns(2)
    
    with col1:
        v = st.number_input("Tensão (Volts)", min_value=0.0, step=0.1)
        i = st.number_input("Corrente (Amperes)", min_value=0.0, step=0.1)
    
    with col2:
        r = st.number_input("Resistência (Ohms)", min_value=0.0, step=0.1)
        p = st.number_input("Potência (Watts)", min_value=0.0, step=0.1)

    if st.button("Calcular Ohm"):
        # Lógica para descobrir qual par de valores foi preenchido
        # Nota: Esta é uma lógica simplificada para o exemplo web
        try:
            if v > 0 and i > 0: # Tem V e I
                r = v / i
                p = v * i
                st.success(f"Calculado! Resistência: {r:.2f} Ω | Potência: {p:.2f} W")
            
            elif v > 0 and r > 0: # Tem V e R
                i = v / r
                p = (v**2) / r
                st.success(f"Calculado! Corrente: {i:.2f} A | Potência: {p:.2f} W")
                
            elif v > 0 and p > 0: # Tem V e P
                i = p / v
                r = (v**2) / p
                st.success(f"Calculado! Corrente: {i:.2f} A | Resistência: {r:.2f} Ω")

            elif i > 0 and r > 0: # Tem I e R
                v = r * i
                p = r * (i**2)
                st.success(f"Calculado! Tensão: {v:.2f} V | Potência: {p:.2f} W")
                
            elif i > 0 and p > 0: # Tem I e P
                v = p / i
                r = p / (i**2)
                st.success(f"Calculado! Tensão: {v:.2f} V | Resistência: {r:.2f} Ω")
                
            elif r > 0 and p > 0: # Tem R e P
                v = math.sqrt(p * r)
                i = math.sqrt(p / r)
                st.success(f"Calculado! Tensão: {v:.2f} V | Corrente: {i:.2f} A")
            
            else:
                st.warning("Por favor, preencha exatamente dois campos maiores que zero.")
                
        except ZeroDivisionError:
            st.error("Erro: Divisão por zero.")

# --- MÓDULO 2: CABOS ---
elif menu == "Dimensionamento de Cabos":
    st.header("2. Dimensionamento de Cabos (PVC/Alvenaria)")
    
    corrente_projeto = st.number_input("Digite a Corrente de Projeto (A):", min_value=0.0, step=0.1)
    
    if st.button("Buscar Cabo"):
        # Tabela NBR 5410 simplificada
        tabela_cabos = {
            1.5: 17.5, 2.5: 24.0, 4.0: 32.0, 6.0: 41.0,
            10.0: 57.0, 16.0: 76.0, 25.0: 101.0, 35.0: 125.0, 50.0: 151.0
        }
        
        cabo_selecionado = None
        capacidade = 0
        
        for secao, ampacidade in tabela_cabos.items():
            if ampacidade >= corrente_projeto:
                cabo_selecionado = secao
                capacidade = ampacidade
                break
        
        if cabo_selecionado:
            st.success(f"✅ Cabo Recomendado: {cabo_selecionado} mm²")
            st.write(f"Capacidade máxima suportada: **{capacidade} A**")
        else:
            st.error("⚠️ Corrente muito alta para a tabela padrão (acima de 150A).")

# Rodapé
st.markdown("---")
st.caption("Desenvolvido com Python e Streamlit")
