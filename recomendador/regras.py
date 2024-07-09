"""Este módulo contém a classe `ConjuntoRegras` que engloba as regras de
recomendação de filmes baseadas em diferentes critérios de preferência do usuário.
"""


class ConjuntoRegras:
    """Classe que contém as regras de recomendação de filmes baseadas em diferentes critérios de preferência do usuário."""

    @staticmethod
    def recomenda_por_ator(filme: dict, ator_preferido: str) -> bool:
        """Realiza a recomendação de um filme baseado em um ator preferido.

        Args:
            filme (dict): Filme a ser ou não recomendado.
            ator_preferido (str): Ator preferido pelo usuário.

        Returns:
            (bool): Informação (True ou False) se o filme deve ser recomendado ou não.
        """
        return any(ator_preferido.lower() in ator.lower() for ator in filme["elenco"])
    
    @staticmethod
    def recomenda_por_diretor(filme: str, diretor_preferido: str) -> bool:
        """Realiza a recomendação de um filme baseado em um diretor preferido.

        Args:
            filme (str): Filme a ser ou não recomendado.
            diretor_preferido (str): Diretor preferido pelo usuário.

        Returns:
            (bool): Informação (True ou False) se o filme deve ser recomendado ou não.
        """
        return diretor_preferido.lower() in filme["diretor"].lower()

    @staticmethod
    def recomenda_por_diretor_e_genero(filme: dict, diretor_preferido: str, genero_preferido: str) -> bool:
        """Realiza a recomendação de um filme baseado em um diretor e gênero preferidos.

        Args:
            filme (dict): Filme a ser ou não recomendado.
            diretor_preferido (str): Diretor preferido pelo usuário.
            genero_preferido (str): Gênero preferido pelo usuário.

        Returns:
            (bool): Informação (True ou False) se o filme deve ser recomendado ou não.
        """
        return (diretor_preferido.lower() in filme['diretor'].lower() and genero_preferido.lower() in filme['genero'].lower())

    @staticmethod
    def recomenda_por_ano_e_avaliacao(filme: dict, ano_inicio: int, ano_fim: int, avaliacao_minima: float) -> bool:
        """Realiza a recomendação de um filme baseado na faixa de ano de lançamento e avaliação média.

        Args:
            filme (dict): Filme a ser ou não recomendado.
            ano_inicio (int): Ano de início da faixa.
            ano_fim (int): Ano de fim da faixa.
            avaliacao_minima (float): Avaliação mínima média do filme.

        Returns:
            (bool): Informação (True ou False) se o filme deve ser recomendado ou não.
        """
        try:
            ano_lancamento = int(filme['ano'])
        except ValueError:
            return False  # Se não for possível converter para int, filme não é recomendado
        avaliacao_media = sum(filme['avaliacoes']) / len(filme['avaliacoes']) if filme['avaliacoes'] else 0

        return ano_inicio <= ano_lancamento <= ano_fim and avaliacao_media >= avaliacao_minima
    
    @staticmethod
    def recomenda_por_genero(filme: str, genero_preferido: str) -> bool:
        """Realiza a recomendação de um filme baseado em um gênero preferido.

        Args:
            filme (str): Filme a ser ou não recomendado.
            genero_preferido (str): Gênero preferido pelo usuário.

        Returns:
            (bool): Informação (True ou False) se o filme deve ser recomendado ou não.
        """
        return genero_preferido.lower() in filme["genero"].lower()
    
    @staticmethod
    def recomenda_por_ator_diretor_avaliacao(filme: dict, ator_preferido: str, diretor_preferido: str, avaliacao_minima: float) -> bool:
        """Realiza a recomendação de um filme baseado em ator/atriz, diretor e avaliação média.

        Args:
            filme (dict): Filme a ser ou não recomendado.
            ator_preferido (str): Ator ou atriz preferido pelo usuário.
            diretor_preferido (str): Diretor preferido pelo usuário.
            avaliacao_minima (float): Avaliação mínima para filtrar os filmes.

        Returns:
            bool: Informação (True ou False) se o filme deve ser recomendado ou não.
        """
        ator_encontrado = any(ator_preferido.lower() in ator.lower() for ator in filme["elenco"])
        diretor_encontrado = diretor_preferido.lower() in filme["diretor"].lower()
        avaliacao_media = sum(filme['avaliacoes']) / len(filme['avaliacoes']) if filme['avaliacoes'] else 0

        return ator_encontrado and diretor_encontrado and avaliacao_media >= avaliacao_minima
    @staticmethod
    def remover_filmes_duplicados(filmes):
        """Remove filmes duplicados da lista de recomendações.

        Args:
            filmes (list): Lista de filmes.

        Returns:
            list: Lista de filmes únicos.
        """
        filmes_unicos = []
        for filme in filmes:
            if filme not in filmes_unicos:
                filmes_unicos.append(filme)
        return filmes_unicos

    @staticmethod
    def recomenda_por_diretor_e_genero(filme: dict, diretor_preferido: str, genero_preferido: str) -> bool:
        """Realiza a recomendação de um filme baseado em um diretor e gênero preferidos.

        Args:
            filme (dict): Filme a ser ou não recomendado.
            diretor_preferido (str): Diretor preferido pelo usuário.
            genero_preferido (str): Gênero preferido pelo usuário.

        Returns:
            (bool): Informação (True ou False) se o filme deve ser recomendado ou não.
        """
        return (diretor_preferido.lower() in filme['diretor'].lower() and genero_preferido.lower() in filme['genero'].lower())
    
    @staticmethod
    def recomenda_por_ator_diretor_avaliacao(filme: dict, ator_preferido: str, diretor_preferido: str, avaliacao_minima: float) -> bool:
        """Realiza a recomendação de um filme baseado em ator/atriz, diretor e avaliação média.

        Args:
            filme (dict): Filme a ser ou não recomendado.
            ator_preferido (str): Ator ou atriz preferido pelo usuário.
            diretor_preferido (str): Diretor preferido pelo usuário.
            avaliacao_minima (float): Avaliação mínima para filtrar os filmes.

        Returns:
            bool: Informação (True ou False) se o filme deve ser recomendado ou não.
        """
        ator_encontrado = any(ator_preferido.lower() in ator.lower() for ator in filme["elenco"])
        diretor_encontrado = diretor_preferido.lower() in filme["diretor"].lower()
        avaliacao_media = sum(filme['avaliacoes']) / len(filme['avaliacoes']) if filme['avaliacoes'] else 0

        return ator_encontrado and diretor_encontrado and avaliacao_media >= avaliacao_minima                                                                                                       