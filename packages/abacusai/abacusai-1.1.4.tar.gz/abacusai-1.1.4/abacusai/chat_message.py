from .return_class import AbstractApiClass


class ChatMessage(AbstractApiClass):
    """
        A single chat message with Abacus Chat.

        Args:
            client (ApiClient): An authenticated API Client instance
            role (str): The role of the message sender
            text (list): A list of text segments for the message
            timestamp (str): The timestamp at which the message was sent
            isUseful (bool): Whether this message was marked as useful or not
            feedback (str): The feedback provided for the message
            docIds (list): A list of IDs of the uploaded document if the message has
            hotkeyTitle (str): The title of the hotkey prompt if the message has one
    """

    def __init__(self, client, role=None, text=None, timestamp=None, isUseful=None, feedback=None, docIds=None, hotkeyTitle=None):
        super().__init__(client, None)
        self.role = role
        self.text = text
        self.timestamp = timestamp
        self.is_useful = isUseful
        self.feedback = feedback
        self.doc_ids = docIds
        self.hotkey_title = hotkeyTitle
        self.deprecated_keys = {}

    def __repr__(self):
        repr_dict = {f'role': repr(self.role), f'text': repr(self.text), f'timestamp': repr(self.timestamp), f'is_useful': repr(
            self.is_useful), f'feedback': repr(self.feedback), f'doc_ids': repr(self.doc_ids), f'hotkey_title': repr(self.hotkey_title)}
        class_name = "ChatMessage"
        repr_str = ',\n  '.join([f'{key}={value}' for key, value in repr_dict.items(
        ) if getattr(self, key, None) is not None and key not in self.deprecated_keys])
        return f"{class_name}({repr_str})"

    def to_dict(self):
        """
        Get a dict representation of the parameters in this class

        Returns:
            dict: The dict value representation of the class parameters
        """
        resp = {'role': self.role, 'text': self.text, 'timestamp': self.timestamp, 'is_useful': self.is_useful,
                'feedback': self.feedback, 'doc_ids': self.doc_ids, 'hotkey_title': self.hotkey_title}
        return {key: value for key, value in resp.items() if value is not None and key not in self.deprecated_keys}
