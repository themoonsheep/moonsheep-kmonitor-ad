from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.urls import path
from .models import *

# Register your models here.

# TODO move this to project_template
class MyAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('project_template/import_declarations', self.import_declarations_from_parldata, name='import_declarations'),
        ]
        return my_urls + urls

    def import_declarations_from_parldata(self, request):
        from .importers import parldata
        # TODO catch requests.exceptions.ConnectionError

        if request.method == 'POST' and request.REQUEST['chamber'] and int(request.REQUEST['year']):
            year = int(request.REQUEST['year'])
            chamber_id = request.REQUEST['chamber']

            report = parldata.import_declarations(document_set, chamber_id, year)

            return render_to_response('admin/kmonitor_import_asset_declarations_report.html',
                                      {
                                          'document_set': document_set,
                                          'current_app': self.admin_site.name,
                                          'report': report
                                      },
                                      RequestContext(request))

        else:
            params = dict(
                # Include common variables for rendering the admin template.
                self.each_context(request),
                # Anything else you want in the context...
                chambers=parldata.get_chambers()
            )
            return TemplateResponse(request, "admin/project_template/import_declarations.html", params)


site = MyAdminSite()
site.register(User)
site.register(Group)


@admin.register(Politician)
class PoliticianAdmin(admin.ModelAdmin):
    pass


site.register(Person)
site.register(Party)
site.register(Declaration)


class PropertyAcquisitionTitleInline(admin.TabularInline):
    model = PropertyAcquisitionTitle


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [
        PropertyAcquisitionTitleInline,
    ]


site.register(Vehicle)
site.register(ArtWork)
site.register(Security)
site.register(Savings)
site.register(Cash)
site.register(Obligation)
site.register(Debt)
site.register(Income)
site.register(EconomicInterest)
site.register(Benefit)
site.register(Present)
site.register(Subsidy)


