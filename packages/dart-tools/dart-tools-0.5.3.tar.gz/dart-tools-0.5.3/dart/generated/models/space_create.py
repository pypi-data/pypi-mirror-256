import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.color_name import ColorName
from ..models.cycle_mode import CycleMode
from ..models.icon_kind import IconKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="SpaceCreate")


@_attrs_define
class SpaceCreate:
    """
    Attributes:
        duid (str):
        order (str):
        drafter_duid (Union[Unset, None, str]):
        accessible_by_team (Union[Unset, bool]):
        accessible_by_user_duids (Union[Unset, List[str]]):
        title (Union[Unset, str]):
        abrev (Union[Unset, str]):
        description (Union[Unset, str]):
        icon_kind (Union[Unset, IconKind]): * `None` - NONE
            * `Icon` - ICON
            * `Emoji` - EMOJI
        icon_name_or_emoji (Union[Unset, str]):
        color_name (Union[Unset, ColorName]): * `Red` - RED
            * `Dark Blue` - DARK_BLUE
            * `Dark Orange` - DARK_ORANGE
            * `Dark Green` - DARK_GREEN
            * `Purple` - PURPLE
            * `Dark Teal` - DARK_TEAL
            * `Pink` - PINK
            * `Orange` - ORANGE
            * `Green` - GREEN
            * `Yellow` - YELLOW
            * `Brown` - BROWN
            * `Dark Red` - DARK_RED
            * `Flat Green` - FLAT_GREEN
            * `Red Orange` - RED_ORANGE
            * `Teal` - TEAL
            * `Light Green` - LIGHT_GREEN
            * `Light Blue` - LIGHT_BLUE
            * `Light Purple` - LIGHT_PURPLE
            * `Light Orange` - LIGHT_ORANGE
            * `Light Pink` - LIGHT_PINK
            * `Tan` - TAN
            * `Dark Gray` - DARK_GRAY
            * `Light Brown` - LIGHT_BROWN
            * `Light Gray` - LIGHT_GRAY
        cycle_mode (Union[Unset, CycleMode]): * `None` - NONE
            * `ANBA` - ANBA
        standup_recurrence (Union[Unset, Any]):
        standup_recurrs_next_at (Union[Unset, None, datetime.datetime]):
        changelog_recurrence (Union[Unset, Any]):
        changelog_recurrs_next_at (Union[Unset, None, datetime.datetime]):
    """

    duid: str
    order: str
    drafter_duid: Union[Unset, None, str] = UNSET
    accessible_by_team: Union[Unset, bool] = UNSET
    accessible_by_user_duids: Union[Unset, List[str]] = UNSET
    title: Union[Unset, str] = UNSET
    abrev: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    icon_kind: Union[Unset, IconKind] = UNSET
    icon_name_or_emoji: Union[Unset, str] = UNSET
    color_name: Union[Unset, ColorName] = UNSET
    cycle_mode: Union[Unset, CycleMode] = UNSET
    standup_recurrence: Union[Unset, Any] = UNSET
    standup_recurrs_next_at: Union[Unset, None, datetime.datetime] = UNSET
    changelog_recurrence: Union[Unset, Any] = UNSET
    changelog_recurrs_next_at: Union[Unset, None, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        duid = self.duid
        order = self.order
        drafter_duid = self.drafter_duid
        accessible_by_team = self.accessible_by_team
        accessible_by_user_duids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.accessible_by_user_duids, Unset):
            accessible_by_user_duids = self.accessible_by_user_duids

        title = self.title
        abrev = self.abrev
        description = self.description
        icon_kind: Union[Unset, str] = UNSET
        if not isinstance(self.icon_kind, Unset):
            icon_kind = self.icon_kind.value

        icon_name_or_emoji = self.icon_name_or_emoji
        color_name: Union[Unset, str] = UNSET
        if not isinstance(self.color_name, Unset):
            color_name = self.color_name.value

        cycle_mode: Union[Unset, str] = UNSET
        if not isinstance(self.cycle_mode, Unset):
            cycle_mode = self.cycle_mode.value

        standup_recurrence = self.standup_recurrence
        standup_recurrs_next_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.standup_recurrs_next_at, Unset):
            standup_recurrs_next_at = self.standup_recurrs_next_at.isoformat() if self.standup_recurrs_next_at else None

        changelog_recurrence = self.changelog_recurrence
        changelog_recurrs_next_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.changelog_recurrs_next_at, Unset):
            changelog_recurrs_next_at = (
                self.changelog_recurrs_next_at.isoformat() if self.changelog_recurrs_next_at else None
            )

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "duid": duid,
                "order": order,
            }
        )
        if drafter_duid is not UNSET:
            field_dict["drafterDuid"] = drafter_duid
        if accessible_by_team is not UNSET:
            field_dict["accessibleByTeam"] = accessible_by_team
        if accessible_by_user_duids is not UNSET:
            field_dict["accessibleByUserDuids"] = accessible_by_user_duids
        if title is not UNSET:
            field_dict["title"] = title
        if abrev is not UNSET:
            field_dict["abrev"] = abrev
        if description is not UNSET:
            field_dict["description"] = description
        if icon_kind is not UNSET:
            field_dict["iconKind"] = icon_kind
        if icon_name_or_emoji is not UNSET:
            field_dict["iconNameOrEmoji"] = icon_name_or_emoji
        if color_name is not UNSET:
            field_dict["colorName"] = color_name
        if cycle_mode is not UNSET:
            field_dict["cycleMode"] = cycle_mode
        if standup_recurrence is not UNSET:
            field_dict["standupRecurrence"] = standup_recurrence
        if standup_recurrs_next_at is not UNSET:
            field_dict["standupRecurrsNextAt"] = standup_recurrs_next_at
        if changelog_recurrence is not UNSET:
            field_dict["changelogRecurrence"] = changelog_recurrence
        if changelog_recurrs_next_at is not UNSET:
            field_dict["changelogRecurrsNextAt"] = changelog_recurrs_next_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        duid = d.pop("duid")

        order = d.pop("order")

        drafter_duid = d.pop("drafterDuid", UNSET)

        accessible_by_team = d.pop("accessibleByTeam", UNSET)

        accessible_by_user_duids = cast(List[str], d.pop("accessibleByUserDuids", UNSET))

        title = d.pop("title", UNSET)

        abrev = d.pop("abrev", UNSET)

        description = d.pop("description", UNSET)

        _icon_kind = d.pop("iconKind", UNSET)
        icon_kind: Union[Unset, IconKind]
        if isinstance(_icon_kind, Unset):
            icon_kind = UNSET
        else:
            icon_kind = IconKind(_icon_kind)

        icon_name_or_emoji = d.pop("iconNameOrEmoji", UNSET)

        _color_name = d.pop("colorName", UNSET)
        color_name: Union[Unset, ColorName]
        if isinstance(_color_name, Unset):
            color_name = UNSET
        else:
            color_name = ColorName(_color_name)

        _cycle_mode = d.pop("cycleMode", UNSET)
        cycle_mode: Union[Unset, CycleMode]
        if isinstance(_cycle_mode, Unset):
            cycle_mode = UNSET
        else:
            cycle_mode = CycleMode(_cycle_mode)

        standup_recurrence = d.pop("standupRecurrence", UNSET)

        _standup_recurrs_next_at = d.pop("standupRecurrsNextAt", UNSET)
        standup_recurrs_next_at: Union[Unset, None, datetime.datetime]
        if _standup_recurrs_next_at is None:
            standup_recurrs_next_at = None
        elif isinstance(_standup_recurrs_next_at, Unset):
            standup_recurrs_next_at = UNSET
        else:
            standup_recurrs_next_at = isoparse(_standup_recurrs_next_at)

        changelog_recurrence = d.pop("changelogRecurrence", UNSET)

        _changelog_recurrs_next_at = d.pop("changelogRecurrsNextAt", UNSET)
        changelog_recurrs_next_at: Union[Unset, None, datetime.datetime]
        if _changelog_recurrs_next_at is None:
            changelog_recurrs_next_at = None
        elif isinstance(_changelog_recurrs_next_at, Unset):
            changelog_recurrs_next_at = UNSET
        else:
            changelog_recurrs_next_at = isoparse(_changelog_recurrs_next_at)

        space_create = cls(
            duid=duid,
            order=order,
            drafter_duid=drafter_duid,
            accessible_by_team=accessible_by_team,
            accessible_by_user_duids=accessible_by_user_duids,
            title=title,
            abrev=abrev,
            description=description,
            icon_kind=icon_kind,
            icon_name_or_emoji=icon_name_or_emoji,
            color_name=color_name,
            cycle_mode=cycle_mode,
            standup_recurrence=standup_recurrence,
            standup_recurrs_next_at=standup_recurrs_next_at,
            changelog_recurrence=changelog_recurrence,
            changelog_recurrs_next_at=changelog_recurrs_next_at,
        )

        space_create.additional_properties = d
        return space_create

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
