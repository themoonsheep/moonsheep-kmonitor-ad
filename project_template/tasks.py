import datetime

from moonsheep.tasks import AbstractTask
from moonsheep.verifiers import *

from .forms import *
from .models import *


def create_mocked_task(self, base):
    base['info'][
        'url'] = 'http://www.parlament.hu/internet/cplsql/ogy_vagyonpub.vagyon_kiir_egys?P_FNEV=/2016/l001_j0161231k.pdf&p_cont=application/pdf'
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
