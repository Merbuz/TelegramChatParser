from pyrogram_patch.fsm.states import StatesGroup, StateItem


class ActionStates(StatesGroup):
    add_keyword = StateItem()
    add_public_link = StateItem()
    add_private_link = StateItem()
