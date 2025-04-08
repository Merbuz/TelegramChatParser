from app.bot.callback_query.factory.callback_query_builder import CallbackData


class ExampleData(CallbackData, prefix="example"):
    data: int
