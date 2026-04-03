import os
from table_extractor import extrair_tabelas
from text_extractor import extrair_dados_texto
from data_processor import processar_e_mesclar

def main():
    print("=" * 60)
    print(" INICIANDO EXTRAÇÃO DE DADOS EM PDF - INTEGRAÇÃO JUDICIAL")
    print("=" * 60)

    tabelas_path = 'dados1.pdf'
    texto_path = 'dados.pdf'
    output_filename = 'Dados_Calculo_Extraidos.xlsx'

    # Verificação de existência
    if not os.path.exists(tabelas_path) or not os.path.exists(texto_path):
        print(f"ERRO: Certifique-se de que '{tabelas_path}' e '{texto_path}' estejam na mesma pasta que o código (aqui na raiz).")
        return

    # Passo 1: Extração das Tabelas Estruturadas via Tabula
    df_tabelas = extrair_tabelas(tabelas_path)

    # Passo 2: Varredura dos Textos Livres usando Regex e PyPDF2
    dados_texto = extrair_dados_texto(texto_path)

    # Passo 3: Cruzamento de dados pelo "Nome Reclamante", Limpeza de Moedas
    resultado_final = processar_e_mesclar(df_tabelas, dados_texto)

    # Passo 4: Salvar em Excel pronto para Banco de Dados/Uso
    try:
        resultado_final.to_excel(output_filename, index=False, engine='openpyxl')
        print(f"\n✅ EXPORTAÇÃO CONCLUÍDA! Resultado: {output_filename}")
        print("\nVisão Estruturada (Head):")
        print(resultado_final.head())
    except Exception as e:
        print(f"ERRO CRÍTICO: Não foi possível salvar salvar o excel. {e}")


if __name__ == "__main__":
    main()
