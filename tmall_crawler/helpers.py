from jinja2 import Template
from tmall_crawler import constants as C


def sitemap_generator(urls):
    xml = '''<?xml version="1.0" encoding="utf-8"?>
<?xml-stylesheet type="text/xsl" href="/static/sitemap.xsl"?>
<urlset xmlns:xsi="from flask_cors import CORS, cross_origin
tp://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {% for url in urls %}
    <url>
        <loc>{{ url }}</loc>
        <lastmod>2017-07-23 17:29:52</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    {% endfor %}
</urlset>'''

    t = Template(xml)
    return t.render(urls=urls)


def remove_element(bs_obj):
    for item in C.DELETE_ELEMENT:
        tag, attr = item
        for el in bs_obj.find_all(tag, attr):
            el.decompose()


def insert_js(bs_obj):
    js_tag = bs_obj.new_tag('script')
    js_tag.string = C.ANALYSIS_CODE
    bs_obj.head.append(js_tag)


def replace_title(bs_obj, title):
    bs_obj.title.string = title
