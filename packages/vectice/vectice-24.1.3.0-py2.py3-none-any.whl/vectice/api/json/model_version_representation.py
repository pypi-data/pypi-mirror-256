from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vectice.api._utils import read_nodejs_date
from vectice.api.json.json_type import TJSON
from vectice.api.json.model_version import ModelVersionStatus

if TYPE_CHECKING:
    from datetime import datetime


class ModelVersionUpdateInput(TJSON):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    @property
    def status(self) -> ModelVersionStatus:
        return ModelVersionStatus[str(self["status"])]


class ModelVersionRepresentationOutput(TJSON):
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
    def model_name(self) -> str | None:
        if "model" in self:
            return str(self["model"]["name"])
        return None

    @property
    def status(self) -> ModelVersionStatus:
        return ModelVersionStatus[self["status"]]

    @property
    def description(self) -> str | None:
        return str(self["description"]) if self["description"] else None

    @property
    def technique(self) -> str | None:
        return str(self["algorithmName"]) if self["algorithmName"] else None

    @property
    def library(self) -> str | None:
        return str(self["framework"]) if self["framework"] else None

    @property
    def project_id(self) -> str | None:
        if "model" in self:
            return str(self["model"]["project"]["vecticeId"])
        return None
