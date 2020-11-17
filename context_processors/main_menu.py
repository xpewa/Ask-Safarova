from django.db.models import Count

from main.models import Profile, Tag, User

def menu(request):
    try:
        profile = Profile.objects.get(id=request.user.id)
    except Profile.DoesNotExist:
        profile = None

    popular_tags = Tag.objects.annotate(num=Count('question')).order_by('-num')[0:12]
    best_members = User.objects.annotate(num=Count('question') + Count('answer')).order_by('-num')[0:6]

    return {
        'user': request.user,
        'profile': profile,
        'popular_tags': popular_tags,
        'best_members': best_members,
    }