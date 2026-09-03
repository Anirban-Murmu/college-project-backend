from django.conf import settings


def get_profile_image(instance, request):
    # User uploaded a photo
    if instance.image:
        return request.build_absolute_uri(
            instance.image.url
        )

    # No uploaded photo → choose default
    if instance.gender == "male":
        default_image = "default_profiles/male.jpg"

    elif instance.gender == "female":
        default_image = "default_profiles/female.png"

    else:
        default_image = "default_profiles/other.png"

    return request.build_absolute_uri(
        settings.STATIC_URL + default_image
    )