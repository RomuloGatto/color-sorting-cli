import csv
from contextlib import AbstractContextManager
from typing import List, Optional, Set, Tuple

from harmony.core.constants import Resources, TableNames
from harmony.core.db_models import HSL, ColorName
from harmony.core.service_layer import RGBToHSLConverter
from harmony.core.utils import ResourceUtils, RGBUtils
from harmony.data_access.adapters import (
    ColorNameRepository,
    DatabaseSession,
    SessionFactory,
    SQLiteSessionFactory,
)
from harmony.data_access.loggers import ColorNamesStorageLogger


class ColorNamesStorage(AbstractContextManager):
    """Provide methods for accessing the color names table in the database"""

    _logger = ColorNamesStorageLogger()

    def __init__(self, session_factory: Optional[SessionFactory] = None):
        self._initialize(session_factory)

    def __enter__(
        self, session_factory: Optional[SessionFactory] = None
    ) -> "ColorNamesStorage":
        self._initialize(session_factory)
        return self

    def _initialize(self, session_factory: Optional[SessionFactory] = None) -> None:
        self._session = self._make_session(session_factory)
        self._repository = ColorNameRepository(self._session)

    def _make_session(
        self, session_factory: Optional[SessionFactory] = None
    ) -> DatabaseSession:
        if session_factory is not None:
            return session_factory.make_session()

        return SQLiteSessionFactory().make_session()

    def __exit__(self, *_args, **_kwargs) -> None:
        self.close()

    def close(self):
        self._session.rollback()
        self._session.close()

    def get_color_name_by_hsl(self, hsl: HSL) -> str:
        """Get the name of the nearest color in database

        Args:
            hsl (HSL): HSL of the color to name

        Returns:
            str: name found
        """
        if self._color_names_were_found(hsl):
            self._logger.log_nearest_color_found(
                hsl, self._get_first_color_data_found(hsl)
            )
            return self._get_first_name_found(hsl)

        self._store()
        return self.get_color_name_by_hsl(hsl)

    def _color_names_were_found(self, hsl: HSL) -> bool:
        return len(self._get_color_names(hsl)) > 0

    def _get_color_names(self, hsl: HSL) -> Set[Tuple[str, ...]]:
        return self._session.execute_query(
            self._get_query_for_finding_the_nearest_color(hsl)
        )

    @staticmethod
    def _get_query_for_finding_the_nearest_color(hsl: HSL) -> str:
        return (
            f"SELECT \n\t{ColorNameRepository.NAME_COLUMN},"
            + f"\n\t{ColorNameRepository.HUE_COLUMN},"
            + f"\n\t{ColorNameRepository.SATURATION_COLUMN},"
            + f"\n\t{ColorNameRepository.LUMINOSITY_COLUMN}"
            + f"\nFROM\n\t{TableNames.COLOR_NAME}"
            + "\nORDER BY"
            + "\n\t("
            + f"(ABS({ColorNameRepository.HUE_COLUMN} - {hsl.hue}) / 360) * 3"
            + ") +"
            + "\n\t("
            + "(ABS("
            + f"{ColorNameRepository.SATURATION_COLUMN} - {hsl.saturation}) / 1.0"
            + ") * 2"
            + ") +"
            + "\n\t("
            + f"ABS({ColorNameRepository.LUMINOSITY_COLUMN} - {hsl.luminosity}) / 1.0"
            + ")"
            + "\nLIMIT 1;"
        )

    def _get_first_name_found(self, hsl: HSL) -> str:
        return self._get_first_color_data_found(hsl)[self._get_name_index_in_row()]

    def _get_first_color_data_found(self, hsl: HSL) -> Tuple[str, ...]:
        return list(self._get_color_names(hsl))[0]

    @staticmethod
    def _get_name_index_in_row() -> int:
        return 0

    @staticmethod
    def _get_hue_index_in_row() -> int:
        return 1

    @staticmethod
    def _get_saturation_index_in_row() -> int:
        return 2

    @staticmethod
    def _get_luminosity_index_in_row() -> int:
        return 3

    def _store(self) -> None:
        with open(
            ResourceUtils.get_resource(Resources.COLOR_NAMES_CSV), "r", encoding="utf8"
        ) as csv_file:
            csv_reader = csv.reader(csv_file)

            for row in csv_reader:
                self._try_to_store_color_name_data(self._make_color_name_data(row))

    def _make_color_name_data(self, csv_row: List[str]) -> ColorName:
        return ColorName(
            self._get_hexcode_from_csv_row(csv_row), self._get_hsl_from_csv_row(csv_row)
        )

    def _get_hsl_from_csv_row(self, csv_row: List[str]) -> HSL:
        return self._get_hsl_from_hexcode(self._get_hexcode_from_csv_row(csv_row))

    def _get_hsl_from_hexcode(self, hexcode: str) -> HSL:
        return RGBToHSLConverter().make_hsl_from_rgb(
            RGBUtils.get_rgb_from_hexcode(hexcode)
        )

    def _get_hexcode_from_csv_row(self, csv_row) -> str:
        return csv_row[self._get_hexcode_index_in_csv()]

    @staticmethod
    def _get_hexcode_index_in_csv() -> int:
        return 0

    @staticmethod
    def _get_name_index_in_csv() -> int:
        return 1

    def _try_to_store_color_name_data(self, color_name_data: ColorName) -> None:
        try:
            self._store_color_name_data(color_name_data)

        except Exception as exception:
            self._logger.warn_error_on_recording_name(color_name_data, exception)

    def _store_color_name_data(self, color_name_data: ColorName) -> None:
        color_name_data.name = color_name_data.name.replace("'", "''")

        self._repository.save(color_name_data)
        self._session.commit()

        self._logger.log_color_name_stored(color_name_data)
