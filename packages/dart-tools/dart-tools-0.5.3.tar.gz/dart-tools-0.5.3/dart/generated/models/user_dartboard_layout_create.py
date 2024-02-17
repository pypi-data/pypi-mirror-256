from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UserDartboardLayoutCreate")


@_attrs_define
class UserDartboardLayoutCreate:
    """
    Attributes:
        user_duid (str):
        dartboard_duid (str):
        layout_duid (str):
    """

    user_duid: str
    dartboard_duid: str
    layout_duid: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_duid = self.user_duid
        dartboard_duid = self.dartboard_duid
        layout_duid = self.layout_duid

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "userDuid": user_duid,
                "dartboardDuid": dartboard_duid,
                "layoutDuid": layout_duid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_duid = d.pop("userDuid")

        dartboard_duid = d.pop("dartboardDuid")

        layout_duid = d.pop("layoutDuid")

        user_dartboard_layout_create = cls(
            user_duid=user_duid,
            dartboard_duid=dartboard_duid,
            layout_duid=layout_duid,
        )

        user_dartboard_layout_create.additional_properties = d
        return user_dartboard_layout_create

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
