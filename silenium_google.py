import shutil
import requests
import urllib.parse
from bs4 import BeautifulSoup as BS4

def get_page(phrase, page):
    # Определяем ссылку на страницу, к которой будем отправлять запрос
    link = "https://www.istockphoto.com/ru/%D1%84%D0%BE%D1%82%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%B8/" + phrase 
    # Определяем словарь с заголовками
    headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

    # Определяем словарь с параметрами запроса
    params = {"page": page, "phrase": phrase, "sort": "mostpopular"} # Отправляем запрос на страницу с картинками
    request = requests.get(link, headers=headers, params=params)
    # Возвращаем HTML-код из функции
    return request.text
# Проверяет, есть ли на странице изображения
def is_404(html):
    page = BS4(html, "html.parser")

    if len(page.select("img.gallery-asset__thumb")) < 0:
        return True
    return False
# Получает список ссылок с конкретной страницы из выдачи по запросу
def get_imgs_from_page(phrase, page):
    # Получаем HTML-код конкретной страницы выдачи
    html = get_page(phrase, page)
    # Определяем локальный список, в который будут помещаться ссылки на изображение
    images = []
    # Если вернуло страницу 404, значит прерываем выполнение функции, возвращая False
    if is_404(html) == True:
        return False

    img_node = BS4(html, "html.parser")

    imgs = img_node.select("img.gallery-asset__thumb")
    for img in imgs:        
        if img.has_attr("src"):
            print(f"Получили ссылку на фото: {img['src']}")
            images.append(img["src"])

    return images
# Получает список ссылок на изображения с заданного количества страниц по запросу
def get_images(query, pages):

    query = urllib.parse.quote(query)

    images = []

    for i in range(pages):

        num_of_page = i + 1
        img = get_imgs_from_page(query, num_of_page)

        if not img:
            break
        else:
            images += img
        return images

def save_image(folder, link):
    image = requests.get(link, stream=True)
    filename = link.split("/")[4]
    filename = filename.split("?")[0]
    path_to_file = f"{folder}/{filename}.jpg"
    print(f"Сохранили фото: {path_to_file}")
    with open(path_to_file, "wb") as file_obj:
        shutil.copyfileobj(image.raw, file_obj)

def download_images(folder, phrase, page):
    images = get_images(phrase, page)
    for image in images:
        try:
            save_image(folder, image)
        except Exception as error:
            print(f"Проблема с записью файла: {error}")

