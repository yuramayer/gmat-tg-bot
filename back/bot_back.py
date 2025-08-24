"""Methods working with bot's text"""


def should_reg_msg():
    """Bot msg for the new users who should be registrated"""
    return (
        "Сейчас вас зарегистрируем 👋"
    )


def registration_msg():
    """Bot registration msg for the new users"""
    return (
        "Регистрация прошла успешно 🎉"
    )


def already_registrated_msg():
    """Bot msg for users who has already registrated"""
    return (
        "Вы уже зарегистрированы 😌"
    )
