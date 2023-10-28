__all__ = ["ban", "delete", "gpt"]

from aiogram import Router, F

from bozenka.telegram.utils.callbacks_factory import *
from bozenka.telegram.queries.ban import inline_ban, inline_unban
from bozenka.telegram.queries.delete import inline_delete
from bozenka.telegram.queries.revoke import inline_revoke
from bozenka.telegram.queries.gpt import *


def register_queries(router: Router) -> None:
    """
    Register all callback queries.
    :param router:
    :return:
    """
    logging.log(msg="Registering callback queries", level=logging.INFO)
    router.callback_query.register(inline_ban, BanData.filter())
    router.callback_query.register(inline_unban, UnbanData.filter())
    router.callback_query.register(inline_delete, DeleteCallbackData.filter())
    router.callback_query.register(inline_revoke, RevokeCallbackData.filter())
    # r.callback_query.register(inline_gpt_menu, GptCategoryCallbackData.filter())
    router.callback_query.register(inline_g4f_ready, Gpt4freeResult.filter())
    router.callback_query.register(inline_gpt4free_models, Gpt4FreeProvider.filter())
    router.callback_query.register(inline_gpt4free, GptCategory.filter(F.category == "Gpt4Free"))
    router.callback_query.register(generate_next_page, Gpt4FreePage.filter(), flags={"rate_limit": {"rate": 5}})
    router.callback_query.register(inline_return_pages, F.data == "gotpages")
    router.callback_query.register(inline_g4a_ready, GptCategory.filter(F.category == "Gpt4All"))
