from wagtail import hooks


@hooks.register("get_avatar_url")
def get_profile_picture(user, size):
    return user.profile_picture
