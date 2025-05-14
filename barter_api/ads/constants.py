CONDITION_CHOICES = [
    ('new', 'Новый'),
    ('used', 'Б/у'),
    ('broken', 'Требует ремонта'),
]
CATEGORY_CHOICES = [
    ('electronics', 'Электроника'),
    ('clothing', 'Одежда'),
    ('books', 'Книги'),
    ('home', 'Дом и сад'),
    ('other', 'Другое'),
]
DESC_LENGHT_MIN = 20
LENGHT_MAX = 50
PAGE_SIZE = 10
PAGE_SIZE_QUERY_PARAM = 'page_size'
PAGE_SIZE_MAX = 100
PAGE_QUERY_PARAM = 'page'
STATUS_LENGHT_MAX = 20
STATUS_CHOICES = [
    ('pending', 'Ожидает'),
    ('accepted', 'Принята'),
    ('rejected', 'Отклонена'),
    ('canceled', 'Отменена'),
]
TITLE_LENGHT_MAX = 200
TITLE_LENGHT_MIN = 5
