from regras import ConjuntoRegras

def consulta_ator(filmes, ator_preferido):
    recomendacoes = [filme for filme in filmes if ConjuntoRegras.recomenda_por_ator(filme, ator_preferido)]
    recomendacoes_unicas = ConjuntoRegras.remover_filmes_duplicados(recomendacoes)
    return recomendacoes_unicas

def consulta_diretor(filmes, diretor_preferido):
    recomendacoes = [filme for filme in filmes if ConjuntoRegras.recomenda_por_diretor(filme, diretor_preferido)]
    recomendacoes_unicas = ConjuntoRegras.remover_filmes_duplicados(recomendacoes)
    return recomendacoes_unicas

def consulta_diretor_e_genero(filmes, diretor_preferido, genero_preferido):
    recomendacoes = [filme for filme in filmes if ConjuntoRegras.recomenda_por_diretor_e_genero(filme, diretor_preferido, genero_preferido)]
    recomendacoes_unicas = ConjuntoRegras.remover_filmes_duplicados(recomendacoes)
    return recomendacoes_unicas

def consulta_ano_e_avaliacao(filmes, ano_inicio, ano_fim, avaliacao_minima):
    recomendacoes = [filme for filme in filmes if ConjuntoRegras.recomenda_por_ano_e_avaliacao(filme, ano_inicio, ano_fim, avaliacao_minima)]
    recomendacoes_unicas = ConjuntoRegras.remover_filmes_duplicados(recomendacoes)
    return recomendacoes_unicas

def consulta_genero(filmes, genero_preferido):
    recomendacoes = [filme for filme in filmes if ConjuntoRegras.recomenda_por_genero(filme, genero_preferido)]
    recomendacoes_unicas = ConjuntoRegras.remover_filmes_duplicados(recomendacoes)
    return recomendacoes_unicas

def consulta_ator_diretor_avaliacao(filmes, ator_preferido, diretor_preferido, avaliacao_minima):
    recomendacoes = [filme for filme in filmes if ConjuntoRegras.recomenda_por_ator_diretor_avaliacao(filme, ator_preferido, diretor_preferido, avaliacao_minima)]
    recomendacoes_unicas = ConjuntoRegras.remover_filmes_duplicados(recomendacoes)
    return recomendacoes_unicas

def consulta_ano(filmes, ano_inicio, ano_fim):
    if ano_inicio and ano_fim:
        return [filme for filme in filmes if ConjuntoRegras.recomenda_por_ano_e_avaliacao(filme, ano_inicio, ano_fim, 0)]
    elif ano_inicio:
        return [filme for filme in filmes if ConjuntoRegras.recomenda_por_ano_e_avaliacao(filme, ano_inicio, 9999, 0)]
    elif ano_fim:
        return [filme for filme in filmes if ConjuntoRegras.recomenda_por_ano_e_avaliacao(filme, 0, ano_fim, 0)]
    else:
        return filmes

def consulta_avaliacao(filmes, avaliacao_minima):
    return [filme for filme in filmes if ConjuntoRegras.recomenda_por_ano_e_avaliacao(filme, 0, 9999, avaliacao_minima)]