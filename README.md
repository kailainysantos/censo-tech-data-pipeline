# 📊 Censo Tech Analytics: Pipeline de Dados Educacionais

![Badge Status](http://img.shields.io/static/v1?label=STATUS&message=CONCLUIDO&color=GREEN&style=for-the-badge)
![Badge Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Badge DuckDB](https://img.shields.io/badge/Engine-DuckDB-yellow?style=for-the-badge&logo=duckdb)
![Badge ETL](https://img.shields.io/badge/Pipeline-ETL-orange?style=for-the-badge)

> **Projeto de Engenharia de Dados** desenvolvido para processamento e análise de microdados públicos do INEP (Censo da Educação Superior 2023), focado em resolver problemas de Big Data Local e otimização de memória.

---

## 📑 Índice
- [Sobre o Projeto](#-sobre-o-projeto)
- [O Desafio Técnico](#-o-desafio-técnico)
- [Arquitetura da Solução](#-arquitetura-da-solução)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Roadmap do Projeto](#-roadmap-do-projeto)
- [Resultados e Visualização](#-resultados-e-visualização)
- [Como Executar](#-como-executar)
- [Autor](#-autor)

---

## 🧐 Sobre o Projeto

O **Censo Tech Analytics** é uma solução de *Data Engineering* criada para mapear o cenário da educação superior em Tecnologia no Brasil. O projeto ingere dados reais e brutos do governo para responder questões de negócio sobre a oferta de cursos (Engenharia de Dados, Ciência da Computação, SI) e a predominância do ensino privado versus público.

Os dados utilizados são oficiais, provenientes do [Portal de Dados Abertos do INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior).

---

## ⚡ O Desafio Técnico

Os arquivos de microdados do Censo (dataset `MICRODADOS_CADASTRO_CURSOS`) possuem estrutura complexa e alta volumetria.
A abordagem tradicional de carregar todo o dataset em memória (ex: Pandas puro `read_csv`) em hardware convencional (Notebook i5, 12GB RAM) é inviável para processamento ágil.

**A Solução:** Implementação de um pipeline **ELT** baseado no **DuckDB**, um motor SQL OLAP embutido que permite:
1.  **Processamento Out-of-Core:** Manipulação de dados maiores que a RAM disponível.
2.  **Streaming de Dados:** Leitura otimizada do CSV bruto sem carga total.
3.  **Alta Performance:** Execução de queries analíticas vetorizadas em segundos.

---

## 🛠 Arquitetura da Solução

O pipeline segue o padrão **ETL (Extract, Transform, Load)**:

1.  **Extract (Ingestão):** Conexão direta com o arquivo CSV bruto via DuckDB.
2.  **Transform (Processamento):**
    * Filtragem de cursos alvo via `SQL` (`ILIKE`).
    * Normalização de dados categóricos (De-para: Pública/Privada).
    * Agregação de métricas (Soma de matrículas, Contagem de ofertas).
3.  **Load & Viz (Entrega):**
    * Exportação dos dados refinados para `.csv`.
    * Geração automática de visualização gráfica estática com `Matplotlib`.

### Query Principal (DuckDB)
```sql
SELECT 
    NO_CINE_ROTULO as Nome_Curso,
    CASE WHEN TP_REDE = 1 THEN 'Pública' ELSE 'Privada' END as Tipo_Faculdade,
    SUM(QT_MAT) as Total_Alunos
FROM read_csv('dados/MICRODADOS_CADASTRO_CURSOS_2023.CSV', auto_detect=True, encoding='latin-1')
WHERE NO_CINE_ROTULO ILIKE '%Engenharia de Dados%'
GROUP BY Nome_Curso, Tipo_Faculdade
ORDER BY Total_Alunos DESC
