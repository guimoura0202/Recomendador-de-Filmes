import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify, redirect, request, render_template, url_for
from tmdbv3api import TMDb, Movie, Person
import json
import math
from recomendador.consultas import *
from recomendador.regras import ConjuntoRegras

# Configurar sua chave de API do TMDb
tmdb = TMDb()
tmdb.api_key = '7ea01ce68715414d0b7f3232f7cdd047'
tmdb.language = 'pt-BR'
tmdb_image_base_url = 'https://image.tmdb.org/t/p/w500'

# Inicializar objetos de busca
movie = Movie()
person = Person()

app = Flask(__name__)

@app.route('/')
def index():
    filmes = carrega_base_de_dados()
    page = request.args.get('page', 1, type=int)
    per_page = 20

    total = len(filmes)
    total_pages = math.ceil(total / per_page)

    start = (page - 1) * per_page
    end = start + per_page
    filmes_paginated = filmes[start:end]

    return render_template('index.html', filmes=filmes_paginated, page=page, total_pages=total_pages, max=max, min=min)

@app.route('/recomenda', methods=['GET'])
def recomenda_filmes():
    atores_preferidos = request.args.getlist('ator')
    if '' in atores_preferidos:
        atores_preferidos.remove('')
    diretores_preferidos = request.args.getlist('diretor')
    if '' in diretores_preferidos:
        diretores_preferidos.remove('')
    generos_preferidos = request.args.getlist('genero')
    if '' in generos_preferidos:
        generos_preferidos.remove('')
    ano_inicio = request.args.get('ano_inicio', type=int)
    ano_fim = request.args.get('ano_fim', type=int)
    avaliacao_minima = request.args.get('avaliacao_minima', type=float)
    page = request.args.get('page', 1, type=int)
    per_page = 20

    print("Atores Preferidos:", atores_preferidos)
    print("Diretores Preferidos:", diretores_preferidos)
    print("Gêneros Preferidos:", generos_preferidos)
    print("Ano Início:", ano_inicio)
    print("Ano Fim:", ano_fim)
    print("Avaliação Mínima:", avaliacao_minima)
    
    filmes = carrega_base_de_dados()
    recomendacoes = filmes

    if atores_preferidos:
        atores_filmes = []
        for ator in atores_preferidos:
            ator_filmes = consulta_ator(recomendacoes, ator)
            atores_filmes.extend(ator_filmes)
        recomendacoes = sorted(atores_filmes, key=lambda x: filmes.index(x))

    if diretores_preferidos:
        diretores_filmes = []
        for diretor in diretores_preferidos:
            diretor_filmes = consulta_diretor(recomendacoes, diretor)
            diretores_filmes.extend(diretor_filmes)
        recomendacoes = sorted(diretores_filmes, key=lambda x: filmes.index(x))

    if generos_preferidos:
        generos_filmes = []
        for genero in generos_preferidos:
            genero_filmes = consulta_genero(recomendacoes, genero)
            generos_filmes.extend(genero_filmes)
        recomendacoes = sorted(generos_filmes, key=lambda x: filmes.index(x))

    if ano_inicio or ano_fim:
        recomendacoes = consulta_ano(recomendacoes, ano_inicio, ano_fim)

    if avaliacao_minima:
        recomendacoes = consulta_avaliacao(recomendacoes, avaliacao_minima)

    recomendacoes = ConjuntoRegras.remover_filmes_duplicados(recomendacoes)
    total = len(recomendacoes)
    total_pages = math.ceil(total / per_page)

    start = (page - 1) * per_page
    end = start + per_page
    recomendacoes_paginated = recomendacoes[start:end]

    return render_template(
        'index.html',
        recomendacoes=recomendacoes_paginated,
        page=page,
        total_pages=total_pages,
        ator_preferido=atores_preferidos,
        diretor_preferido=diretores_preferidos,
        genero_preferido=generos_preferidos,
        ano_inicio=ano_inicio,
        ano_fim=ano_fim,
        avaliacao_minima=avaliacao_minima,
        max=max,
        min=min
    )

@app.route('/filme/<titulo>')
def detalhes_filme(titulo):
    filmes = carrega_base_de_dados()
    filme = next((filme for filme in filmes if filme['titulo'] == titulo), None)
    if filme is None:
        return render_template('404.html'), 404
    return render_template('detalhes.html', filme=filme)

@app.route('/ator/<nome>')
def detalhes_ator(nome):
    resultados = person.search(nome)
    if not resultados:
        return render_template('404.html'), 404
    ator = resultados[0]
    filmes_do_ator = person.movie_credits(ator.id)['cast']
    filmes_do_ator = sorted(filmes_do_ator, key=lambda x: x.get('release_date', 'N/A'), reverse=True)
    return render_template('ator.html', ator=ator, filmes=filmes_do_ator, tmdb_image_base_url=tmdb_image_base_url)

@app.route('/alterar_preferencias')
def alterar_preferencias():
    try:
        with open('preferencias.json', 'r') as f:
            preferencias = json.load(f)
    except FileNotFoundError:
        preferencias = {
            'generos': [],
            'atores': [],
            'diretores': [],
            'ano_minimo': '',
            'ano_maximo': '',
            'nota_minima': ''
        }

    return render_template('preferencias.html', preferencias=preferencias)

@app.route('/salvar_preferencias', methods=['POST'])
def salvar_preferencias():
    def convert_to_int(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0

    def convert_to_float(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    preferencias = {
        'generos': request.form.getlist('generos'),
        'atores': request.form.getlist('atores'),
        'diretores': request.form.getlist('diretores'),
        'ano_minimo': convert_to_int(request.form.get('ano_minimo')),
        'ano_maximo': convert_to_int(request.form.get('ano_maximo')),
        'nota_minima': convert_to_float(request.form.get('nota_minima'))
    }

    with open('preferencias.json', 'w') as f:
        json.dump(preferencias, f)

    return redirect(url_for('index'))

@app.route('/recomendacoes', methods=['GET'])
def recomendacoes():
    try:
        with open('preferencias.json', 'r') as f:
            preferencias = json.load(f)
    except FileNotFoundError:
        preferencias = {
            'generos': [],
            'atores': [],
            'diretores': [],
            'ano_minimo': 0,
            'ano_maximo': 9999,
            'nota_minima': 0.0
        }

    filmes = carrega_base_de_dados()
    
    recomendacoes_por_atores = []
    for ator in preferencias['atores']:
        recomendacoes_por_atores.extend(consulta_ator(filmes, ator))
    recomendacoes_por_atores = sorted(ConjuntoRegras.remover_filmes_duplicados(recomendacoes_por_atores), key=lambda x: filmes.index(x))

    recomendacoes_por_diretores = []
    for diretor in preferencias['diretores']:
        recomendacoes_por_diretores.extend(consulta_diretor(filmes, diretor))
    recomendacoes_por_diretores = sorted(ConjuntoRegras.remover_filmes_duplicados(recomendacoes_por_diretores), key=lambda x: filmes.index(x))

    recomendacoes_por_generos = []
    for genero in preferencias['generos']:
        recomendacoes_por_generos.extend(consulta_genero(filmes, genero))
    recomendacoes_por_generos = sorted(ConjuntoRegras.remover_filmes_duplicados(recomendacoes_por_generos), key=lambda x: filmes.index(x))

    recomendacoes_por_ano_e_avaliacao = sorted(
        consulta_ano_e_avaliacao(
            filmes,
            preferencias['ano_minimo'],
            preferencias['ano_maximo'],
            preferencias['nota_minima']
        ),
        key=lambda x: filmes.index(x)
    )

    recomendacoes_por_diretor_e_genero = []
    for diretor in preferencias['diretores']:
        for genero in preferencias['generos']:
            recomendacoes_por_diretor_e_genero.extend(consulta_diretor_e_genero(filmes, diretor, genero))
    recomendacoes_por_diretor_e_genero = sorted(ConjuntoRegras.remover_filmes_duplicados(recomendacoes_por_diretor_e_genero), key=lambda x: filmes.index(x))

    recomendacoes_por_ator_diretor_avaliacao = []
    for ator in preferencias['atores']:
        for diretor in preferencias['diretores']:
            recomendacoes_por_ator_diretor_avaliacao.extend(consulta_ator_diretor_avaliacao(filmes, ator, diretor, preferencias['nota_minima']))
    recomendacoes_por_ator_diretor_avaliacao = sorted(ConjuntoRegras.remover_filmes_duplicados(recomendacoes_por_ator_diretor_avaliacao), key=lambda x: filmes.index(x))

    return render_template(
        'recomendacoes.html',
        recomendacoes_por_atores=recomendacoes_por_atores,
        recomendacoes_por_diretores=recomendacoes_por_diretores,
        recomendacoes_por_generos=recomendacoes_por_generos,
        recomendacoes_por_ano_e_avaliacao=recomendacoes_por_ano_e_avaliacao,
        recomendacoes_por_diretor_e_genero=recomendacoes_por_diretor_e_genero,
        recomendacoes_por_ator_diretor_avaliacao=recomendacoes_por_ator_diretor_avaliacao
    )

def carrega_base_de_dados():
    with open('base.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)
    return dados['filmes']

if __name__ == '__main__':
    app.run(debug=True)
