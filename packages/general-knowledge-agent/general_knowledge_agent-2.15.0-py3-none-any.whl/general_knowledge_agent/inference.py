import langroid as lr
import pandas as pd

from langroid import ChatAgentConfig
from langroid.language_models.base import (
    LLMMessage,
    Role
)
from langchain.schema.document import Document
from typing import List


class Interaction:
    def __init__(self, role: str, message: str):
        self.role = role
        self.message = message


class Conversation:
    @property
    def roles(self):
        return [llm_message.role for llm_message in self.llm_messages]

    @property
    def messages(self):
        return [llm_message.content for llm_message in self.llm_messages]


    def __init__(self, roles: List[str], messages: List[str], documents: List[Document] = []):
        self.llm_messages = [LLMMessage(role=role, content=message.strip()) for role, message in zip(roles, messages)]
        self.documents = documents
    

    def to_pandas(self):
        return pd.DataFrame(
            {
                'Role': [role.value for role in self.roles], 
                'Message': self.messages
            }
        )
    

    def to_llm_messages(self):
        return self.llm_messages
    

    def to_str(self):
        return '\n'.join([f'{llm_message.role}: {llm_message.content}' for llm_message in self.llm_messages])

    
    def to_openai(self):
        return [{'role': llm_message.role, 'content': llm_message.message} for llm_message in self.llm_messages]


    def set_documents(self, documents: List[Document]):
        self.documents = documents


    def add_interaction(self, role: str, message: str):
        self.llm_messages.append(LLMMessage(role=role, content=message))


class LLM:
    def __init__(self, conversation: Conversation, agent_config: ChatAgentConfig = ChatAgentConfig()):
        self.conversation = conversation
        self.agent_config = agent_config

        self.agent = lr.ChatAgent(
            config=self.agent_config,
            task=self.conversation.to_llm_messages()
        )

    
    def infer(self):
        """
        Infer the next message using model specified in `agent_config`.
        Returns a stripped string response.
        """
        last_message = self.conversation.llm_messages[-1].content
        self.conversation.llm_messages = self.conversation.llm_messages[:-1]

        response = self.agent.llm_response(message=last_message)
        
        if response == None:
            raise Exception('Inquiry response is None.')

        return response.to_LLMMessage(response).content.strip()
