from bs4 import BeautifulSoup
import requests

def spisok_number_to60():
    counter_number=int()
    list_rt=str()
    while counter_number != 60:
        counter_number+=1
        list_rt+=f'{str(counter_number)} '
    list_rt=list_rt.split()
    return list_rt

async def search(name_film):
    url='https://kino.mail.ru/search/?q='+name_film
    request=requests.get(url)
    soup=BeautifulSoup(request.text, "html.parser")
    a=soup.find('div', class_='margin_top_20')

    url='https://kino.mail.ru'+a.find('a')['href']
    request=requests.get(url)
    soup=BeautifulSoup(request.text, "html.parser")

    type_kino=soup.find('div', class_='p-truncate p-truncate_background-gray p-truncate_multiline p-truncate_multiline-3 p-truncate_multiline-podrobnee js-module js-toggle__truncate margin_bottom_20 reset-inner-fonts')
    type_kino=type_kino.find('h2', class_='text text_inline text_bold_normal text_fixed text_letter-spacing text-mode_uppercase valign_baseline').text
    type_kino=type_kino[type_kino.find(' '):type_kino.find(':')][1:-1].title()

    film_data=soup.find('div', class_='block block_bg_gray padding_vertical_x8')
    more=soup.find_all('div', class_='margin_bottom_20')

    for i in more:
        genre=i.find_all('span', class_='nowrap')
        if genre != []:
            break
    for i in genre:
        genre_one=i.find('a', class_='badge badge_gray badge_gray_rgba badge_border_off badge_link')
        if genre_one != None:
            genre_one=genre_one.text
            break

    photo=film_data.find('picture', class_='picture p-framer__picture').find('img')['src']
    director=film_data.find('div', class_='p-truncate p-truncate_ellipsis js-module js-toggle__truncate js-toggle__truncate js-toggle__truncate-first').text
    text_autor=film_data.find('div', class_='table__cell padding_right_10').text
    name_film=soup.find('div', class_='p-movie-intro__content-inner').find('h1',class_='text text_light_promo color_white').text
    #try:
    film_data2=soup.find_all('div', class_='margin_bottom_20')

    for i in film_data2:
        length=i.find('span', class_='margin_left_40 nowrap')
        try:
            if length != None and length.text[0] in spisok_number_to60():
                break
        except:
            pass
    if length == None:
        length='Неизвестно'
    else:
        length=length.text
    
    class rt_films_data():
        name_film_=name_film
        type_kino_=type_kino
        genre_=genre_one
        photo_=photo
        director_=director
        text_autor_=text_autor
        length_=length
                
    return rt_films_data

