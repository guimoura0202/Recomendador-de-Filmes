from tmdbv3api import TMDb, Movie
import json
import time

# Configurar sua chave de API do TMDb
tmdb = TMDb()
tmdb.api_key = '7ea01ce68715414d0b7f3232f7cdd047'
tmdb.language = 'pt-BR'
tmdb.image_base_url = 'https://image.tmdb.org/t/p/w500'

# Inicializar o objeto de busca de filmes
movie = Movie()

# Preparar a lista para salvar os filmes
filmes_list = []

# Buscar até 50 páginas de resultados (20 filmes por página)
for i in range(1, 51):  # 50 páginas * 20 filmes por página = 1000 filmes
    popular_movies = movie.popular(page=i)
    for m in popular_movies:
        # Obter informações detalhadas de cada filme
        details = movie.details(m.id, append_to_response='credits')

        # Verificar se os créditos existem e são acessíveis
        if hasattr(details, 'credits'):
            credits = details.credits

            diretor = next((crew.name for crew in credits.crew if crew.job == 'Director'), "N/A")
            elenco = [cast.name for cast in list(credits.cast)[:10]]  # Pegando os 5 primeiros atores
        else:
            diretor = "N/A"
            elenco = []

        # Montar a URL da imagem do pôster
        poster_url = f"{tmdb.image_base_url}{details.poster_path}" if details.poster_path else "N/A"

        # Adicionar sinopse
        sinopse = details.overview if details.overview else "Sinopse não disponível"

        filme = {
            "titulo": details.title,
            "genero": ", ".join([g.name for g in details.genres]),
            "diretor": diretor,
            "ano": details.release_date.split('-')[0] if details.release_date else "N/A",
            "elenco": elenco,
            "avaliacoes": [details.vote_average],
            "poster_url": poster_url,
            "sinopse": sinopse
        }
        filmes_list.append(filme)
    print(f'Página {i} processada...')
    time.sleep(0.3)  # Pequeno atraso para evitar sobrecarga na API

# Salvar os filmes em um arquivo JSON
with open('base.json', 'w', encoding='utf-8') as f:
    json.dump({"filmes": filmes_list}, f, ensure_ascii=False, indent=4)

print(f'{len(filmes_list)} filmes salvos em base.json')
