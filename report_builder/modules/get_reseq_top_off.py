import pandas as pd


class GetReseqTopOff:
    def __init__(self, data: pd.DataFrame) -> None:
        """
        Модуль выставления флагов reseq/top-off.
        data - датафрейм с данными для проставления лейблов
        """
        self.data = data

    def group_and_count_samples(self) -> None:
        """
        Группирует и выполняет подсчет количества образцов
        для экстракта и библиотеки.
        """
        self.data["sample_by_extract"] = self.data.groupby(["Extract BG_ID"])[
            "Sample sheet_Sample_ID"
        ].transform("nunique")
        self.data["sample_by_library"] = self.data.groupby(
            ["Extract BG_ID", "Library Lab_ID \n(unique)"]
        )["Sample sheet_Sample_ID"].transform("nunique")

    def get_group(self, reseq: str, top_off: str, condition: str) -> pd.DataFrame:
        """
        Определяет данные по каждой группе (reseq, top-off, ничего).
        Проставляет лейблы для столбцов 'Is it reseq?', 'Is it top off seq?'.

        :param reseq (str): переподготовка библиотеки, возможные значения: 'Yes','No'
        :param top_off (str): 'доливка' библиотеки, возможные значения: 'Yes','No'
        :param condition (str): условие определения группы, возможные значения:
            - reseq : 'sample_by_extract > 1 & sample_by_library == 1'
            - top-off : 'sample_by_library > 1'
            - other : 'sample_by_extract == 1'
        :return (pd.DataFrame): датафрейм с проставленными лейблами для одной из групп
        """
        group = self.data.query(condition)
        group[["Is it reseq?", "Is it top off seq?"]] = [reseq, top_off]

        if reseq == "Yes" or top_off == "Yes":
            group["Sample target"] = group["Sample sheet_Sample_ID"]
            group["Sample sheet_Sample_ID"] = group["Sample sheet_Sample_ID"] + "2"
        else:
            group["Sample target"] = "No"

        return group

    def get_reseq_top_off(self) -> pd.DataFrame:
        """
        Отдает датафрейм с проставленными лейблами по каждой из групп.

        :return (pd.DataFrame): датафрейм с проставленными лейблами reseq и top-off
        """
        self.group_and_count_samples()

        reseq = self.get_group(
            reseq="Yes",
            top_off="No",
            condition="sample_by_extract > 1 & sample_by_library == 1",
        )
        top_off = self.get_group(
            reseq="No", top_off="Yes", condition="sample_by_library > 1"
        )
        other = self.get_group(
            reseq="No", top_off="No", condition="sample_by_extract == 1"
        )
        result = pd.concat([reseq, top_off, other])
        return result
