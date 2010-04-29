from django.contrib.admin.options import IncorrectLookupParameters
from django.contrib.admin.views.main import ChangeList
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.core.serializers import serialize
from django.template import loader, RequestContext
from django.template.defaultfilters import slugify
from django.db.models.loading import get_model
from django.utils.encoding import smart_str
import csv

ALLOWED_EXPORT_TYPES = {
    'csv': {
        'mimetype': 'text/csv',
        'filename': '%s.csv',
        'template': 'admin/export/csv',
    },
    'json': {
        'mimetype': 'text/json',
        'filename': '%s.json',
        'serializer': 'json',
    },
    'xml': {
        'mimetype': 'text/xml',
        'filename': '%s.xml',
        'serializer': 'xml',
    },
    'yaml': {
        'mimetype': 'text/yaml',
        'filename': '%s.yaml',
        'serializer': 'yaml',
    },
    'py': {
        'mimetype': 'application/python',
        'filename': '%s.py',
        'serializer': 'python',
    }
}

def export(request, admin_site, model_name, app_label, format='csv'):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    if not format in ALLOWED_EXPORT_TYPES:
        raise Http404('%s is not a supported format.' % format)

    model = get_model(app_label, model_name)
    model_admin = None

    for entry in admin_site._registry:
        if entry._meta.object_name == model._meta.object_name:
            model_admin = admin_site._registry[entry]

    if model_admin == None:
        raise Http404('ModelAdmin for model %s.%s not found' % (app_label, model_name))

    cl = ChangeList(request, model, list(model_admin.list_display), model_admin.list_display_links,
                    model_admin.list_filter, model_admin.date_hierarchy, model_admin.search_fields,
                    model_admin.list_select_related, model_admin.list_per_page, model_admin.list_editable,
                    model_admin)
    cl.formset = None

    c = RequestContext(request)
    if 'template' in ALLOWED_EXPORT_TYPES[format]:
        rows = []
        headers = []

        for field in model._meta.fields:
            headers.append(field.name)

        rows.append(headers)

        for record in cl.query_set:
            column = []

            for field in headers:
                val = getattr(record, field)

                if callable(val):
                    val = val()

                val = smart_str(val)
                column.append(val)

            rows.append(column)

        t = loader.get_template(ALLOWED_EXPORT_TYPES[format]['template'])
        c['rows'] = rows
        responseContents = t.render(c)
    elif 'serializer' in ALLOWED_EXPORT_TYPES[format]:
        responseContents = serialize(ALLOWED_EXPORT_TYPES[format]['serializer'], cl.query_set.all())
    else:
        raise Http404('Export type for %s must have value for template or serializer' % format)

    response = HttpResponse(responseContents, mimetype=ALLOWED_EXPORT_TYPES[format]['mimetype'])
    response['Content-Disposition'] = 'attachment; filename=%s' % (ALLOWED_EXPORT_TYPES[format]['filename'] % slugify(model_name))

    return response