# __init__.py
from enum import Enum

from .models.database_span_attributes import DatabaseSpanAttributes
from .models.langtrace_span_attributes import LangTraceSpanAttributes
from .models.openai_span_attributes import OpenAISpanAttributes


class Event(Enum):
    STREAM_START = "stream.start"
    STREAM_OUTPUT = "stream.output"
    STREAM_END = "stream.end"
class LlamaIndexMethods(Enum):
    TASK_LLAMAINDEX_BASEEXTRACTOR_EXTRACT = "task.llamaindex.BaseExtractor.extract"
    TASK_LLAMAINDEX_SIMPLEPROMPT_CALL = "task.llamaindex.SimplePrompt.call"
    TASK_LLAMAINDEX_CHATENGINE_EXTRACT = "task.llamaindex.ChatEngine.chat"
    TASK_LLAMAINDEX_RETRIEVER_RETRIEVE = "task.llamaindex.Retriever.retrieve"
    TASK_LLAMAINDEX_QUERYENGINE_QUERY = "task.llamaindex.QueryEngine.query"
    TASK_LLAMAINDEX_BASEREADER_LOADDATA = "task.llamaindex.BaseReader.loadData"

# Export only what you want to be accessible directly through `import my_package`
__all__ = ['OpenAISpanAttributes', 'LangTraceSpanAttributes', 'DatabaseSpanAttributes', 'Event', 'LlamaIndexMethods']
