"""Private functions for the chat app goes here."""

from chat import dal


send_message = dal.create_message


def get_unread_message_for_user(user_id: int, sender_id: int = None) -> list[dict]:
    """Returns all unread messages for the user.

    Args:
        user_id (int): Id of the user.
        sender_id (int, optional): Id of the sender. Defaults to None.

    Returns:
        list[dict]: List of unread messages for the user.

    """
    unread_messages = dal.get_unread_message_for_user(user_id, sender_id)
    response = []
    for messages in unread_messages:
        response.append(
            {
                "text": messages.text,
                "sender_id": messages.sender.id,
            }
        )
        messages.mark_message_as_read()
    return response


def get_all_messages_for_user(user_id: int, sender_id: int = None) -> list[dict]:
    """Returns all messages for the user.

    Args:
        user_id (int): Id of the user.

    Returns:
        list[dict]: List of all messages for the user.

    """
    all_messages = dal.get_all_message_for_user(user_id, sender_id)
    response = []
    for messages in all_messages:
        response.append(
            {
                "text": messages.text,
                "sender_id": messages.sender.id,
            }
        )
    return response
