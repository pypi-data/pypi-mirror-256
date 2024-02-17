from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, computed_field

from maplestory.apis.guild import get_basic_info_by_id, get_guild_id
from maplestory.models.guild import GuildBasic
from maplestory.models.guild.basic import GuildSkill
from maplestory.utils.kst import yesterday


class Guild(BaseModel):
    name: str = Field(frozen=True)
    world: str = Field(frozen=True)

    def model_post_init(self, __context: Any) -> None:
        basic_info = get_basic_info(self.name, self.world)
        # basic 속성의 모든 필드를 반복하며 상위 객체에 설정합니다.
        for field_name in basic_info.model_fields_set:
            value = getattr(basic_info, field_name)
            setattr(self, field_name, value)

        # Value error, "Guild" object has no field "date" [type=value_error, input_value={'name': '리더', 'world': '스카니아'}, input_type=dict]
        # 이런 에러가 발생함.
        # 모든 등록하려는 attributes를 미리 name, world 밑에 등록해놔야 하는 건데,
        # 그러면 그냥 property 추가하는 것과 다를 바 없어짐.

    # @computed_field
    # def id(self) -> str:
    #     return get_guild_id(self.name, self.world)

    # def oguild_id(self) -> str:
    #     return self.id

    # @computed_field(repr=False)
    # def basic(self) -> GuildBasic:
    #     return get_basic_info(self.name, self.world)

    # @property
    # def level(self) -> int:
    #     return self.basic.level

    # @property
    # def point(self) -> int:
    #     return self.basic.point

    # @property
    # def fame(self) -> int:
    #     return self.basic.fame

    # @property
    # def member_count(self) -> int:
    #     return self.basic.member_count

    # @property
    # def members(self) -> list[str]:
    #     # TODO: Add character model
    #     return self.basic.members

    # @property
    # def master_name(self) -> str:
    #     return self.basic.master_name

    # @property
    # def master(self) -> str:
    #     # TODO: Add character model
    #     return self.basic.master_name

    # @property
    # def master_character(self) -> str:
    #     # TODO: Add character model
    #     return self.basic.master_character

    # @property
    # def skills(self) -> list[GuildSkill]:
    #     return self.basic.skills

    # @property
    # def noblesse_skills(self) -> list[GuildSkill]:
    #     return self.basic.noblesse_skills

    # @property
    # def mark(self) -> str:
    #     return self.basic.mark

    # @property
    # def custom_mark(self) -> str:
    #     return self.basic.custom_mark


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
