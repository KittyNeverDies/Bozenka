__all__ = ["ban", "delete", "gpt"]

from aiogram import Router, F

from bozenka.instances.telegram.utils.callbacks_factory import *
from bozenka.instances.telegram.queries.ban import *
from bozenka.instances.telegram.queries.pins import *
from bozenka.instances.telegram.queries.threads import *
from bozenka.instances.telegram.queries.delete import *
from bozenka.instances.telegram.queries.revoke import *
from bozenka.instances.telegram.queries.gpt import *
from bozenka.instances.telegram.queries.setup import *


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

    # Threads (Close/Open)
    router.callback_query.register(inline_close_thread, CloseThread.filter())
    router.callback_query.register(inline_open_thread, OpenThread.filter())

    # Pins (Pin/Unpin)
    router.callback_query.register(inline_pin_msg, PinMsg.filter())
    router.callback_query.register(inline_unpin_msg, UnpinMsg.filter())

    # GPT Related queries

    # Back to gpt categories
    router.callback_query.register(inline_start_gpt, GptBackMenu.filter(F.back_to == "category"))

    # Gpt4Free menus (Providers/Models)
    router.callback_query.register(inline_g4f_providers, GptCategory.filter(F.category == "Gpt4Free"))
    router.callback_query.register(inline_g4f_models, Gpt4FreeProvider.filter())

    # Get back to menu state
    router.callback_query.register(inline_g4f_providers_back, GptBackMenu.filter(F.back_to == "providers"))

    # Generates next pages (Providers/Models)
    router.callback_query.register(inline_next_g4f_models, Gpt4FreeModelPage.filter(), flags={"rate_limit": {"rate": 5}})
    router.callback_query.register(inline_next_g4f_providers, Gpt4FreeProviderPage.filter(),
                                   flags={"rate_limit": {"rate": 5}})

    # Help information (for page button under menu)
    router.callback_query.register(inline_return_pages, F.data == "gotpages")
    router.callback_query.register(inline_g4f_ready, Gpt4freeResult.filter())

    # Gpt4All menus
    # Gpt4All model menu
    router.callback_query.register(inline_g4a, GptCategory.filter(F.category == "Gpt4All"))

    # Gpt4All back
    router.callback_query.register(inline_g4a_back, GptBackMenu.filter(F.back_to == "g4amodels"))

    # Gpt4All selected model menu
    router.callback_query.register(inline_g4a_model, Gpt4AllModel.filter())
    router.callback_query.register(inline_g4a_select_model, Gpt4AllSelect.filter())

    # Stop dialog button under gpt message answer
    router.callback_query.register(inline_stop_dialog, GptStop.filter())

    # /setup command related queries
    # List of features based on category
    router.callback_query.register(inline_setup_features, SetupCategory.filter())

    # Menu of feature to enable or disable
    router.callback_query.register(inline_feature, SetupFeature.filter())
