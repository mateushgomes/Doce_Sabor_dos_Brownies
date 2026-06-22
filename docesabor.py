import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

# 1 Configuração da página e título 
st.set_page_config(page_title="Doces Sabor", page_icon="🍫", layout="wide")
st.title("🍫 Sistema de Gestão - Doces Sabor")

# 2 Criando as categorias de doces e seus respectivos sabores
doces = {
    "Brownie": ["Brigadeiro", "Doce de Leite", "Oreo", "Ninho com Nutella", "Beijinho", "Maracujá"],
    "Copo": ["Brigadeiro", "Brownoff", "Morango", "Maracujá", "Ninho com Nutella"]
}

# =========================================================================
# BANCO DE DADOS EM MEMÓRIA (st.session_state)
# =========================================================================
if "estoque" not in st.session_state:
    st.session_state.estoque = {
        "Brownie": {"Brigadeiro": 0, "Doce de Leite": 0, "Oreo": 0, "Ninho com Nutella": 0, "Beijinho": 0, "Maracujá": 0},
        "Copo": {"Brigadeiro": 0, "Brownoff": 0, "Morango": 0, "Maracujá": 0, "Ninho com Nutella": 0}
    }

if "historico_vendas" not in st.session_state:
    st.session_state.historico_vendas = []

# NOVO: Histórico detalhado de todas as movimentações do estoque
if "historico_movimentacoes" not in st.session_state:
    st.session_state.historico_movimentacoes = []

# Botão para resetar tudo
if st.button("🔄 Resetar Estoque, Movimentações e Vendas"):
    st.session_state.estoque = {
        "Brownie": {"Brigadeiro": 0, "Doce de Leite": 0, "Oreo": 0, "Ninho com Nutella": 0, "Beijinho": 0, "Maracujá": 0},
        "Copo": {"Brigadeiro": 0, "Brownoff": 0, "Morango": 0, "Maracujá": 0, "Ninho com Nutella": 0}
    }
    st.session_state.historico_vendas = []
    st.session_state.historico_movimentacoes = []
    st.success("✅ Todo o sistema foi resetado com sucesso!")

precos = {"Brownie": 10.00, "Copo": 15.00}

# FUNÇÕES AUXILIARES PARA EXPORTAÇÃO
def para_excel(df, nome_aba):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=nome_aba)
    return output.getvalue()

# 3 Criando as abas no streamlit
aba_estoque, aba_relatorio, aba_cliente = st.tabs(["📦 Controle de Estoque", "📊 Resumo de Vendas", "🛒 Painel do Cliente"])

## ========= ABA 1: CONTROLE DE ESTOQUE (PRODUÇÃO / AJUSTES) =========
with aba_estoque:
    st.header("Gerenciamento de Inventário")
   
    with st.container(border=True):
        st.write("### Lançamento de Movimentação")
        st.write("Insira os dados da movimentação do estoque:")
        
        col_tipo, col_doce, col_sabor, col_quantidade = st.columns(4)

        with col_tipo:
            movimentacao = st.selectbox("Tipo de Operação:", ["Entrada", "Saída"])
        with col_doce:
            tipo = st.selectbox("Tipo de Doce:", list(doces.keys()), key="adm_tipo")
        with col_sabor:
            sabor = st.selectbox("Sabor do Doce:", doces[tipo], key="adm_sabor")
        with col_quantidade:
            quantidade = st.number_input("Quantidade:", min_value=1, value=10, key="adm_qtd")
            
        if st.button("Registrar Movimentação", type="primary"):
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if movimentacao == "Entrada":
                st.session_state.estoque[tipo][sabor] += quantidade
                saldo_atual = st.session_state.estoque[tipo][sabor]
                
                # Registra no histórico detalhado
                st.session_state.historico_movimentacoes.append({
                    "Data": data_atual,
                    "Categoria": tipo,
                    "Sabor": sabor,
                    "Entrada": quantidade,
                    "Saída": 0,
                    "Saldo Atual": saldo_atual
                })
                st.success(f"✅ Adicionado(a) {quantidade} unidades de {tipo} ({sabor}) ao estoque!")
                st.rerun()
            else:
                if st.session_state.estoque[tipo][sabor] >= quantidade:
                    st.session_state.estoque[tipo][sabor] -= quantidade
                    saldo_atual = st.session_state.estoque[tipo][sabor]
                    
                    # Registra no histórico detalhado
                    st.session_state.historico_movimentacoes.append({
                        "Data": data_atual,
                        "Categoria": tipo,
                        "Sabor": sabor,
                        "Entrada": 0,
                        "Saída": quantidade,
                        "Saldo Atual": saldo_atual
                    })
                    st.success(f"📉 Removido(a) {quantidade} unidades de {tipo} ({sabor}) do estoque!")
                    st.rerun()
                else:
                    st.error("❌ Estoque insuficiente para realizar essa saída!")
