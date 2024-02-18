# __init__.py
from .models.langtrace_span_attributes import LangTraceSpanAttributes
from .models.openai_span_attributes import OpenAISpanAttributes

# Export only what you want to be accessible directly through `import my_package`
__all__ = ['OpenAISpanAttributes', 'LangTraceSpanAttributes']
