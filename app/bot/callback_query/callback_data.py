from app.bot.callback_query.factory.callback_query_builder import CallbackData


class KeywordData(CallbackData, prefix="keyword"):
    word: str


class KeywordParse(CallbackData, prefix="kw_parse"):
    word: str


class KeywordRemove(CallbackData, prefix="kw_remove"):
    word: str


class ChatData(CallbackData, prefix="chat"):
    link: str


class ChatRemove(CallbackData, prefix="ct_remove"):
    link: str


class SessionData(CallbackData, prefix="session"):
    name: str


class SessionRemove(CallbackData, prefix="sn_remove"):
    name: str
