from pathlib import Path


def patch_promplate(patch_openai=False):
    import promplate

    class Loader(promplate.template.Loader):
        """making HTTP requests in pyodide runtime"""

        @classmethod
        async def afetch(cls, url: str, **kwargs):
            from pyodide.http import pyfetch

            res = await pyfetch(cls._join_url(url))
            obj = cls(await res.text())
            obj.name = Path(url).stem

            return obj

        @classmethod
        def fetch(cls, url: str, **kwargs):
            from pyodide.http import open_url

            res = open_url(cls._join_url(url))
            obj = cls(res.read())
            obj.name = Path(url).stem

            return obj

    class Node(Loader, promplate.Node):
        """patched for making HTTP requests in pyodide runtime"""

    class Template(Loader, promplate.Template):
        """patched for making HTTP requests in pyodide runtime"""

    promplate.template.Loader = Loader
    promplate.template.Template = promplate.Template = Template
    promplate.node.Node = promplate.Node = Node

    if patch_openai:
        from promplate.prompt.chat import ensure as _ensure

        from .utils.proxy import to_js

        def ensure(text_or_list: list[promplate.Message] | str):
            """This function is patched to return a JS array. So it should not be called from Python."""
            return to_js(_ensure(text_or_list))

        promplate.prompt.chat.ensure = ensure

        from functools import partial, wraps

        import promplate.llm.openai as llm_openai

        llm_openai.TextComplete = llm_openai.AsyncTextComplete = wraps(
            llm_openai.AsyncTextComplete
        )(partial(llm_openai.AsyncTextComplete, http_client=None))

        llm_openai.TextGenerate = llm_openai.AsyncTextGenerate = wraps(
            llm_openai.AsyncTextGenerate
        )(partial(llm_openai.AsyncTextGenerate, http_client=None))

        llm_openai.ChatComplete = llm_openai.AsyncChatComplete = wraps(
            llm_openai.AsyncChatComplete
        )(partial(llm_openai.AsyncChatComplete, http_client=None))

        llm_openai.ChatGenerate = llm_openai.AsyncChatGenerate = wraps(
            llm_openai.AsyncChatGenerate
        )(partial(llm_openai.AsyncChatGenerate, http_client=None))

        del llm_openai.SyncTextOpenAI
        del llm_openai.SyncChatOpenAI
