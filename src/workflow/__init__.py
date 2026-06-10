# Import the compiled linear sequence graph from your module file
from .sequence import sequential_workflow

# Define the public interface for the workflow package
__all__ = [
    "sequential_workflow"
]