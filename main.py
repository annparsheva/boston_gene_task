import sys
import logging

from data_loader import DataLoader
from config_reader import ConfigReader

from modules.qc_test import QCTest
from modules.samples_exclusion import SamplesExclusion
from modules.get_reseq_top_off import GetReseqTopOff


def main():
    config = ConfigReader("report_building_config.yaml")

    logging.basicConfig(
        filename=config.get_parameter("log_file"),
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    data_loader = DataLoader(
        config.get_parameter("data_path"), config.get_parameter("data_file")
    )
    project = config.get_project()

    logging.info(f"Загрузка отчета для проекта '{project}' начата")

    # Read data
    data_loader.init_db()

    # Get project and filter data
    project_data = data_loader.get_project_data(project)

    if project_data.empty:
        logging.error("Не верно указано имя проекта")
        sys.exit(1)
    else:
        # Fill reseq/top-off columns
        get_reseq_top_off_module = GetReseqTopOff(project_data)
        labeled_project_data = get_reseq_top_off_module.get_reseq_top_off()

        # Add qc test result column
        qc_test_module = QCTest()
        labeled_project_data = qc_test_module.add_qc_test_column(labeled_project_data)

        # Clear None values
        sample_exclusion_module = SamplesExclusion(labeled_project_data)
        filtered_data = sample_exclusion_module.filter_empty_data()
        sample_exclusion_module.make_empty_data_report()

        # Make report
        if filtered_data.empty:
            logging.warning("Не найдено записей для добавления в отчет")
            sys.exit(1)
        else:
            data_loader.save_data(config, filtered_data)

        logging.info("Загрузка отчета завершена")


if __name__ == "__main__":
    main()
