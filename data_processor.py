import pandas as pd
from typing import List, Dict

def clean_numeric_value(value):
    """Limpa a formatação de moeda do tipo numérico do brasil para o padrão Float."""
    if isinstance(value, str):
        cleaned_value = value.replace('.', '').replace(',', '.')
        try:
            return float(cleaned_value)
        except ValueError:
            return None
    return value

def processar_e_mesclar(df_tabelas: pd.DataFrame, dados_texto: List[Dict]) -> pd.DataFrame:
    """Combina o DataFrame de tabelas capturadas com as variáveis de list/dic capturadas pelo REGEX e faz curadoria nos dados."""
    print("\nIniciando cruzamento e limpeza de dados (Módulo de Processamento)...")
    
    if len(dados_texto) == 0:
        print("Aviso: Nenhum dado de texto recebido. Retornando apenas as tabelas puras.")
        return df_tabelas
    
    extraidos_df = pd.DataFrame(dados_texto)
    extraidos_df_renomeado = extraidos_df.rename(columns={'Reclamante': 'Nome Reclamante'})

    if df_tabelas.empty:
        print("Aviso: Nenhum dado de tabela para merge. Retornando os dados extraídos de texto puros.")
        merged_df = extraidos_df_renomeado
    else:
        # Merge 'left' como era no código original: mantém infos do PDF Tabelado e puxa correlatos.
        merged_df = pd.merge(df_tabelas, extraidos_df_renomeado, on='Nome Reclamante', how='left')

    # Tratar dados numéricos da Consolidação
    if 'Carga Horária (Padrão)' in merged_df.columns:
        merged_df['Carga Horária (Padrão)'] = merged_df['Carga Horária (Padrão)'].apply(clean_numeric_value)
        
    if 'Cálculo' in merged_df.columns:
        merged_df['Cálculo'] = pd.to_numeric(merged_df['Cálculo'], errors='coerce')

    # Cifras da tabela consolidada que precisam virar Float (do Tabula)
    if 'Bruto por Reclamante' in merged_df.columns:
        merged_df['Bruto por Reclamante'] = merged_df['Bruto por Reclamante'].apply(clean_numeric_value)
        
    if 'Líquido por Reclamante' in merged_df.columns:
        merged_df['Líquido por Reclamante'] = merged_df['Líquido por Reclamante'].apply(clean_numeric_value)
        
    if 'Total Devido pelo Reclamado' in merged_df.columns:
        merged_df['Total Devido pelo Reclamado'] = merged_df['Total Devido pelo Reclamado'].apply(clean_numeric_value)
        
    if 'Débitos por Reclamante' in merged_df.columns:
        merged_df['Débitos por Reclamante'] = merged_df['Débitos por Reclamante'].apply(clean_numeric_value)
    
    print("=> Processamento Panda-DataFrames e formatação limpa concluídos.")
    return merged_df
