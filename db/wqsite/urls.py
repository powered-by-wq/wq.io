from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from wq.db.rest import app
app.autodiscover()

from content.views import DocRedirectView
from content.models import Page, Doc
page_detail = app.router.get_viewset_for_model(Page).as_view(
    {'get': 'retrieve'}
)
doc_detail = app.router.get_viewset_for_model(Doc).as_view(
    {'get': 'retrieve'}
)

urlpatterns = patterns('',
    # Special handing for wq.* and docs/*.js pages since their slugs are
    # technically invalid
    url(r'^(?P<primary_identifiers__slug>wq\.\w+)', page_detail),
    url(r'^docs/(?P<primary_identifiers__slug>\w+\.py)/?$', doc_detail),
    url(r'^docs/(?P<doc>\w+\.js)/?$', DocRedirectView.as_view()),

    # Default admin and wq.db routes
    url(r'^admin/', include(admin.site.urls)),
    url(r'^',       include(app.router.urls)),
)
