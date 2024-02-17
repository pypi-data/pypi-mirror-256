from datetime import datetime
from typing import Any

import httpx
from PIL import Image
from pydantic import Base64Str, BaseModel, ConfigDict, Field, HttpUrl, computed_field

from maplestory.apis.guild import get_basic_info_by_id, get_guild_id
from maplestory.models.guild import GuildBasic
from maplestory.models.guild.basic import GuildSkill
from maplestory.utils.image import get_image_from_base64str, get_image_from_url
from maplestory.utils.kst import yesterday
from maplestory.utils.number import korean_format_number


class Guild(BaseModel):
    name: str = Field(frozen=True)
    world: str = Field(frozen=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @computed_field
    def id(self) -> str:
        return get_guild_id(self.name, self.world)

    @property
    def oguild_id(self) -> str:
        return self.id

    @computed_field(repr=False)
    def basic(self) -> GuildBasic:
        return get_basic_info(self.name, self.world)

    @computed_field
    def level(self) -> int:
        return self.basic.level

    @computed_field
    def point(self) -> int:
        return self.basic.point

    @computed_field
    def point_str(self) -> int:
        return korean_format_number(self.point)

    @computed_field
    def fame(self) -> int:
        return self.basic.fame

    @computed_field
    def fame_str(self) -> int:
        return korean_format_number(self.fame)

    @computed_field
    def member_count(self) -> int:
        return self.basic.member_count

    @computed_field
    def member_names(self) -> list[str]:
        return self.basic.members

    # @computed_field
    # def members(self) -> list[str]:
    #     # TODO: Add character model
    #     return self.basic.members

    @computed_field
    def master_name(self) -> str:
        return self.basic.master_name

    # @computed_field
    # def master(self) -> str:
    #     # TODO: Add character model
    #     return self.basic.master_name

    # @computed_field
    # def master_character(self) -> str:
    #     # TODO: Add character model
    #     return self.basic.master_character

    @computed_field
    def skills(self) -> list[GuildSkill]:
        return self.basic.skills

    @computed_field
    def noblesse_skills(self) -> list[GuildSkill]:
        return self.basic.noblesse_skills

    # "guild_mark": null,
    # "guild_mark_custom": null

    # "guild_mark": "https://open.api.nexon.com/static/maplestory/GuildMark/HMIKJCPEKA.png",
    # "guild_mark_custom": null

    # "guild_mark": None,
    # "guild_mark_custom": "iVBORw0KGgoAAAANSUhEUgAAABEAAAARCAYAAAA7bUf6AAAACXBIWXMAAA7EAAAOxAGVKw4bAAACX0lEQVQ4jX2UPWgUQRiGn2+5QoJFSGEh4SpJQCSYZEawEAuLVIpiAilPLqB32bOXFGJhZaW37IEWiRAwkIiNiFpZSIr7Rk4OUaIiclwhFhIsgkXYsdjZy5nCqXZ2vnnmfd/5Ee89w82Y+qZz6cJBvzYGjANR/kcyoO9c+quoiQ4BKs6l88bUN4cAZWAGqIJUw/d4UQMghRJj6k3n0nhIQQI8yifJnHPpYqh7KBI9Bt6rJnv/KHEubRhT2wqAa8BtkGMg086li8bU2wAiURk4Dhy1Nn42gBhTq+Sg1oIxtS3nWmsgJ4GJYAeRqBvW+wPsA/uqyRWAyJhaxbnW6jAoFB8BJp1LL1sbt4ei6wPfQS4NgnWutWZMrQpsGFMvBd9TwESQDtBVTZasjV+DvAO5qtq8Y22jBSCzszfGQIotzIDfItEJ4KJqctPauK2anMnVyBNgRLV5PdjsWRuvlAJgBjgvEnWAXWAyhEcOaLwFeQq8Ad+zNu6pJnetjVdUk/UoKJh1Lq0A54A5YEI1mQewtvEcGABUk8EhG5wTY5ZPA1XVJD48aG1jA/gJvpOHyS6A91kGTDmXrhtTvy/GLE8FO9O5BdlVbS5Z22iD7wKjYfJeAETAJ+BzvgD9UtiyW8ArEMIkwHdVk6XD6sLubYXcOoWdCORUUDOn2lw8sBNve599LFQAI8Coc+l8gD0AVksgRbhnC4C18Qvgq/fZTlDaC5Ay+eX7EfodICsBGXiAHWvjb8BL77MvwAeR6J732YXi2htT75E/C9sBkgF98d5jbVwOgxPeZ3shtN7wm/G/9heAAv9DLXHWKgAAAABJRU5ErkJggg==",

    # @computed_field(repr=False)
    # def mark(self) -> HttpUrl | Base64Str | None:
    #     return self.basic.mark or self.basic.custom_mark

    @computed_field
    def mark(self) -> Image.Image | None:
        if self.basic.mark:
            return get_image_from_url(self.basic.mark)
        elif self.basic.custom_mark:
            return get_image_from_base64str(self.basic.custom_mark)
        return None

    @computed_field
    def is_custom_mark(self) -> bool:
        return self.basic.custom_mark is not None


def get_basic_info(
    guild_name: str,
    world_name: str,
    date: datetime = yesterday(),
) -> GuildBasic:
    """
    길드 기본 정보를 조회합니다.
    Fetches the basic information of the guild.

    Args:
        guild_name : 길드 명. The name of the guild.
        world_name : 월드 명. The name of the world.
        date : 조회 기준일(KST). Reference date for the query (KST).

    Returns:
        GuildBasic: 길드의 기본 정보. The basic information of the guild.
    """

    guild_id = get_guild_id(guild_name, world_name)
    return get_basic_info_by_id(guild_id, date)


def get_basic_info_in_details(
    guild_name: str,
    world_name: str,
    date: datetime = yesterday(),
) -> GuildBasic:
    """
    길드 기본 정보를 조회합니다.
    Fetches the basic information of the guild.

    Args:
        guild_name : 길드명. The name of the guild.
        world_name : 월드명. The name of the world.
        date : 조회 기준일(KST). Reference date for the query (KST).

    Returns:
        GuildBasic: 길드의 기본 정보. The basic information of the guild.
    """

    guild_basic: GuildBasic = get_basic_info(guild_name, world_name, date)

    from maplestory.services.character import get_basic_character_info

    # Add master character info
    guild_basic.master = get_basic_character_info(guild_basic.master_name, date)

    # TODO: Add members character info

    return guild_basic
