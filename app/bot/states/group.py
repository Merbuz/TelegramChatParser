from pyrogram_patch.fsm.states import StatesGroup, StateItem


class ActionStates(StatesGroup):
    add_keyword = StateItem()
    add_chat = StateItem()
    add_session = StateItem()
