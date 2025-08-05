from typing import Self

from maxo.omit import Omittable, Omitted
from maxo.types.api.contact_attachment_payload import ContactAttachmentPayload
from maxo.types.api.user import User
from maxo.types.base import MaxoType
from maxo.types.enums.attachment_type import AttachmentType


class ContactAttachment(MaxoType):
    """
    Вложение контактов.

    Args:
        payload: Содержимо вложения контактов.

    """

    type = AttachmentType.CONTACT

    payload: ContactAttachmentPayload

    @classmethod
    def factory(
        cls,
        vcf_info: Omittable[str | None] = Omitted(),
        max_info: Omittable[User | None] = Omitted(),
    ) -> Self:
        """
        Фабричный метод.

        Args:
            vcf_info: Информация о пользователе в формате VCF.
            max_info: Информация о пользователе.

        """
        return cls(
            payload=ContactAttachmentPayload(
                max_info=max_info,
                vcf_info=vcf_info,
            ),
        )
