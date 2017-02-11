from .models import Profile

def save_avatar(backend, user, response, *args, **kwargs):
    try:
        profile = Profile.objects.get(user_id=user.id)
    except Profile.DoesNotExist:
        profile = Profile(user_id=user.id)

    if backend.name == 'facebook':
        if not profile.name:
            profile.name = '%s' % response.get('name')
        if not profile.email:
            profile.email = '%s' % response.get('email')
        profile.avatar = 'http://graph.facebook.com/%s/picture?type=large' % response['id']

    if backend.name == 'twitter':
        if not profile.name:
            profile.name = '%s' % response.get('name')
        if not profile.email:
            profile.email = '%s' % response.get('email')
        # profile.name = '%s' % response.get('name')
        # profile.email = '%s' % response.get('email')
        profile.avatar = response['profile_image_url_https']

    profile.save()