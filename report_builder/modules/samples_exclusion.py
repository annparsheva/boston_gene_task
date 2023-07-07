import logging
import numpy as np
import pandas as pd


class SamplesExclusion:
    def __init__(self, data: pd.DataFrame) -> None:
        """
        Модуль, исключающий образцы из отчета, если у них не заполнено
        хотябы одно из значений
            'Library construction kit',
            'Library prob set kit',
            'Extraction kit'.
        Для пропущенных значений добавляется запись в лог
        'Заполните {имя пустого поля} для {имя библиотеки LIBxxxxxx}'.

        data - датафрейм для фильтрации и поиска пропущенных значений
        """
        self.data = data

    def make_empty_data_report(self) -> None:
        """Добавляет запись о пропусках в лог."""
        report_data = pd.melt(
            self.data,
            id_vars="Library Lab_ID \n(unique)",
            value_vars=[
                "Library construction kit",
                "Library prob set kit",
                "Extraction kit",
            ],
        )
        report_data = report_data[report_data["value"].isna()].drop_duplicates()
        report = (
            report_data.groupby("Library Lab_ID \n(unique)")["variable"]
            .apply(lambda x: "','".join(x))
            .reset_index()
        )

        for row in report.iterrows():
            library = row[1]["Library Lab_ID \n(unique)"]
            empty_fields = row[1]["variable"]
            logging.warning(f"Заполните '{empty_fields}' для {library}.")

    def filter_empty_data(self) -> pd.DataFrame:
        """
        Отдает отфильтрованный датафрейм без образцов с пропусками.
        
        :return filtered_data (pd.DataFrame): датафрейм, где исключены
        образцы с пропусками
        """
        self.data["Extraction kit"] = self.data["Extraction kit"].replace(
            "Unknown", np.nan
        )

        filtered_data = self.data[
            self.data[
                ["Library construction kit", "Library prob set kit", "Extraction kit"]
            ]
            .notnull()
            .all(1)
        ]

        return filtered_data
