from maxo.types.api.audio_attachment_request import AudioAttachmentRequest
from maxo.types.api.contact_attachment_request import ContactAttachmentRequest
from maxo.types.api.file_attachment_request import FileAttachmentRequest
from maxo.types.api.image_attachment_request import ImageAttachmentRequest
from maxo.types.api.inline_keyboard_attachment_request import InlineKeyboardAttachmentRequest
from maxo.types.api.location_attachment_request import LocationAttachmentRequest
from maxo.types.api.share_attachment_request import ShareAttachmentRequest
from maxo.types.api.sticker_attachment_request import StickerAttachmentRequest
from maxo.types.api.video_attachment_request import VideoAttachmentRequest

MediaAttachmentsRequests = (
    ImageAttachmentRequest | VideoAttachmentRequest | AudioAttachmentRequest | FileAttachmentRequest
)

AttachmentsRequests = (
    MediaAttachmentsRequests
    | StickerAttachmentRequest
    | ContactAttachmentRequest
    | InlineKeyboardAttachmentRequest
    | LocationAttachmentRequest
    | ShareAttachmentRequest
)
