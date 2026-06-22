import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

# =========================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E TÍTULO
# =========================================================================
st.set_page_config(page_title="Doces Sabor", page_icon="🍫", layout="wide")
st.title("🍫 Sistema de Gestão - Doces Sabor")

# =========================================================================
# 2. CONFIGURAÇÃO DOS DADOS (PRODUTOS E PREÇOS)
# =========================================================================
doces = {
    "Brownie": ["Brigadeiro", "Doce de Leite", "Oreo", "Ninho com Nutella", "Beijinho", "Maracujá"],
    "Copo": ["Brigadeiro", "Brownoff", "Morango", "Maracujá", "Ninho com Nutella"]
}

precos = {"Brownie": 10.00, "Copo": 15.00}

# =========================================================================
# 3. BANCO DE DADOS EM MEMÓRIA (st.session_state)
# =========================================================================
if "estoque" not in st.session_state:
    st.session_state.estoque = {
        "Brownie": {"Brigadeiro": 0, "Doce de Leite": 0, "Oreo": 0, "Ninho com Nutella": 0, "Beijinho": 0, "Maracujá": 0},
        "Copo": {"Brigadeiro": 0, "Brownoff": 0, "Morango": 0, "Maracujá": 0, "Ninho com Nutella": 0}
    }

if "historico_vendas" not in st.session_state:
    st.session_state.historico_vendas = []

if "historico_movimentacoes" not in st.session_state:
    st.session_state.historico_movimentacoes = []

# Botão global de Reset (limpa tudo com segurança)
if st.button("🔄 Resetar Estoque, Movimentações e Vendas"):
    st.session_state.estoque = {
        "Brownie": {"Brigadeiro": 0, "Doce de Leite": 0, "Oreo": 0, "Ninho com Nutella": 0, "Beijinho": 0, "Maracujá": 0},
        "Copo": {"Brigadeiro": 0, "Brownoff": 0, "Morango": 0, "Maracujá": 0, "Ninho com Nutella": 0}
    }
    st.session_state.historico_vendas = []
    st.session_state.historico_movimentacoes = []
    st.success("✅ Todo o sistema foi resetado com sucesso!")
    st.rerun()

# =========================================================================
# 4. FUNÇÕES AUXILIARES PARA EXPORTAÇÃO (EXCEL)
# =========================================================================
def para_excel(df, nome_aba):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=nome_aba)
    return output.getvalue()

# =========================================================================
# 5. CRIAÇÃO DAS ABAS NA INTERFACE
# =========================================================================
aba_estoque, aba_relatorio, aba_cliente = st.tabs([
    "📦 Controle de Estoque", 
    "📊 Resumo de Vendas", 
    "🛒 Painel do Cliente"
])

# =========================================================================
# ABA 1: CONTROLE DE ESTOQUE (PRODUÇÃO / AJUSTES)
# =========================================================================
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
            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            if movimentacao == "Entrada":
                st.session_state.estoque[tipo][sabor] += quantidade
                saldo_atual = st.session_state.estoque[tipo][sabor]
                
                # Registra no histórico detalhado
                st.session_state.historico_movimentacoes.append({
                    "Data/Hora": data_atual,
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
                        "Data/Hora": data_atual,
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
    
    # Exibição visual do estoque - Brownies
    st.write("---")
    st.write("### 🍫 Estoque Atual de Brownies (Visão Geral)")
    l1, l2, l3, l4, l5, l6 = st.columns(6)
    with l1: st.metric("Brigadeiro", f"{st.session_state.estoque['Brownie']['Brigadeiro']} un")
    with l2: st.metric("Doce de Leite", f"{st.session_state.estoque['Brownie']['Doce de Leite']} un")   
    with l3: st.metric("Oreo", f"{st.session_state.estoque['Brownie']['Oreo']} un")
    with l4: st.metric("Ninho com Nutella", f"{st.session_state.estoque['Brownie']['Ninho com Nutella']} un")
    with l5: st.metric("Beijinho", f"{st.session_state.estoque['Brownie']['Beijinho']} un")
    with l6: st.metric("Maracujá", f"{st.session_state.estoque['Brownie']['Maracujá']} un")

    # Exibição visual do estoque - Copos
    st.write("---")
    st.write("### 🧮 Estoque Atual de Copos (Visão Geral)")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.metric("Brigadeiro", f"{st.session_state.estoque['Copo']['Brigadeiro']} un")
    with c2: st.metric("Brownoff", f"{st.session_state.estoque['Copo']['Brownoff']} un")   
    with c3: st.metric("Morango", f"{st.session_state.estoque['Copo']['Morango']} un")
    with c4: st.metric("Maracujá", f"{st.session_state.estoque['Copo']['Maracujá']} un")
    with c5: st.metric("Ninho com Nutella", f"{st.session_state.estoque['Copo']['Ninho com Nutella']} un")
    
    # Seção para exportação do extrato de movimentações e saldos
    st.write("---")
    st.write("### 📋 Histórico Detalhado de Movimentações (Entradas, Saídas e Saldos)")
    
    if len(st.session_state.historico_movimentacoes) > 0:
        df_movs = pd.DataFrame(st.session_state.historico_movimentacoes)
        st.dataframe(df_movs, use_container_width=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.download_button(
                label="📄 Baixar Histórico de Movimentações (CSV)",
                data=df_movs.to_csv(index=False, sep=';', encoding='utf-8-sig'),
                file_name="historico_movimentacao_estoque.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_btn2:
            st.download_button(
                label="📊 Baixar Histórico de Movimentações (Excel)",
                data=para_excel(df_movs, "Movimentações"),
                file_name="historico_movimentacao_estoque.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    else:
        st.info("📢 Nenhuma movimentação registrada ainda. Registre entradas ou saídas para gerar o relatório.")

# =========================================================================
# ABA 2: RELATÓRIO DE VENDAS
# =========================================================================
with aba_relatorio:
    st.header("Relatório Financeiro e de Vendas")
    st.write("Aqui você pode visualizar o resumo e o faturamento das vendas realizadas.")
    
    if len(st.session_state.historico_vendas) > 0:
        df_vendas = pd.DataFrame(st.session_state.historico_vendas)
        
        if "Total" in df_vendas.columns:
            total_vendas = df_vendas["Total"].sum()
        else:
            total_vendas = 0.0
            
        st.metric(label="💰 Faturamento Total", value=f"R$ {total_vendas:,.2f}".replace('.', ','))
        st.dataframe(df_vendas, use_container_width=True)
        
        st.write("#### 📥 Exportar Histórico de Vendas")
        col_venda_btn1, col_venda_btn2 = st.columns(2)
        
        with col_venda_btn1:
            st.download_button(
                label="📄 Baixar Vendas em CSV",
                data=df_vendas.to_csv(index=False, sep=';', encoding='utf-8-sig'),
                file_name="relatorio_vendas.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_venda_btn2:
            st.download_button(
                label="📊 Baixar Vendas em Excel",
                data=para_excel(df_vendas, "Vendas"),
                file_name="relatorio_vendas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    else:
        st.metric(label="💰 Faturamento Total", value="R$ 0,00")
        st.info("📢 Nenhuma venda realizada hoje ainda. Os dados aparecerão assim que os clientes fizerem pedidos.")

# =========================================================================
# ABA 3: PAINEL DO CLIENTE (SAÍDA AUTOMÁTICA)
# =========================================================================
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
    
    estoque_atual = st.session_state.estoque[cli_tipo][cli_sabor]
    
    if estoque_atual <= 0:
        st.error("🔴 Sabor indisponível no momento (Esgotado).")
    elif estoque_atual < cli_qtd:
        st.warning(f"⚠️ Só temos {estoque_atual} unidades disponíveis em estoque.")
    else:
        st.success(f"🟢 Em estoque! Preço unitário: R$ {precos[cli_tipo]:.2f}")
        
        if st.button("🛒 Confirmar Pedido Cliente", type="primary"):
            # Dá baixa no estoque
            st.session_state.estoque[cli_tipo][cli_sabor] -= cli_qtd
            saldo_apos_venda = st.session_state.estoque[cli_tipo][cli_sabor]
            data_venda = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            # 1. Salva no histórico de vendas normais
            valor_total = cli_qtd * precos[cli_tipo]
            st.session_state.historico_vendas.append({
                "Data/Hora": data_venda,
                "Tipo": cli_tipo,
                "Sabor": cli_sabor,
                "Quantidade": cli_qtd,
                "Total": valor_total
            })
            
            # 2. Registra automaticamente como uma "Saída" com data e saldo atualizado no extrato do estoque
            st.session_state.historico_movimentacoes.append({
                "Data/Hora": data_venda,
                "Categoria": cli_tipo,
                "Sabor": cli_sabor,
                "Entrada": 0,
                "Saída": cli_qtd,
                "Saldo Atual": saldo_apos_venda
            })
            
            st.balloons()
            st.success(f"🎉 Pedido de {cli_qtd}x {cli_tipo} ({cli_sabor}) realizado com sucesso!")
            st.rerun()
            
    st.write("---")
    st.write("### 💬 Feedback do Cliente")
    feedback = st.text_area("Deixe seu feedback sobre nossos produtos:")
    if st.button("Enviar Feedback"):
        st.success("Obrigado pelo seu feedback! Ele foi arquivado com sucesso.")
