from maxo.types.api.audio_attachment import AudioAttachment
from maxo.types.api.contact_attachment import ContactAttachment
from maxo.types.api.file_attachment import FileAttachment
from maxo.types.api.image_attachment import ImageAttachment
from maxo.types.api.keyboard import Keyboard
from maxo.types.api.location_attachment import LocationAttachment
from maxo.types.api.share_attachment import ShareAttachment
from maxo.types.api.sticker_attachment import StickerAttachment
from maxo.types.api.video_attachment import VideoAttachment

Attachments = (
    ImageAttachment
    | VideoAttachment
    | AudioAttachment
    | FileAttachment
    | StickerAttachment
    | ContactAttachment
    | Keyboard
    | ShareAttachment
    | LocationAttachment
)
