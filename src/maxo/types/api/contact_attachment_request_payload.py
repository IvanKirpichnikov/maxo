from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class ContactAttachmentRequestPayload(MaxoType):
    """
    Полезная нагрузка для запроса прикрепления контакта.

    Args:
        name: Имя контакта.
        contact_id: ID контакта, если он зарегистирован в MAX.
        vcf_info: Полная информация о контакте в формате VCF.
        vcf_phone: Телефон контакта в формате VCF.

    """

    name: str | None = None
    contact_id: Omittable[int | None] = Omitted()
    vcf_info: Omittable[str | None] = Omitted()
    vcf_phone: Omittable[str | None] = Omitted()
