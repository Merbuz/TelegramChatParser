from pyrogram_patch.middlewares.middleware_types import OnUpdateMiddleware
from pyrogram_patch.middlewares import PatchHelper

from app.settings.configparse import Settings


class SecurityMiddleware(OnUpdateMiddleware):
    async def __call__(self, update, client, patch_helper: PatchHelper):
        settings = Settings()

        if update.from_user.id not in settings.white_list:
            await patch_helper.skip_handler()
