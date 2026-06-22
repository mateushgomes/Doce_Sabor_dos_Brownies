import streamlit as st
import pandas as pd

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
# Isso impede que o Streamlit resete os valores quando um botão for clicado.
# =========================================================================
if "estoque" not in st.session_state:
    st.session_state.estoque = {
        "Brownie": {"Brigadeiro": 0, "Doce de Leite": 0, "Oreo": 0, "Ninho com Nutella": 0, "Beijinho": 0, "Maracujá": 0},
        "Copo": {"Brigadeiro": 0, "Brownoff": 0, "Morango": 0, "Maracujá": 0, "Ninho com Nutella": 0}
    }

if "historico_vendas" not in st.session_state:
    st.session_state.historico_vendas = []

# Botão para resetar o estoque e o histórico de vendas
if st.button("🔄 Resetar Estoque e Histórico de Vendas"):
    st.session_state.estoque = {
        "Brownie": {"Brigadeiro": 0, "Doce de Leite": 0, "Oreo": 0, "Ninho com Nutella": 0, "Beijinho": 0, "Maracujá": 0},
        "Copo": {"Brigadeiro": 0, "Brownoff": 0, "Morango": 0, "Maracujá": 0, "Ninho com Nutella": 0}
    }
    st.session_state.historico_vendas = []
    st.success("✅ Estoque e histórico de vendas resetados com sucesso!")

# Tabela de preços para calcular o financeiro automaticamente
precos = {"Brownie": 10.00, "Copo": 15.00  }

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
            # Lógica de somar ou subtrair do estoque central
            if movimentacao == "Entrada":
                st.session_state.estoque[tipo][sabor] += quantidade
                st.success(f"✅ Adicionado(a) {quantidade} unidades de {tipo} ({sabor}) ao estoque!")
            else:
                if st.session_state.estoque[tipo][sabor] >= quantidade:
                    st.session_state.estoque[tipo][sabor] -= quantidade
                    st.success(f"📉 Removido(a) {quantidade} unidades de {tipo} ({sabor}) do estoque!")
                else:
                    st.error("❌ Estoque insuficiente para realizar essa saída!")
    
    # Exibição do painel visual AUTOMÁTICO do estoque atual de Brownies
    st.write("---")
    st.write("### 🧮 Estoque Atual de Brownies (Visão Geral)")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: st.metric("Brigadeiro", f"{st.session_state.estoque['Brownie']['Brigadeiro']} un")
    with c2: st.metric("Doce de Leite", f"{st.session_state.estoque['Brownie']['Doce de Leite']} un")   
    with c3: st.metric("Oreo", f"{st.session_state.estoque['Brownie']['Oreo']} un")
    with c4: st.metric("Ninho com Nutella", f"{st.session_state.estoque['Brownie']['Ninho com Nutella']} un")
    with c5: st.metric("Beijinho", f"{st.session_state.estoque['Brownie']['Beijinho']} un")
    with c6: st.metric("Maracujá", f"{st.session_state.estoque['Brownie']['Maracujá']} un")

    st.write("---")
    st.write("### 🧮 Estoque Atual de Copos (Visão Geral)")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.metric("Brigadeiro", f"{st.session_state.estoque['Copo']['Brigadeiro']} un")
    with c2: st.metric("Brownoff", f"{st.session_state.estoque['Copo']['Brownoff']} un")   
    with c3: st.metric("Morango", f"{st.session_state.estoque['Copo']['Morango']} un")
    with c4: st.metric("Maracujá", f"{st.session_state.estoque['Copo']['Maracujá']} un")
    with c5: st.metric("Ninho com Nutella", f"{st.session_state.estoque['Copo']['Ninho com Nutella']} un")
        
## ========= ABA 2: RELATÓRIO DE VENDAS =========
with aba_relatorio:
    st.header("Relatório de Vendas")
    st.write("Aqui você pode visualizar o resumo das vendas realizadas.")
    
    # Verifica se há dados no histórico
    if len(st.session_state.historico_vendas) > 0:
        df_vendas = pd.DataFrame(st.session_state.historico_vendas)
        
        # Correção segura: só soma se a coluna "Total" existir no DataFrame
        if "Total" in df_vendas.columns:
            total_vendas = df_vendas["Total"].sum()
        else:
            total_vendas = 0.0
            
        st.metric(label="💰 Faturamento Total", value=f"R$ {total_vendas:,.2f}".replace('.', ','))
        st.dataframe(df_vendas, use_container_width=True)
    else:
        st.metric(label="💰 Faturamento Total", value="R$ 0,00")
        st.info("📢 Nenhuma venda realizada hoje ainda. Os dados aparecerão aqui assim que os clientes fizerem os pedidos!")

# Botão para exportar o relatório de vendas para CSV
    if st.button("📥 Exportar Relatório de Vendas para CSV"):
        if len(st.session_state.historico_vendas) > 0:
            df_vendas.to_csv("relatorio_vendas.csv", index=False)
            st.success("✅ Relatório exportado com sucesso! O arquivo 'relatorio_vendas.csv' foi gerado.")
        else:
            st.warning("⚠️ Nenhuma venda realizada para exportar.")

## ========= ABA 3: PAINEL DO CLIENTE (SAÍDA AUTOMÁTICA) =========
with aba_cliente:
    st.header("Painel do Cliente")
    st.write("Faça o seu pedido aqui:")
    
    col_cli_tipo, col_cli_sabor, col_cli_qtd = st.columns(3)
    
    with col_cli_tipo:
        cli_tipo = st.selectbox("Escolha a categoria:", list(doces.keys()), key="cli_tipo")
    with col_cli_sabor:
        cli_sabor = st.selectbox("Escolha o sabor:", doces[cli_tipo], key="cli_sabor")
    with col_cli_qtd:
        cli_qtd = st.number_input("Quantidade desejada:", min_value=1, value=1, key="cli_qtd")
    
    # Verifica a disponibilidade real em estoque
    estoque_atual = st.session_state.estoque[cli_tipo][cli_sabor]
    
    if estoque_atual <= 0:
        st.error("🔴 Sabor indisponível no momento (Esgotado).")
    elif estoque_atual < cli_qtd:
        st.warning(f"⚠️ Só temos {estoque_atual} unidades disponíveis em estoque.")
    else:
        st.success(f"🟢 Em estoque! Preço unitário: R$ {precos[cli_tipo]:.2f}")
        
        if st.button("🛒 Confirmar Pedido Cliente", type="primary"):
            # 1. Subtrai do estoque
            st.session_state.estoque[cli_tipo][cli_sabor] -= cli_qtd
            
            # 2. Calcula valor total e salva no histórico de vendas (Pandas)
            valor_total = cli_qtd * precos[cli_tipo]
            nova_venda = {
                "Data": "2026-06-22", # Data atual simulada
                "Tipo": cli_tipo,
                "Sabor": cli_sabor,
                "Quantidade": cli_qtd,
                "Total": valor_total
            }
            st.session_state.historico_vendas.append(nova_venda)
            
            st.balloons() # Efeito de comemoração na tela!
            st.success(f"🎉 Pedido realizado com sucesso! {cli_qtd}x {cli_tipo} de {cli_sabor} decolaram para o cliente.")
            
    # Seção de feedback do cliente
    st.write("---")
    st.write("### 💬 Feedback do Cliente")
    feedback = st.text_area("Deixe seu feedback sobre nossos produtos:")
    if st.button("Enviar Feedback"):
        st.success("Obrigado pelo seu feedback! Ele foi enviado para a gerência.")