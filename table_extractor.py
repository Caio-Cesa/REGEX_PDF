import tabula
import pandas as pd

def extrair_tabelas(pdf_path: str) -> pd.DataFrame:
    """Extrai matrizes de dados (tabelas) a partir das páginas do PDF e consolida num único DataFrame."""
    print(f"[{pdf_path}] Iniciando extração de tabelas com Tabula...")
    
    try:
        tabelacomum = tabula.read_pdf(pdf_path, pages='all')
    except Exception as e:
        print(f"Erro ao ler PDF com Tabula: {e}")
        return pd.DataFrame()

    cleaned_tables = []
    
    if len(tabelacomum) > 1:
        reference_columns = tabelacomum[1].columns.tolist()
        cleaned_tables.append(tabelacomum[1])
    else:
        print("Não há tabelas suficientes para processar. Esperado pelo menos index [1].")
        return pd.DataFrame()

    for i in range(2, min(30, len(tabelacomum))):
        table_df = tabelacomum[i]

        if not table_df.empty:
            processed_df = table_df.iloc[1:].copy().reset_index(drop=True)

            if not processed_df.empty and len(processed_df.columns) == len(reference_columns):
                processed_df.columns = reference_columns
                cleaned_tables.append(processed_df)
            elif not processed_df.empty:
                print(f"Aviso: Tabela índice {i} tem número de colunas inconsistente. Tentando reindexar.")
                temp_df = pd.DataFrame(columns=reference_columns)
                for col_idx, col_name in enumerate(reference_columns):
                    if col_idx < len(processed_df.columns):
                        temp_df[col_name] = processed_df.iloc[:, col_idx]
                cleaned_tables.append(temp_df)
            else:
                cleaned_tables.append(pd.DataFrame(columns=reference_columns))
        else:
            cleaned_tables.append(pd.DataFrame(columns=reference_columns))
            
    try:
        final_combined_df = pd.concat(cleaned_tables, ignore_index=True)
        print(f"[{pdf_path}] {len(cleaned_tables)} tabelas consolidadas com sucesso.")
        return final_combined_df
    except Exception as e:
        print(f"Erro ao concatenar tabelas: {e}")
        return pd.DataFrame()
