import numpy as np
import pandas as pd


class QCTest:
    def __init__(self) -> None:
        """
        Модуль, который проставляет в поле “QC” значение pass/failed
        для всех образцов.
        QC для DNA образцов:
            Library concentration от 10 до 100 - pass, иначе failed.
        QC для RNA образцов:
            Library concentration от 15 до 110 - pass, иначе failed.

        dna_borders - границы пройденного теста для DNA образцов
        rna_borders - границы пройденного теста для RNA образцов
        """
        self.dna_borders = {"start": 10, "end": 99}
        self.rna_borders = {"start": 15, "end": 109}

    def add_qc_test_column(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Добавляет столбец QC со значениями pass/failed в зависимости
        от Library concentration.

        :param data (pd.DataFrame): датафрейм с данными образцов,
                                    куда добавляется столбец QC
        :return (pd.DataFrame): датафрейм с проставленными лейблами QC
                                для каждого образца
        """
        data["QC"] = np.select(
            [
                (data["Extract BG_ID"].str[0] == "D")
                & (
                    data["Library Concentration"].between(
                        self.dna_borders["start"], self.dna_borders["end"]
                    )
                )
                | (data["Extract BG_ID"].str[0] == "R")
                & (
                    data["Library Concentration"].between(
                        self.rna_borders["start"], self.rna_borders["end"]
                    )
                )
            ],
            ["pass"],
            default="failed",
        )
        return data
