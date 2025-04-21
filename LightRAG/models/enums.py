from enum import Enum, auto

class RetrievalMode(Enum):
    """Specifies the retrieval strategy."""
    VECTOR = auto()
    GRAPH = auto()
    HYBRID = auto() # Combines vector and graph
    NAIVE = auto() # Simple text matching (less common in complex RAG)

class ProcessingStatus(Enum):
    """Represents the status of document processing."""
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()

class DataSource(Enum):
    """Type of the input data source."""
    FILE = auto()
    TEXT = auto()
    URL = auto()
    DATABASE = auto()
    API = auto() 