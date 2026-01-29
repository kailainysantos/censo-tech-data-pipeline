import duckdb
import time

# Nome exato do arquivo que você mostrou no print
arquivo_csv = 'dados/MICRODADOS_CADASTRO_CURSOS_2023.CSV'

print(f"🚀 [ENGENHARIA] Analisando o mercado de cursos de TI...")
print(f"📂 Lendo: {arquivo_csv}")

start_time = time.time()
con = duckdb.connect()

# NO_CINE_ROTULO: Nome padronizado do curso
# QT_MAT: Quantidade de alunos matriculados naquele curso
# TP_REDE: 1 = Pública, 2 = Privada
query = f"""
    SELECT 
        NO_CINE_ROTULO as Nome_Curso,
        CASE 
            WHEN TP_REDE = 1 THEN 'Pública' 
            WHEN TP_REDE = 2 THEN 'Privada'
            ELSE 'Outra' 
        END as Tipo_Faculdade,
        SUM(QT_MAT) as Total_Alunos,
        COUNT(*) as Qtd_Cursos_Ofertados
    FROM read_csv('{arquivo_csv}', sep=';', header=True, auto_detect=True, encoding='latin-1')
    WHERE 
        (NO_CINE_ROTULO ILIKE '%Ciência da Computação%' 
        OR NO_CINE_ROTULO ILIKE '%Sistemas de Informação%'
        OR NO_CINE_ROTULO ILIKE '%Engenharia de Dados%'
        OR NO_CINE_ROTULO ILIKE '%Engenharia de Software%'
        OR NO_CINE_ROTULO ILIKE '%Análise e Desenvolvimento de Sistemas%')
    GROUP BY Nome_Curso, Tipo_Faculdade
    ORDER BY Total_Alunos DESC
"""

# Executa a query
df_resultado = con.execute(query).df()

end_time = time.time()

print("-" * 50)
print(f"✅ Análise de mercado concluída em {end_time - start_time:.2f} segundos!")
print("-" * 50)

# Mostra o Top 10 no terminal
print(df_resultado.head(10))

# Salva o relatório
df_resultado.to_csv('relatorio_mercado_ti.csv', index=False, sep=';', encoding='utf-8')
print(f"\n💾 Relatório salvo como: 'relatorio_mercado_ti.csv'")