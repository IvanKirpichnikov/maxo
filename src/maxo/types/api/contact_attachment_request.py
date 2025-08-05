from typing import Self

from maxo.omit import Omittable, Omitted
from maxo.types.api.contact_attachment_request_payload import ContactAttachmentRequestPayload
from maxo.types.base import MaxoType


class ContactAttachmentRequest(MaxoType):
    """
    Запрос на прикрепление контакта.

    Args:
        payload: Полезная нагрузка для запроса прикрепления контакта.

    """

    payload: ContactAttachmentRequestPayload

    @classmethod
    def factory(
        cls,
        name: str | None = None,
        contact_id: Omittable[int | None] = Omitted(),
        vcf_info: Omittable[str | None] = Omitted(),
        vcf_phone: Omittable[str | None] = Omitted(),
    ) -> Self:
        """
        Фабричный метод.

        Args:
            name: Имя контакта.
            contact_id: ID контакта, если он зарегистирован в MAX.
            vcf_info: Полная информация о контакте в формате VCF.
            vcf_phone: Телефон контакта в формате VCF.

        """
        return cls(
            payload=ContactAttachmentRequestPayload(
                name=name,
                contact_id=contact_id,
                vcf_info=vcf_info,
                vcf_phone=vcf_phone,
            ),
        )
