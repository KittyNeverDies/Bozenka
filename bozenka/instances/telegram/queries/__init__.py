__all__ = ["ban", "delete", "gpt"]

from aiogram import Router, F

from bozenka.instances.telegram.utils.callbacks_factory import *
from bozenka.instances.telegram.queries.ban import inline_ban, inline_unban
from bozenka.instances.telegram.queries.delete import inline_delete
from bozenka.instances.telegram.queries.revoke import inline_revoke
from bozenka.instances.telegram.queries.gpt import *


def register_queries(router: Router) -> None:
    """
    Register all callback queries.
    :param router:
    :return:
    """
    logging.log(msg="Registering callback queries", level=logging.INFO)
    # Moderation
    # Ban / Unban buttons reactions
    router.callback_query.register(inline_ban, BanData.filter())
    router.callback_query.register(inline_unban, UnbanData.filter())

    # Revoke telegram invite link button
    router.callback_query.register(inline_revoke, RevokeCallbackData.filter())
    # Delete button message reaction
    router.callback_query.register(inline_delete, DeleteCallbackData.filter())

    # GPT Related queries
    # Back to gpt categories
    router.callback_query.register(inline_start_gpt, GptBackMenu.filter(F.back_to == "category"))
    # Gpt4Free menus (Providers/Models)
    router.callback_query.register(inline_g4f_providers, GptCategory.filter(F.category == "Gpt4Free"))
    router.callback_query.register(inline_g4f_models, Gpt4FreeProvider.filter())
    # Get back to menu state
    router.callback_query.register(inline_g4f_providers_back, GptBackMenu.filter(F.back_to == "providers"))
    # Generates next pages (Providers/Models)
    router.callback_query.register(next_g4f_models, Gpt4FreeModelPage.filter())
    router.callback_query.register(next_g4f_providers, Gpt4FreeProviderPage.filter(),
                                   flags={"rate_limit": {"rate": 5}})
    # Help information (for page button under menu)
    router.callback_query.register(inline_return_pages, F.data == "gotpages")
    router.callback_query.register(inline_g4f_ready, Gpt4freeResult.filter())
    # Stop dialog button under gpt message answer
    router.callback_query.register(inline_stop_dialog, GptStop.filter())

