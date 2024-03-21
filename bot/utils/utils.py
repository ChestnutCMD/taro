import asyncio
import random
from PIL import Image
import httpx
from bs4 import BeautifulSoup


def choice_cart():
    carts = [cart for cart in range(1, 79)]
    return random.choice(carts)


def choice_tree_carts():
    carts = [cart for cart in range(1, 79)]
    random.shuffle(carts)
    choices_carts = [carts[0], carts[1], carts[2]]
    return choices_carts


def image_join(image1: str, image2: str, image3: str, name: str):
    img1 = Image.open(image1)
    img2 = Image.open(image2)
    img3 = Image.open(image3)

    new_img = Image.new("RGB", (660, 400), "black")

    new_img.paste(img1, (0, 0))
    new_img.paste(img2, (220, 0))
    new_img.paste(img3, (440, 0))
    new_img.save(f'Images/Prediction/{name}.jpg', 'JPEG')
    return f'Images/Prediction/{name}.jpg'

# converted_img = img.transpose(Images.FLIP_TOP_BOTTOM)  # перевернуть изображение # rotated_img = img.rotate(180)


headers = {
    'accept-language': 'en-us,en;q=0.5',
    'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}


async def get_response(link: str):
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as htx:
        result: httpx.Response = await htx.get(url=link)
        if result.status_code != 200:
            return await get_response(link=link)
        else:
            return await result.aread()


async def get_text_horoscope(zodiac: str, period: str = 'today'):
    link = f'https://horo.mail.ru/prediction/{zodiac}/{period}/'
    response_result = await get_response(link=link)
    beautifulsoup: BeautifulSoup = BeautifulSoup(markup=response_result, features='lxml')
    text = beautifulsoup.find(name='div', class_='article__item article__item_alignment_left article__item_html')
    return text.text
