# book_api
## Установка
```
git clone https://github.com/andrekur/book_api.git
cd book_api/_CD
mv env.example .env
sudo docker-compose build
sudo docker-compose up
```
после проверьте адресс localhost:80/docs
## Ссылки в продукте

book_slug - это isbn книги

| Тип запроса |           Адрес           |                                                         Описание                                                         |
|:-----------:|:-------------------------:|:------------------------------------------------------------------------------------------------------------------------:|
|     GET     |           /docs           |                                                 документация по проекту                                                  |
|     GET     |          /books           |                                                    Получить все книги                                                    |
|    POST     |          /books           |                                                      Создать книгу                                                       |
|     GET     |    /books/{book_slug}     |                                          Получить информацию о конкретной книге                                          |
|     GET     |  /books/{book_slug}/urls  |                                    Получить все ссылки(страница в магазине) на книгу                                     |
|    POST     |  /books/{book_slug}/urls  |                                      Добавить ссылку(страница в магазине) на книгу                                       |
|     GET     | /books/{book_slug}/prices | Получить все цены в магазинах на книгу.<br/>query_params:  last_price если нужно выбрать последние цены. default = false |
|    POST     | /books/{book_slug}/prices |                                        Добавить цену кники в конкретном магазине                                         |
|     GET     |          /shops           |                                                  Получить все магазины                                                   |
|    POST     |          /shops           |                                                     Создать магазин                                                      ||
|    POST     |      /systems/parser      |                                              Необходимо для работы парсера                                               |


## Модели

# BookModel

|    Поле     |   Тип   | Обязательно |    Описание    |
|:-----------:|:-------:|:-----------:|:--------------:|
|    slug     | string  |    True     |   isbn книги   |
|    name     | string  |    True     | Название книги |
| count_pages | integer |    True     |  Кол. страниц  |
|   weight    | integer |    True     |      Вес       |
|    size     | string  |    True     |    Размеры     |

# ShopModel

|    Поле     |   Тип   | Обязательно |     Описание      |
|:-----------:|:-------:|:-----------:|:-----------------:|
|    name     | string  |    True     | Название магазина |

# PriceModel

|   Поле   |     Тип     | Обязательно |       Описание        |
|:--------:|:-----------:|:-----------:|:---------------------:|
|  price   |   integer   |    True     | Цена книги в магазине |
| discount |   integer   |    True     |        Скидка         |
| shop_id  | integer(FK) |    True     | Внешний ключ магазина |