from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from maplestory.types.character import AbilityNumber

from ..types import Grade, PresetNumber


class AbilityInfoItem(BaseModel):
    """어빌리티 한 줄 정보

    Attributes:
        number (int): 어빌리티 번호 (몇 번째 줄인지)
        grade (str): 어빌리티 등급
        value (str): 어빌리티 옵션 및 수치
    """

    number: AbilityNumber = Field(alias="ability_no", repr=False)
    grade: Grade = Field(alias="ability_grade")
    value: str = Field(alias="ability_value")


class AbilityPreset(BaseModel):
    """어빌리티 프리셋 정보

    Attributes:
        grade (str): 어빌리티 프리셋의 어빌리티 등급
        info (list[AbilityInfoItem]): 어빌리티 프리셋 정보
    """

    grade: Grade = Field(alias="ability_preset_grade")
    info: list[AbilityInfoItem] = Field(alias="ability_info")

    def model_post_init(self, __context: Any) -> None:
        self.info = sorted(self.info, key=lambda x: x.number)


class Ability(BaseModel):
    """어빌리티 정보

    Attributes:
        date (datetime): 조회 기준일 (KST, 일 단위 데이터로 시, 분은 일괄 0으로 표기)
        grade (Grade): 어빌리티 등급
        info (list[AbilityInfoItem]): 어빌리티 정보
        remain_fame (int): 보유 명성치
        preset_no (PresetNumber): 적용 중인 어빌리티 프리셋 번호(number)
        preset1 (AbilityPreset): 어빌리티 1번 프리셋 정보
        preset2 (AbilityPreset): 어빌리티 2번 프리셋 정보
        preset3 (AbilityPreset): 어빌리티 3번 프리셋 정보
    """

    date: datetime = Field(repr=False)
    grade: Grade = Field(alias="ability_grade")
    info: list[AbilityInfoItem] = Field(alias="ability_info")
    remain_fame: int
    preset_no: PresetNumber
    preset1: AbilityPreset = Field(alias="ability_preset_1", repr=False)
    preset2: AbilityPreset = Field(alias="ability_preset_2", repr=False)
    preset3: AbilityPreset = Field(alias="ability_preset_3", repr=False)
