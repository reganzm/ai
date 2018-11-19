from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic import TemplateView
from settings import IMG_PATH, BASE_DIR

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #     url(r'^more.html', TemplateView.as_view(template_name="sxz/more.html")),
    url(r'^more.html', 'sxz.views.more'),

    url(r'^sxz/(?P<path>.*)', 'django.views.static.serve', {'document_root': BASE_DIR + '/templates/sxz'}),
    url(r'^salary_predict_pro', 'sxz.views.salary_predict_pro'),

    url(r'^save_email', 'sxz.views.save_email'),
    url(r'^share_statis', 'sxz.views.share_statis'),
    url(r'^share_picture', 'sxz.views.produce_html_image'),
    url(r'^predict_feedback', 'sxz.views.predict_feedback'),
    url(r'^share_plantform', 'sxz.views.share_plantform'),
    url(r'^$', TemplateView.as_view(template_name="sxz/sxz.html")),
    url(r'^images/(?P<path>.*)', 'django.views.static.serve', {'document_root': IMG_PATH}),
    url(r'^(?P<path>.*)', 'django.views.static.serve', {'document_root': BASE_DIR + '/templates/sxz'}),
)
