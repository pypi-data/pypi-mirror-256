from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast, List
from typing import Union
from ..types import UNSET, Unset


T = TypeVar("T", bound="CreateParticipantGroupJsonBody")


@_attrs_define
class CreateParticipantGroupJsonBody:
    """
    Attributes:
        workspace_id (str): The id of the workspace to create the participant group in
        name (str): The name of the participant group Example: Group 1.
        description (Union[Unset, str]): A description of the participant group Example: Participants with confirmed
            special dietary requirements..
        participant_ids (Union[Unset, List[str]]): The ids of participants to be initially added to the group Example:
            ['5e9b9c9b0f9c9a0001b0b1f4', '5e9b9c9b0f9c9a0001b0b1f5', '5e9b9c9b0f9c9a0001b0b1f6'].
    """

    workspace_id: str
    name: str
    description: Union[Unset, str] = UNSET
    participant_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        name = self.name
        description = self.description
        participant_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.participant_ids, Unset):
            participant_ids = self.participant_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspace_id": workspace_id,
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if participant_ids is not UNSET:
            field_dict["participant_ids"] = participant_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        name = d.pop("name")

        description = d.pop("description", UNSET)

        participant_ids = cast(List[str], d.pop("participant_ids", UNSET))

        create_participant_group_json_body = cls(
            workspace_id=workspace_id,
            name=name,
            description=description,
            participant_ids=participant_ids,
        )

        create_participant_group_json_body.additional_properties = d
        return create_participant_group_json_body

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
