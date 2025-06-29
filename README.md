Весь проект представляет из себя сервис атоматического распознавания лечения из историй болезней и их формализацию.
Под формализацией подразумивается занесения назначенных лекарств и их характеристик (дозировка, время приёма, способ приёма) в один из двух форматов
#### Формат первый:
{
    "route": "внутрь",
    "dosage": "500.0 мл",
    "total": "1000.0 мл",
    "name": "Дибен",
    "period": "1-1"
  }
  route - способ приёма
  dosage - единоразовая дорзировка препарата
  total - дневноая доза препарата
  name - наименование препарата
  period - интервал приёма препарата на основе всего курса лечения пациента
  #### Формат второй:
  {
    "route": "внутрь",
    "dosage": "90 мг",
    "total": "2",
    "name": "Брилинта",
    "period": "1-7"
  }
  route - способ приёма
  total - общее количестко приёма препарата в день
  dosage - единоразовая дорзировка препарата
  comment - коментарии к приёму
  name - наименование препарата
  period - интервал приёма препарата на основе всего курса лечения пациента
  _________________________________________________
  Структура проекта следующая :
  final_diplom/
|── date_dynamics/
|── end/
|── no_date_dynamics/
|── no_table/
|── parser_form_hourly_assignment_sheet/
|──     |── concentration.py
|──     |── date_dynamics.py
|──     |── html_to_json.py
|──     └── regular_expressions_parser.py
|── parser_with_no_hourly_assignment_sheet/
|──     |── end_parser.py
|──     |── medicine_with_date.txt
|──     |── model_result.txt
|──     |── parse_and_clean_table.py
|──     |── resul_parser.txt
|──     └── sort_by_date.py
|── RuBioBert_model/
|──     |── rubio_bert_classifier/
|──     └── RuBioBert.py
|── table/
|── test/
|── main.py
└── requirements.txt
**date_dynamics** - Директория с результатом обработки парсером по назначениям, которые не входяд в лист почасовых назначений
**end** - Директория содержащая результаты обработки всех историй болезней
**no_date_dynamics** - Директория с результатами работы регулярных строк над данными, извлечёнынми из листов почасовых назначений
**no_table** - Директория с файлами, не содержащими листы почасовых назначений
**parser_form_hourly_assignment_sheet** - Директория содержащая скрипты  связаныне с обработкой документов, содержащих листы почасовых назначений
**concentration.py** - Скрипт извлекающий паттерн с содержанием концентрации
**date_dynamics.py** - Скрипт позволяющий извлечь динамику по дням из результатов обработки историй болезней, содержащих листы почасовых назначений
**html_to_json.py** - Скрипт, извлекающий данные из листов почасовых назначений, а в случае их отсутсвия в документе, копирование документа для последующей обработки
**regular_expressions_parser.py** - Скрипт разбиения данных из историй болезней в json формат, с помощью регулярных выражений
**parser_with_no_hourly_assignment_sheet** - Директория содержащая всё связанное с обработкой историй болезней, не содержащих листы почасовых назначений.
**end_parser.py** - Скрипт отвечающий за распределениея отсортированных результатов работы модели в json форму
**test** - Директория содержит 20 примеров историй болезней для тестирования системы
**medicine_with_date.txt** - Результат сортировки выхода модели, проще говоря извлечение всех назначений с окончанием в виде дат
**model_result.txt** - Результат работы модели RuBioBERT по нахождению лекарств в таблицах
**parse_and_clean_table.py** - Скрипт парсинга и очистки всех таблиц из документов, не содержищих листы почасовых назначений
**result_parser.txt** - путь ко всем таблицам из историй болезней, не содержащих листы почасовых назначений
**sort_by_date.py** - Скрипт, отвечающий за сортировку результатов работы модели, основывающаяся на строках, заканчивающихся на даты
**RuBioBert_model** - Директориях хранящая всё что связано с моделью RuBioBert 
**rubio_bert_classifier** - Директория хранящая модель RuBioBert
**RuBioBert.py** - Скрипт, отвечающий за вызов модели RuBioBert
**table** - Директория с данными из файлов, содержащих листы почасовых назначений
**main.py** - Основной файл, объеденяющий все скрипты в единую структуру
**requirements.txt** - Необходимые для работы сервиса библиотеки Python
_________________________________________________
Весь процесс обработки представлен в виде блок-схемы в Process.jpg.
Если говорить словами то его можно представить следующим образом:
Проверям html документ на наличие таблиц с тегом "tab_lhp"
Если тег присутсвует:
парсим данные из этих таблиц -> с помощью регулярных выражений заносим эти данные в json формат -> отоборажаем динамику по дням.
Если тег отсутсвует:
парсим данные со всех таблиц в документа -> каждую из получившихся строк даём на вход модели RuBioBert -> из всех результатов работы модели берём те, что заканчиваются на даты -> с помощью регулярных выражений заносим эти данные в json формат -> отоборажаем динамику по дням.
_________________________________________________
Руководство по запуску:
## Требования

- Python версии 3.8 или выше
- pip (установщик пакетов для Python)

Если Python не установлен, его можно загрузить с официального сайта:

https://www.python.org/downloads/

После установки рекомендуется перезапустить терминал или добавить Python в переменную окружения PATH вручную.

## Установка

### 1. Клонирование проекта
git clone https://github.com/your/repo.git
cd repo
### 2. Создание виртуального окружения (рекомендуется)
python -m venv venv
Активация виртуального окружения: venv\Scripts\activate
### 3. Установка зависимостей 
pip install -r requirements.txt
### 4. Загрузка весов модели
Загрузить веса модели и распаковать по пути: repo/RuBioBert_model/rubio_bert_classifier
ссылка на закрузку модели:https: //drive.google.com/file/d/1g1sDlZzv0x-Xii5tqbxrJD47uslvsOM_/view?usp=sharing
### 5. Запустить скрипт main.py с указанием директории с историями болезней
пример: python python .\main.py .\test\history\
