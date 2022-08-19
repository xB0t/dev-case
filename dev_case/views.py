from django.db.models import Q
from django.shortcuts import render

from blog.models import BlogPost
from config.models import SocialAccountsConfig
from pages.models import AboutSiteConfig, IndexSiteConfig, Page
from portfolio.models import Project

from .settings import ROBOTS_DISALLOW
from .sitemaps import get_sitemap_absolute_url

# TODO: refactor and tweak queries


def home(request):
    index_config = IndexSiteConfig.get_solo()
    social_accounts = SocialAccountsConfig.get_solo()
    posts = BlogPost.objects.filter(status=1)[:3]
    projects = Project.objects.filter(status=1)
    pages = Page.objects.all()
    context = {
        "index_config": index_config,
        "social_accounts": social_accounts,
        "posts": posts,
        "projects": projects,
        "pages": pages,
    }
    return render(request, "index.html", context=context)


def about(request):
    about_config = AboutSiteConfig.get_solo()
    social_accounts = SocialAccountsConfig.get_solo()
    pages = Page.objects.all()
    context = {
        "about_config": about_config,
        "social_accounts": social_accounts,
        "pages": pages,
    }
    return render(request, "about.html", context=context)


def search(request):
    posts = BlogPost.objects.filter(status=1)
    pages = Page.objects.all()

    if request.method == "GET":
        query = request.GET.get("q")
        if query:
            posts = BlogPost.objects.filter(
                Q(title__icontains=query) | Q(category__name__icontains=query)
            )

    context = {
        "posts": posts,
        "pages": pages,
    }

    return render(request, "search.html", context=context)


def robots_txt(request):
    context = {
        "sitemap": get_sitemap_absolute_url(request),
        "disallow": ROBOTS_DISALLOW,
    }
    return render(request, "robots.txt", context=context, content_type="text/plain")
