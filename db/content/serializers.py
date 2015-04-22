from wq.db.rest.serializers import ModelSerializer
from rest_framework.serializers import Field
from rest_framework.serializers import SerializerMethodField
import markdown
import re
from django.conf import settings
from .models import ScreenShot

SUFFIX = {
    1: "st",
    2: "nd",
    3: "rd",
}


class PageSerializer(ModelSerializer):
    version_date_label = SerializerMethodField("get_version_date")

    def get_html(self, obj):
        html = markdown.markdown(obj.markdown, settings.MARKDOWN)
        html = re.sub(
            r'(<\/h1>\s*<p><a) (href="https:\/\/github.com\/[^"]+\/blob)',
            r'\1 class="github-file" \2',
            html,
            count=1
        )
        html = re.sub(
            r'a (href="https:\/\/github.com\/[^"]+\/blob)',
            r'a class="github-src" \1',
            html
        )
        html = re.sub(
            r'(href="http[s]?:\/\/(?!wq\.io))',
            r'rel="external" \1',
            html
        )
        return html

    def get_version_date(self, obj):
        if not getattr(obj, 'version_date', None):
            return None
        date = obj.version_date.strftime('%B %d, %Y')
        date = date.replace(" 0", " ")
        sfx = SUFFIX.get(obj.version_date.day % 10, 'th')
        date = date.replace(",", sfx + ",")
        return date

    def get_default_fields(self, *args, **kwargs):
        default_fields = super(PageSerializer, self).get_default_fields(
            *args, **kwargs
        )
        if self.context['view'].depth > 0:
            default_fields['html'] = SerializerMethodField('get_html')
        return default_fields


class DocSerializer(PageSerializer):
    next_id = SerializerMethodField('get_next_id')
    next_label = SerializerMethodField('get_next_label')
    prev_id = SerializerMethodField('get_prev_id')
    prev_label = SerializerMethodField('get_prev_label')

    def get_next_id(self, instance):
        if instance.next:
            return instance.next.primary_identifier.slug

    def get_next_label(self, instance):
        if instance.next:
            return unicode(instance.next)

    def get_prev_id(self, instance):
        if instance.prev:
            return instance.prev.primary_identifier.slug

    def get_prev_label(self, instance):
        if instance.prev:
            return unicode(instance.prev)

class ScreenShotSerializer(ModelSerializer):
    class Meta:
        model = ScreenShot


class ExampleSerializer(PageSerializer):
    modules = Field()
    full_api = Field()
    screenshots = ScreenShotSerializer(many=True, source="screenshot_set")


class PaperSerializer(ModelSerializer):
    acm_dl = Field()
    doi = Field()
    citation_date = Field()
    author_list = Field()
