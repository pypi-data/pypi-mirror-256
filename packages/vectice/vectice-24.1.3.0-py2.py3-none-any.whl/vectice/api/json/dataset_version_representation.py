from __future__ import annotations

from typing import TYPE_CHECKING

from vectice.api._utils import read_nodejs_date
from vectice.api.json.json_type import TJSON

if TYPE_CHECKING:
    from datetime import datetime


class DatasetVersionRepresentationOutput(TJSON):
    @property
    def created_date(self) -> datetime | None:
        return read_nodejs_date(str(self["createdDate"]))

    @property
    def updated_date(self) -> datetime | None:
        return read_nodejs_date(str(self["updatedDate"]))

    @property
    def id(self) -> str:
        return str(self["vecticeId"])

    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def dataset_name(self) -> str | None:
        if "dataSet" in self:
            return str(self["dataSet"]["name"])
        return None

    @property
    def description(self) -> str | None:
        return str(self["description"]) if self["description"] else None

    @property
    def project_id(self) -> str | None:
        if "dataSet" in self:
            return str(self["dataSet"]["project"]["vecticeId"])
        return None
