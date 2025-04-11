from app.bot.callback_query.factory.callback_query_builder import CallbackData


class KeywordData(CallbackData, prefix="keyword"):
    word: str


class KeywordParse(CallbackData, prefix="kw_parse"):
    word: str


class KeywordRemove(CallbackData, prefix="kw_remove"):
    word: str


class PublicChatData(CallbackData, prefix="public_chat"):
    id: int


class PublicChatParse(CallbackData, prefix="pubc_parse"):
    id: int


class PublicChatRemove(CallbackData, prefix="pubc_remove"):
    id: int


class PrivateChatData(CallbackData, prefix="private_chat"):
    id: int


class PrivateChatParse(CallbackData, prefix="prc_parse"):
    id: int


class PrivateChatRemove(CallbackData, prefix="prc_remove"):
    id: int
