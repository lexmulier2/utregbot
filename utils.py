def message_chat(bot, update, message, chat_id=None):
    """
    Send a message to a chat.
    :param bot: Bot object
    :param update: Update object
    :param message: Message  to be send to the chat
    :param chat_id: Chat id if no update object available.
    :return:
    """
    if chat_id:
        chat_id = chat_id
    elif hasattr(update, 'message'):
        chat_id = update.message.chat_id

    if not chat_id:
        raise ValueError('No chat_id specified. Nowhere to send message to.')

    bot.send_message(chat_id=chat_id, text=message)
