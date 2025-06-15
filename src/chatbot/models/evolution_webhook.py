from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class MessageKey(BaseModel):
    remote_jid: str = Field(..., alias="remoteJid")
    from_me: bool = Field(..., alias="fromMe")
    id: str

class DeviceListMetadata(BaseModel):
    recipient_key_hash: str = Field(..., alias="recipientKeyHash")
    recipient_timestamp: str = Field(..., alias="recipientTimestamp")


class MessageContextInfo(BaseModel):
    device_list_metadata: Optional[DeviceListMetadata] = Field(None, alias="deviceListMetadata")
    device_list_metadata_version: Optional[int] = Field(None, alias="deviceListMetadataVersion")
    message_secret: Optional[str] = Field(None, alias="messageSecret")

class AudioMessage(BaseModel):
    url: str
    mimetype: str
    file_sha256: str = Field(..., alias="fileSha256")
    file_length: str = Field(..., alias="fileLength")
    seconds: int
    ptt: bool
    media_key: str = Field(..., alias="mediaKey")
    file_enc_sha256: str = Field(..., alias="fileEncSha256")
    direct_path: str = Field(..., alias="directPath")
    media_key_timestamp: str = Field(..., alias="mediaKeyTimestamp")
    waveform: str

class Message(BaseModel):
    conversation: Optional[str] = None
    message_context_info: Optional[MessageContextInfo] = Field(None, alias="messageContextInfo")
    audio_message: Optional[AudioMessage] = Field(None, alias="audioMessage")

class WebhookData(BaseModel):
    key: MessageKey
    push_name: str = Field(..., alias="pushName")
    status: str
    message: Message
    message_type: str = Field(..., alias="messageType")
    message_timestamp: int = Field(..., alias="messageTimestamp")
    instance_id: str = Field(..., alias="instanceId")
    source: str

class WebhookPayload(BaseModel):
    event: Literal["messages.upsert"]
    instance: str
    data: WebhookData
    destination: str
    date_time: datetime = Field(..., alias="date_time")
    sender: str
    server_url: str = Field(..., alias="server_url")
    apikey: str
