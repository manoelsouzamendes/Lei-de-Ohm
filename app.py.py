import streamlit as st
import math

# --- CONFIGURAÇÃO DA PÁGINA ---
# O título da aba do navegador também foi atualizado
st.set_page_config(page_title="Calc. Eletricista - Prof. Manoel", page_icon="⚡")

# --- CABEÇALHO PERSONALIZADO ---
st.title("⚡ Calculadora do Eletricista")
st.subheader("Desenvolvido por Prof. Manoel Mendes")
st.markdown("---") # Linha divisória visual
st.write("Bem-vindo! Selecione a ferramenta desejada no menu lateral (canto esquerdo).")

# --- BARRA LATERAL (MENU) ---
menu = st.sidebar.selectbox(
    "Escolha a Ferramenta",
    ["Lei de Ohm & Potência", "Dimensionamento de Cabos"]
)
st.sidebar.markdown("---")
st.sidebar.caption("Ferramenta de apoio didático.")

# --- MÓDULO 1: LEI DE OHM ---
if menu == "Lei de Ohm & Potência":
    st.header("1. Lei de Ohm e Potência")
    st.info("💡 Instrução: Deixe 0 nos valores que você NÃO tem. Preencha apenas dois campos.")

    col1, col2 = st.columns(2)
    
    with col1:
        v = st.number_input("Tensão (Volts)", min_value=0.0, step=0.1, format="%.2f")
        i = st.number_input("Corrente (Amperes)", min_value=0.0, step=0.1, format="%.2f")
    
    with col2:
        r = st.number_input("Resistência (Ohms)", min_value=0.0, step=0.1, format="%.2f")
        p = st.number_input("Potência (Watts)", min_value=0.0, step=0.1, format="%.2f")

    if st.button("Calcular Agora"):
        try:
            # Validação: Verifica se exatamente 2 campos foram preenchidos
            inputs = [v > 0, i > 0, r > 0, p > 0]
            
            if sum(inputs) != 2:
                 st.warning("⚠️ Atenção: Por favor, preencha exatamente dois campos com valores maiores que zero.")
            else:
                # Lógica de Cálculo
                if v > 0 and i > 0: # Tem V e I
                    r = v / i
                    p = v * i
                elif v > 0 and r > 0: # Tem V e R
                    i = v / r
                    p = (v**2) / r
                elif v > 0 and p > 0: # Tem V e P
                    i = p / v
                    r = (v**2) / p
                elif i > 0 and r > 0: # Tem I e R
                    v = r * i
                    p = r * (i**2)
                elif i > 0 and p > 0: # Tem I e P
                    v = p / i
                    r = p / (i**2)
                elif r > 0 and p > 0: # Tem R e P
                    v = math.sqrt(p * r)
                    i = math.sqrt(p / r)
                
                # Exibição dos Resultados (Visual Moderno)
                st.success("✅ Cálculo realizado com sucesso!")
                
                # Cria 4 colunas para mostrar os resultados lado a lado
                res1, res2, res3, res4 = st.columns(4)
                res1.metric("Tensão (V)", f"{v:.2f} V")
                res2.metric("Corrente (I)", f"{i:.2f} A")
                res3.metric("Resistência (R)", f"{r:.2f} Ω")
                res4.metric("Potência (P)", f"{p:.2f} W")
                
        except ZeroDivisionError:
            st.error("Erro Matemático: Divisão por zero.")

# --- MÓDULO 2: CABOS ---
elif menu == "Dimensionamento de Cabos":
    st.header("2. Dimensionamento de Cabos")
    st.caption("Baseado na NBR 5410 (Cobre, PVC, Instalação B1 - Eletroduto em Alvenaria)")
    
    corrente_projeto = st.number_input("Digite a Corrente de Projeto (A):", min_value=0.0, step=0.1)
    
    if st.button("Buscar Cabo Ideal"):
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
            st.info(f"Este cabo suporta até **{capacidade} A** na instalação B1 (2 condutores carregados).")
        else:
            st.error("⚠️ Corrente muito alta para a tabela padrão (acima de 150A).")

# --- RODAPÉ ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey;'>"
    "© 2025 - Desenvolvido por <b>Prof. Manoel Mendes</b><br>"
    "Ferramenta para fins didáticos"
    "</div>", 
    unsafe_allow_html=True
)
