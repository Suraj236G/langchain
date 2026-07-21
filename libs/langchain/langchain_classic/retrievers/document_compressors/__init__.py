import importlib
from typing import Any

from langchain_classic.retrievers.document_compressors.base import (
    DocumentCompressorPipeline,
)
from langchain_classic.retrievers.document_compressors.chain_extract import (
    LLMChainExtractor,
)
from langchain_classic.retrievers.document_compressors.chain_filter import (
    LLMChainFilter,
)
from langchain_classic.retrievers.document_compressors.cohere_rerank import CohereRerank
from langchain_classic.retrievers.document_compressors.cross_encoder_rerank import (
    CrossEncoderReranker,
)
from langchain_classic.retrievers.document_compressors.embeddings_filter import (
    EmbeddingsFilter,
)
from langchain_classic.retrievers.document_compressors.listwise_rerank import (
    LLMListwiseRerank,
)

_module_lookup = {
    "FlashrankRerank": "langchain_community.document_compressors.flashrank_rerank",
}


_ALLOWED_MODULE_PATHS = frozenset(_module_lookup.values())


def __getattr__(name: str) -> Any:
    if name in _module_lookup:
        module_path = _module_lookup[name]
        if module_path not in _ALLOWED_MODULE_PATHS:
            msg = f"Blocked import of non-whitelisted module: {module_path}"
            raise ImportError(msg)
        module = importlib.import_module(module_path)
        return getattr(module, name)
    msg = f"module {__name__} has no attribute {name}"
    raise AttributeError(msg)


__all__ = [
    "CohereRerank",
    "CrossEncoderReranker",
    "DocumentCompressorPipeline",
    "EmbeddingsFilter",
    "FlashrankRerank",
    "LLMChainExtractor",
    "LLMChainFilter",
    "LLMListwiseRerank",
]
