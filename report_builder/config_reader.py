import yaml
import argparse
from typing import Union


class ConfigReader:
    def __init__(self, yaml_file: str) -> None:
        """
        Класс, объединяющий методы чтения конфигурации и входных параметров.
        config - словарь с параметрами конфигурации:
            - result_path
            - result_columns
            - data_path
            - data_file
            - log_file
        """
        with open(yaml_file, "r") as f:
            self.config = yaml.safe_load(f)

    def get_parameter(self, parameter_name: str) -> Union[str, list]:
        """Отдает значение параметра конфигурации по его имени.

        :param parameter_name (str): название параметра
        :return (Union[str,list]): значение параметра
        """
        return self.config[parameter_name]

    def get_project(self) -> str:
        """Отдает название проекта, полученное при запуске программы.

        :return project (str): название проекта
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--project",
            type=str,
            required=True,
            help="""
            Project name for building report (in brackets).
            Example: 'cfDNA Fusions'
            """,
        )
        args = parser.parse_args()
        project = args.project
        return project
