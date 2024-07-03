def get_news():
    from news.models import News
    return News.objects.all()