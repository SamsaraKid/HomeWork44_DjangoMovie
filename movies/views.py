from django.shortcuts import render
import os
# Create your views here.

dir = os.getcwd()
colors = {'dune': '#6B8B89', 'lotr': '#76663E', 'term': '#E74E35'}

def index(req):
    return render(req, 'index.html')

# функция получения данных
def getdata(title):
    # задаём пути к папкам
    posters_path = dir + '/movies/static/' + title + '/img/posters/'
    photos_path = dir + '/movies/static/' + title + '/img/personas/'
    personas_desc_path = dir + '/movies/static/' + title + '/text/personas/'

    # массивы с путями к файлам
    posters = list(map(lambda x: title + '/img/posters/' + x,
                       [f for f in os.listdir(posters_path) if os.path.isfile(os.path.join(posters_path, f))]))
    photos = list(map(lambda x: title + '/img/personas/' + x,
                        [f for f in os.listdir(photos_path) if os.path.isfile(os.path.join(photos_path, f))]))
    desc_file = dir + '/movies/static/' + title + '/text/desc.txt'
    personas_desc_files = list(map(lambda x: personas_desc_path + x,
                                   [f for f in os.listdir(personas_desc_path) if
                                    os.path.isfile(os.path.join(personas_desc_path, f))]))

    # получаем название и описание фильма
    desc_file = open(desc_file, 'r', encoding='utf-8')
    desc_file_text = desc_file.readlines()
    title = desc_file_text[0].replace('\n', '')
    desc = desc_file_text[1]
    desc_file.close()

    link_names = list(map(lambda x: x.split('/')[-1].split('.')[0], photos))

    # получаем информацию о персонажах
    names = []
    bios = []
    actors = []
    wikis = []
    for f in personas_desc_files:
        persona_desc = open(f, 'r', encoding='utf-8')
        persona_desc_text = persona_desc.readlines()
        names.append(persona_desc_text[0].replace('\n', ''))
        bios.append(persona_desc_text[1].replace('\n', ''))
        actors.append(persona_desc_text[2].replace('\n', ''))
        wikis.append(persona_desc_text[3].replace('\n', ''))
        persona_desc.close()

    return {'title': title, 'posters': posters, 'desc': desc, 'photos': photos, 'names': names, 'bios': bios,
            'actors': actors, 'wikis': wikis, 'link_names': link_names}


def movie(req, title):
    data = getdata(title)
    color = colors[title]
    data = {'title': data['title'], 'posters': data['posters'], 'desc': data['desc'], 'title_link': title,
            'characters': zip(data['photos'], data['names'], data['link_names']), 'color': color}
    return render(req, 'movie.html', context=data)

def persona(req, title, name):
    data = getdata(title)
    color = colors[title]
    num = data['link_names'].index(name)
    data = {'name': data['names'][num], 'photo': data['photos'][num], 'bio': data['bios'][num],
            'actor': data['actors'][num], 'wiki': data['wikis'][num], 'title': title, 'color': color}
    return render(req, 'persona.html', context=data)

