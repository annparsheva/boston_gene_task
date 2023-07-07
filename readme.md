# Тестовое задание DataEngineer (Benchling)
## Описание
Необходимо разработать сервис по выгрузке отчета в формате csv из базы данных Benchling.csv на python.
## Установка
```
git clone https://github.com/annparsheva/boston_gene_task
cd report_builder
docker build -t report_builder .
```
## Запуск
```
docker run -t -v ${PWD}:/app report_builder 'HRD validation'
```
## Просмотр результатов
```
cat result/report_20230707_13:52:31.csv
```
## Просмотр лога
```
cat report_building.log
```
## Модули
### GetReseqTopOff
Модуль выставления флагов reseq/top-off.
* **group_and_count_samples** - группирует и выполняет подсчет количества образцов для экстракта и библиотеки.
* **get_group** - определяет данные по каждой группе (reseq, top-off, ничего).б проставляет лейблы для столбцов ```Is it reseq?```, ```Is it top off seq?```.
* **get_reseq_top_off** - отдает датафрейм с проставленными лейблами по каждой из групп.
### QCTest
Модуль, который проставляет в поле  ```QC``` значение pass/failed для всех образцов.
1. QC для DNA образцов: 
Library concentration от 10 до 100 - pass, иначе failed.
2. QC для RNA образцов: Library concentration от 15 до 110 - pass, иначе failed.
* **add_qc_test_column** - добавляет столбец QC со значениями pass/failed в зависимости от Library concentration.
### SamplesExclusion
Модуль, исключающий образцы из отчета, если у них не заполнено хотя бы одно из значений:
1. ```Library construction kit```
2. ```Library prob set kit```
3. ```Extraction kit```

Для пропущенных значений добавляется запись в лог
```'Заполните {имя пустого поля} для {имя библиотеки LIBxxxxxx}'.```
* **make_empty_data_report** - добавляет запись о пропусках в лог.
* **filter_empty_data** - отдает отфильтрованный датафрейм без образцов с пропусками
### ConfigReader
Класс, объединяющий методы чтения конфигурации и входных параметров.
* **get_parameter** - отдает значение параметра конфигурации по его имени.
* **get_project** - отдает название проекта, полученное при запуске программы
### DataLoader
Класс, объединяющий методы работы с данными: чтение, фильтрация, сохранение.
* **init_db** - сохраняет файл с базой данных в датафрейм.
* **get_project_data** - фильтрует базу данных по имени проекта.
* **save_data** - сохраняет итоговый отчет.

**data_base_analysis.pdf** - документ с аналитикой базы данных.