from contextvars import ContextVar

conversation_id = ContextVar('conversation_id', default=None)
user_id = ContextVar('user_id', default=None)
last_assistant_message_id = ContextVar('last_assistant_message_id', default=None)