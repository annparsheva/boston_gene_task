import os
import pandas as pd
from typing import Type
from datetime import datetime
from config_reader import ConfigReader


class DataLoader:
    def __init__(self, db_path, db_file_name) -> None:
        """
        Класс, объединяющий методы работы с данными: чтение, фильтрация, сохранение.
        db_path - путь к базе данных
        db_file_name - название файла базы данных
        data - датафрейм с данными
        """
        self.db_path = db_path
        self.db_file_name = db_file_name
        self.data = pd.DataFrame()

    def init_db(self):
        """Сохраняет файл с базой данных в датафрейм."""
        file_path = os.path.join(self.db_path, self.db_file_name)
        self.data = pd.read_csv(file_path)

    def get_project_data(self, project: str) -> pd.DataFrame:
        """Фильтрует базу данных по имени проекта.

        :param project (str): название проекта
        :return project_data (pd.DataFrame): датафрейм с отфильтрованной по проекту базой данных
        """
        project_data = self.data.query("Project == @project")
        return project_data

    def save_data(self, config: Type[ConfigReader], data: pd.DataFrame) -> None:
        """Сохраняет итоговый отчет.

        :param config (ConfigReader): объект, хранящий информацию о конфигурации отчета
        :param data (pd.DataFrame): датафрейм, подготовленный для записи
        """
        write_datetime = datetime.now()
        write_datetime_str = write_datetime.strftime("%Y%m%d_%H:%M:%S")

        result_columns = config.get_parameter("result_columns")
        result_path = config.get_parameter("result_path")

        if not(os.path.exists(result_path)):
            os.mkdir(result_path)

        data[result_columns].to_csv(
            os.path.join(result_path, f"report_{write_datetime_str}.csv"), index=False
        )
