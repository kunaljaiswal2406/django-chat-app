"""Data Access Layer for the challenge app."""

from django.contrib.auth.models import User
from chat import models


def create_message(sender_id: int, receiver_id: int, text: str) -> bool:
    """Create a message.

    Args:
        sender_id (int): Id of the sender.
        receiver_id (int): Id of the receiver.
        text (str): Text of the message.

    Returns:
        bool: True if message is created successfully, False otherwise.

    """
    message = models.Message.objects.create(
        sender_id=sender_id,
        receiver_id=receiver_id,
        text=text,
    )
    if message:
        return True
    return False


def get_unread_message_for_user(
    user_id: int, sender_id: int = None
) -> list[models.Message]:
    """Returns all unread messages for the user.

    Args:
        user_id (int): Id of the user.
        sender_id (int, optional): Id of the sender. Defaults to None.

    Returns:
        list[models.Message]: List of unread messages for the user.

    """
    messages = models.Message.objects.filter(receiver=user_id, is_read=False)
    if sender_id is not None:
        messages = messages.filter(sender_id=sender_id)
    return list(messages)


def get_all_message_for_user(
    user_id: int, sender_id: int = None
) -> list[models.Message]:
    """Returns all messages for the user.

    Args:
        user_id (int): Id of the user.
        sender_id (int, optional): Id of the sender. Defaults to None.

    Returns:
        list[models.Message]: List of all messages for the user.

    """
    messages = models.Message.objects.filter(receiver=user_id)
    if sender_id is not None:
        messages = messages.filter(sender_id=sender_id)
    return list(messages)
