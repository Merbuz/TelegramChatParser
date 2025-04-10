from app.bot.callback_query.factory.callback_query_builder import CallbackData


class KeywordData(CallbackData, prefix="keyword"):
    word: str
