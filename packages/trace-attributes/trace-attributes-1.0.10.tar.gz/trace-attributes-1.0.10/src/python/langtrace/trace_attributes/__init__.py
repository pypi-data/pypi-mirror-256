# __init__.py
from enum import Enum

from .models.langtrace_span_attributes import LangTraceSpanAttributes
from .models.openai_span_attributes import OpenAISpanAttributes


class Event(Enum):
    STREAM_START = "stream.start"
    STREAM_OUTPUT = "stream.output"
    STREAM_END = "stream.end"


# Export only what you want to be accessible directly through `import my_package`
__all__ = ['OpenAISpanAttributes', 'LangTraceSpanAttributes', 'Event']
