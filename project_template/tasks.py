import datetime

from moonsheep.tasks import AbstractTask
from moonsheep.verifiers import *

from .forms import *
from .models import *


def create_mocked_task(self, base):
    if Declaration.objects.exists():
        d = Declaration.objects.order_by('?').first()
        base['info'].update({
            'url': d.url,
            'politician_id': d.politician.id
        })
    else:
        base['info'].update({
            'url': 'http://www.parlament.hu/internet/cplsql/ogy_vagyonpub.vagyon_kiir_egys?P_FNEV=/2016/l001_j0161231k.pdf&p_cont=application/pdf',
        })

    return base
#
# class BigTask(AbstractTask):
#     task_form_template = 'tasks/base.html'
#
#     # def save_verified_data(self, verified_data):
#     #     party, created = PoliticalParty.objects.get_or_create(
#     #         name=verified_data['party_name'],
#     #         legal_id=verified_data['party_legal_id']
#     #     )
#     #     Report.objects.get_or_create(
#     #         report_date=datetime.datetime.strptime(verified_data['report_date'], "%Y-%m-%d"),
#     #         party=party,
#     #         document_page_start=verified_data['page']
#     #     )
#
#     def after_save(self, verified_data):
#         pass
#
#     create_mocked_task = create_mocked_task

class S1PersonalData(AbstractTask):
    """
    Személyes információk
    """
    task_form_template = 'tasks/personal_data.html'

    create_mocked_task = create_mocked_task

class S2Properties(AbstractTask):
    """
    Ingatlanok
    """
    task_form_template = 'tasks/properties.html'

    create_mocked_task = create_mocked_task


class S3Movables(AbstractTask):
    """
    Nagy értékű ingóságok
    """
    task_form_template = 'tasks/movables.html'

    create_mocked_task = create_mocked_task

    def save_verified_data(self, vd: dict):
        d = Declaration.objects.get(url=self.url)

        # TODO assuming this declarations has not been verified
        # otherwise we need to get existing properties, order them by how they were saved (additional field)
        # and update their properties!

        for i in range(len(vd['location'])):
            fields = {
                'declaration': d,
            }

            def get(fld_name, param_name=None, convert=lambda x: x):
                if param_name is None:
                    param_name = fld_name
                if vd[param_name][i].strip():
                    fields[fld_name] = convert(vd[param_name][i].strip())

            def get_checkbox(fld_name, param_name=None):
                if param_name is None:
                    param_name = fld_name
                # checkboxes won't be in POST if they are not checked
                # TODO how does it affect processing forms?
                if param_name in vd and vd[param_name][i]:
                    fields[fld_name] = True
                else:
                    fields[fld_name] = False # not needed if we do NullBooleanField

            get('location')
            get('area')
            get('area_unit')
            get('area_unit', 'area_unit_other')

            get_checkbox('cultivation_belterulet', 'cultivation1')
            get_checkbox('cultivation_kulterulet', 'cultivation2')
            get_checkbox('cultivation_lakas', 'cultivation3')
            get('cultivation_other')

            get_checkbox('building_nature_garazs', 'building_nature1')
            get_checkbox('building_nature_lakohaz', 'building_nature2')
            get_checkbox('building_nature_udulo', 'building_nature3')
            get('building_nature_other')

            get('building_area')
            get('building_area_unit')
            get('building_area_unit', 'building_area_unit_other')

            get_checkbox('legal_designation_csaladi_haz', 'legal_designation1')
            get_checkbox('legal_designation_tarsashaz', 'legal_designation2')
            get_checkbox('legal_designation_garazs', 'legal_designation3')
            get('legal_designation_other')

            get_checkbox('legal_status_tulajdonos', 'legal_status1')
            get_checkbox('legal_status_haszonelvezo', 'legal_status2')
            get_checkbox('legal_status_berlo', 'legal_status3')
            get('legal_status_other')

            get('ownership_ratio_numerator', 'ownership_ratio1', convert=int)
            get('ownership_ratio_denominator', 'ownership_ratio2', convert=int)
            get('ownership_ratio_percent', 'ownership_ratio_percent', convert=float)

            p = Property(**fields)
            p.save()

            # Property titles
            for j in range(len(vd['acquisition1'][i])):
                fields = {
                    'property': p,
                }

                def get(fld_name, param_name=None, convert=lambda x: x):
                    if param_name is None:
                        param_name = fld_name
                    if vd[param_name][i][j].strip():
                        fields[fld_name] = convert(vd[param_name][i][j].strip())

                get('title', 'acquisition1')
                get('title', 'acquisition-other')

                get('year', 'acquisition-year')
                get('month', 'acquisition-month') # TODO fix default option: choose in forms
                get('day', 'acquisition-day')

                PropertyAcquisitionTitle(**fields).save()


    # TODO feedback 'something_wrong': ['']}


class S4FinancialAndOther(AbstractTask):
    """
    tartozások ?
    megtakarításról, befektetésről, pénzkövetelésről, tartozásokról
    savings, investments, money claims, debts

    egyéb közlendők (other)
    """
    task_form_template = 'tasks/financial.html'

    create_mocked_task = create_mocked_task


class S5Income(AbstractTask):
    """
    Jövedelemnyilatkozat
    """
    task_form_template = 'tasks/income.html'

    create_mocked_task = create_mocked_task


class S6EconomicInterest(AbstractTask):
    """
    érdekeltségi
    """
    task_form_template = 'tasks/economic_interest.html'

    create_mocked_task = create_mocked_task


class S7Benefits(AbstractTask):
    """
    juttatásról, ajándékról, támogatásról
    benefits, gifts, or subsidies
    """
    task_form_template = 'tasks/benefits.html'

    create_mocked_task = create_mocked_task
