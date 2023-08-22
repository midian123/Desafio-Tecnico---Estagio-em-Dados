import pandas as pd

# Carregar os dados das tabelas
perfil_eleitorado = pd.read_csv('perfil_eleitorado_2020.csv', sep=';', encoding='latin1')
sp_turno_1 = pd.read_csv('SP_turno_1.csv', sep=';', encoding='latin1')

# Filtrar dados para o estado de São Paulo (SG_UF = 'SP')
perfil_sp = perfil_eleitorado[perfil_eleitorado['SG_UF'] == 'SP']

# Filtrar dados de CD_MUNICIPIO que fazem parte do estado de São Paulo
cd_municipios_sp = perfil_sp['CD_MUNICIPIO'].unique()
sp_turno_1_sp = sp_turno_1[sp_turno_1['CD_MUNICIPIO'].isin(cd_municipios_sp)]

# Criar uma tabela tratada
tabela_tratada = perfil_sp.merge(sp_turno_1_sp, left_on='CD_MUNICIPIO', right_on='NR_VOTAVEL')

# Selecionar colunas relevantes
colunas_selecionadas = [
    'NM_MUNICIPIO_x', 'DS_GENERO', 'DS_ESTADO_CIVIL', 'DS_FAIXA_ETARIA', 'DS_GRAU_ESCOLARIDADE',
    'NM_VOTAVEL', 'QT_VOTOS'
]
tabela_final = tabela_tratada[colunas_selecionadas]

# Agrupar por município e candidato para encontrar os candidatos mais votados
mais_votados = tabela_final.groupby(['NM_MUNICIPIO_x', 'NM_VOTAVEL'])['QT_VOTOS'].max().reset_index()

# Calcular a média da coluna CD_GRAU_ESCOLARIDADE
media_grau_escolaridade = perfil_sp.groupby('CD_GRAU_ESCOLARIDADE')['DS_GRAU_ESCOLARIDADE'].count().reset_index()
maior_media_repetida = media_grau_escolaridade[media_grau_escolaridade['DS_GRAU_ESCOLARIDADE'] == media_grau_escolaridade['DS_GRAU_ESCOLARIDADE'].max()]

# Dividir os resultados em partes menores e salvar em arquivos separados
part_size = 1000000  # Tamanho máximo de linhas por planilha
num_parts = len(tabela_final) // part_size + 1

for part_num in range(num_parts):
    start_idx = part_num * part_size
    end_idx = (part_num + 1) * part_size
    tabela_part = tabela_final[start_idx:end_idx]

    with pd.ExcelWriter(f'resultados_analise_part{part_num + 1}.xlsx') as writer:
        tabela_part.to_excel(writer, sheet_name=f'Dados Parte {part_num + 1}', index=False)

print("Análise concluída e resultados salvos em arquivos separados.")
