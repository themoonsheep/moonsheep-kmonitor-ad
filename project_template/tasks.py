import datetime

from moonsheep.models import ModelMapper
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
            m = ModelMapper(Property, vd, getter=lambda param_name: vd[param_name][i])
            m.map()

            # Overwrite _other fields if they are set
            m.map_one('area_unit', 'area_unit_other')\
                .map_one('building_area_unit', 'building_area_unit_other')

            p = m.create()
            p.declaration = d
            p.save()

            # Property titles
            for j in range(len(vd['acquisition1'][i])):
                m = ModelMapper(PropertyAcquisitionTitle, vd, getter=lambda param_name: vd[param_name][i][j])
                m.map(rename={
                    'title': 'acquisition1',
                    'year': 'acquisition-year',
                    'month': 'acquisition-month',
                    'day': 'acquisition-day'
                })
                m.map_one('title', 'acquisition-other')

                title = m.create()
                title.property = p
                title.save()

            # # Map it when replying data from CrowData
            # get_checkbox('cultivation_belterulet', 'cultivation_checkbox1')
            # get_checkbox('cultivation_kulterulet', 'cultivation_checkbox2')
            # get_checkbox('cultivation_lakas', 'cultivation_checkbox3')
            #
            # get_checkbox('building_nature_garazs', 'building_nature1')
            # get_checkbox('building_nature_lakohaz', 'building_nature2')
            # get_checkbox('building_nature_udulo', 'building_nature3')
            #
            #
            # get_checkbox('legal_designation_csaladi_haz', 'legal_designation1')
            # get_checkbox('legal_designation_tarsashaz', 'legal_designation2')
            # get_checkbox('legal_designation_garazs', 'legal_designation3')
            #
            # get_checkbox('legal_status_tulajdonos', 'legal_status1')
            # get_checkbox('legal_status_haszonelvezo', 'legal_status2')
            # get_checkbox('legal_status_berlo', 'legal_status3')
            #
            # get('ownership_ratio_numerator', 'ownership_ratio1', convert=int)
            # get('ownership_ratio_denominator', 'ownership_ratio2', convert=int)


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
