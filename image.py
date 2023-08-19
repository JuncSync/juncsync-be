import base64
from io import BytesIO
import json
from PIL import Image, ImageDraw, ImageFont
import requests

URL = "https://stage00.common.solumesl.com/common/api/v2/common/labels/image?company=JC13&store=1111"

LABEL_LIST = [
    "0848A722E1DB",
    "085C1AFCE1DB",
    "085C1B02E1DB",
    "085C1B0BE1D2",
    "085C1B14E1DC",
]


def solumn_image_push(label: str, page: int, image: str) -> bool:
    headers = {
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ilg1ZVhrNHh5b2pORnVtMWtsMll0djhkbE5QNC1jNTdkTzZRR1RWQndhTmsiLCJ0eXAiOiJKV1QifQ.eyJpZHAiOiJMb2NhbEFjY291bnQiLCJvaWQiOiIwODJjYzA3Ni0xMTBmLTQxODUtYjlkYS0xZTUxYWVhNDZhNjkiLCJzdWIiOiIwODJjYzA3Ni0xMTBmLTQxODUtYjlkYS0xZTUxYWVhNDZhNjkiLCJuYW1lIjoiY3NpYTEwa21sYTIzIiwibmV3VXNlciI6ZmFsc2UsImV4dGVuc2lvbl9BZG1pbkFwcHJvdmVkIjp0cnVlLCJleHRlbnNpb25fQ3VzdG9tZXJDb2RlIjoiSkMxMyIsImV4dGVuc2lvbl9DdXN0b21lckxldmVsIjoiMSIsImVtYWlscyI6WyJjc2lhMTBrbWxhMjNAZ21haWwuY29tIl0sInRmcCI6IkIyQ18xX1JPUENfQXV0aCIsImF6cCI6ImUwOGU1NGZmLTViYjEtNGFlNy1hZmRlLWI5Y2RjOGZhMjNhZSIsInZlciI6IjEuMCIsImlhdCI6MTY5MjQ1MjIwNCwiYXVkIjoiZTA4ZTU0ZmYtNWJiMS00YWU3LWFmZGUtYjljZGM4ZmEyM2FlIiwiZXhwIjoxNjkyNTM4NjA0LCJpc3MiOiJodHRwczovL3NvbHVtYjJjLmIyY2xvZ2luLmNvbS9iMGM4ZTNkOS0wOGZhLTQ4N2EtYWZmMS04NWJhZTExZmM2YzUvdjIuMC8iLCJuYmYiOjE2OTI0NTIyMDR9.szfIericwcqvyYSwpBvZG8-ecTFL_ZnB3zYQj35XX7-q4Ep49fnwBu9tE6soaIVdERosjmwUVjc_yhTg8KnHCieQMMaeP7IxJZ42N3Y-YY7ZkG3n4Zu5BtH_lpRoPSzjj08rF2D8cauZeALG6pEEWg17TqSpNfAqAlHiFDKF_wZ8SKD-3r8F5sDXUhp80Ejz-qYbVlpZCvvosKi3J6hxxauVHQAH7LfBh34HH3M8zxm1PIzmh3MDcaDn2g4kIYlla5rISgA3GP9g3ukL4dZP_bjs_pdlaRWabQa-ub1n6gdKJFEbWWCqdBBBS2oQLAKWvH1d1VfcWYppUJ1zbCgHHw",
        # "Authorization": "Bearer " + token.replace(" ", ""),
        "Content-Type": "application/json",
    }

    data = {
        "labelCode": label,
        "page": page,
        "frontPage": 1,
        "image": image,
        "articleList": [
            {
                "articleId": "B100001",
                "articleName": "OAP DISPENSER LARGE",
                "nfcUrl": "http://www.solumesl.com",
                "data": {
                    "ARTICLE_ID": "B100001",
                    "ARTICLE_NAME": "OAP DISPENSER LARGE",
                    "NFC_URL": "http://www.solum.com/p/B100001",
                    "SALE_PRICE": "$100",
                    "DISCOUNT_PRICE": "$90",
                },
            }
        ],
    }

    response = requests.post(URL, headers=headers, data=json.dumps(data))
    print(response.text)
    if response.status_code == 200:
        return True
    else:
        return False


def draw_blank_image(
    bed: str,
    name: str,
    age: int,
    gender: str,
    diagnosis: str,
    date: str = "20.08.2023",
) -> str:
    with Image.open("template/blank.png") as img:
        # width, height = img.size
        # img.show()
        bed_font = ImageFont.truetype("font/Pretendard-SemiBold.otf", 14)
        name_font = ImageFont.truetype("font/Pretendard-SemiBold.otf", 20)
        detail_font = ImageFont.truetype("font/Pretendard-Medium.otf", 8)

        draw = ImageDraw.Draw(img)
        draw.text((21, 16.11), bed, font=bed_font, fill=(113, 113, 113))
        draw.text((20, 34), name + "(" + str(age) + ")", font=name_font, fill=(0, 0, 0))
        draw.text((20, 67), ": " + gender, font=detail_font, fill=(113, 113, 113))
        draw.text((20, 77), ": " + diagnosis, font=detail_font, fill=(113, 113, 113))
        draw.text((20, 87), ": " + date, font=detail_font, fill=(113, 113, 113))
        draw = ImageDraw.Draw(img)

        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str.replace(" ", "")


def draw_level_image(level: int, bed: str, time: str) -> str:
    image_path = "template/level-" + str(level) + ".png"
    with Image.open(image_path) as img:
        bed_font = ImageFont.truetype("font/Pretendard-SemiBold.otf", 14)
        time_font = ImageFont.truetype("font/Pretendard-SemiBold.otf", 40)

        draw = ImageDraw.Draw(img)
        draw.text((21, 16.11), bed, font=bed_font, fill=(113, 113, 113))
        draw.text((118.2, 59.64), time, font=time_font, fill=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str.replace(" ", "")


res = solumn_image_push(LABEL_LIST[0], 1, draw_level_image(5, "BED-0B", "23:43"))
print(res)
