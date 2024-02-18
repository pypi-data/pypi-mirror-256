from typing import Optional, List, Dict, Union, Any, Literal
from pydantic import BaseModel, Field

class LLMChatBaseModel(BaseModel):
    # Override dict method to exclude None values
    def dict(self, **kwargs) -> Dict[str, Any]:
        kwargs.setdefault('exclude_none', True)
        return super().dict(**kwargs)


# Base LLM Chat Message Schema
class BaseLLMChatMessage(LLMChatBaseModel):
    role: str
    content: str
    userName: Optional[str] = None

    # Override dict method to exclude None values
    def dict(self, **kwargs) -> Dict[str, Any]:
        kwargs.setdefault('exclude_none', True)
        return super().dict(**kwargs)

# Function Call Schema
class FunctionCall(LLMChatBaseModel):
    name: str
    arguments: Any

# Base LLM Chat Message With Function Call Schema
class BaseLLMChatMessageWithFunctionCall(BaseLLMChatMessage):
    functionCall: Optional[FunctionCall] = None
    
    # Override dict method to exclude None values
    def dict(self, **kwargs) -> Dict[str, Any]:
        kwargs.setdefault('exclude_none', True)
        return super().dict(**kwargs)

# RegML Issue Schema (Placeholder Implementation)
class RegMLIssueSchema(LLMChatBaseModel):
    # Assuming a simple schema for demonstration; adjust as needed.
    issueType: str
    description: str

# Common Output Schema
class OutputSchema(LLMChatBaseModel):
    choices: List[BaseLLMChatMessageWithFunctionCall]
    issues: Optional[List[RegMLIssueSchema]] = None

# Version 0.0.0 Input Schema
class InputSchemaV000(LLMChatBaseModel):
    messages: List[BaseLLMChatMessage]

# Version 0.0.1 Input Schema
class InputSchemaV001(InputSchemaV000):
    numChoices: Optional[int] = Field(default=1, description="The number of choices to generate. (default: 1)")

# Function Description Schema
class FunctionDescription(LLMChatBaseModel):
    name: str
    description: str
    parameters: Any

# Version 0.1.0 Input Schema
class LLMChat_V0_1_0_InputSchema(LLMChatBaseModel):
    messages: List[BaseLLMChatMessageWithFunctionCall]
    numChoices: Optional[int] = Field(default=1, description="The number of choices to generate. (default: 1)")
    functions: Optional[List[FunctionDescription]] = None
    functionCall: Union[None, Literal['none'], Literal['auto'], Dict[str, str]] = None

# Task Schema Wrapper
class TaskSchema(LLMChatBaseModel):
    InputSchema: LLMChat_V0_1_0_InputSchema
    OutputSchema: OutputSchema

# Versioned Task Definitions
class LLMChat_V0_1_0_Task(LLMChatBaseModel):
    taskName: str
    taskVersion: str
    taskSchema: TaskSchema