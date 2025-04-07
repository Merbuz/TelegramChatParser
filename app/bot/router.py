from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Callable,
    Optional,
    TypeVar,
    List
)

import pyrogram

if TYPE_CHECKING:
    from pyrogram.filters import Filter
    from pyrogram.handlers.handler import Handler


T = TypeVar("T", bound=Callable)


class Router:
    def __init__(self, name: str):
        self.name = name
        self.handlers: List[Handler] = []

    def on_business_bot_connection(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.business_bot_connection_handler.BusinessBotConnectionHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.business_bot_connection_handler.BusinessBotConnectionHandler(func)  # noqa: E501
                )

            return func

        return wrapper

    def on_callback_query(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.callback_query_handler.CallbackQueryHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.callback_query_handler.CallbackQueryHandler(func)  # noqa: E501
                )

            return func

        return wrapper

    def on_chat_join_request(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.chat_join_request_handler.ChatJoinRequestHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.chat_join_request_handler.ChatJoinRequestHandler(func)  # noqa: E501
                )

            return func

        return wrapper

    def on_chat_member_updated(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.chat_member_updated_handler.ChatMemberUpdatedHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.chat_member_updated_handler.ChatMemberUpdatedHandler(func)  # noqa: E501
                )

            return func

        return wrapper

    def on_chosen_inline_result(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.chosen_inline_result_handler.ChosenInlineResultHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.chosen_inline_result_handler.ChosenInlineResultHandler(func)  # noqa: E501
                )

            return func

        return wrapper

    def on_deleted_messages(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.deleted_messages_handler.DeletedMessagesHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.deleted_messages_handler.DeletedMessagesHandler(func)  # noqa: E501
                )

            return func

        return wrapper

    def on_disconnect(self) -> Callable[[T], T]:
        def wrapper(func: T) -> T:
            self.handlers.append(
                pyrogram.handlers.disconnect_handler.DisconnectHandler(func)
            )

            return func

        return wrapper

    def on_edited_message(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.edited_message_handler.EditedMessageHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.edited_message_handler.EditedMessageHandler(func)  # noqa: E501
                )

            return func

        return wrapper

    def on_inline_query(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.inline_query_handler.InlineQueryHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.inline_query_handler.InlineQueryHandler(func)  # noqa: E501
                )

            return func

        return wrapper

    def on_message(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.message_handler.MessageHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.message_handler.MessageHandler(func)
                )

            return func

        return wrapper

    def on_poll(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.poll_handler.PollHandler(func, filters)
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.poll_handler.PollHandler(func)
                )

            return func

        return wrapper

    def on_raw_update(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.raw_update_handler.RawUpdateHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.raw_update_handler.RawUpdateHandler(func)
                )

            return func

        return wrapper

    def on_user_status(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.user_status_handler.UserStatusHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.user_status_handler.UserStatusHandler(func)  # noqa: E501
                )

            return func

        return wrapper

    def on_message_reaction_updated(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.message_reaction_updated_handler.MessageReactionUpdatedHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.message_reaction_updated_handler.MessageReactionUpdatedHandler(func)  # noqa: E501
                )

            return func

        return wrapper

    def on_message_reaction_count_updated(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.message_reaction_count_updated_handler.MessageReactionCountUpdatedHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.message_reaction_count_updated_handler.MessageReactionCountUpdatedHandler(func)  # noqa: E501
                )

            return func

        return wrapper

    def on_pre_checkout_query(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.pre_checkout_query_handler.PreCheckoutQueryHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.pre_checkout_query_handler.PreCheckoutQueryHandler(func)  # noqa: E501
                )

            return func

        return wrapper

    def on_purchased_paid_media(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.purchased_paid_media_handler.PurchasedPaidMediaHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.purchased_paid_media_handler.PurchasedPaidMediaHandler(func)  # noqa: E501
                )

            return func

        return wrapper

    def on_shipping_query(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.shipping_query_handler.ShippingQueryHandler(func, filters)  # noqa: E501
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.shipping_query_handler.ShippingQueryHandler(func)  # noqa: E501
                )

            return func

        return wrapper

    def on_story(self, filters: Optional[Filter] = None) -> Callable[[T], T]:  # noqa: E501
        def wrapper(func: T) -> T:
            if filters:
                self.handlers.append(
                    pyrogram.handlers.story_handler.StoryHandler(func, filters)
                )

            else:
                self.handlers.append(
                    pyrogram.handlers.story_handler.StoryHandler(func)
                )

            return func

        return wrapper
