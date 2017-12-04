import datetime

from moonsheep.tasks import AbstractTask
from moonsheep.verifiers import *

from .forms import *
from .models import *


class SomeTask(AbstractTask):
    task_template = 'tasks/find_table.html'

    verify_page = EqualsVerifier

    def verify_party_name(self, values):
        return values[0], 1

    def save_verified_data(self, verified_data):
        party, created = PoliticalParty.objects.get_or_create(
            name=verified_data['party_name'],
            legal_id=verified_data['party_legal_id']
        )
        Report.objects.get_or_create(
            report_date=datetime.datetime.strptime(verified_data['report_date'], "%Y-%m-%d"),
            party=party,
            document_page_start=verified_data['page']
        )

    def after_save(self, verified_data):
        self.create_new_task(GetTransactionTask, **verified_data)


    def get_presenter(self):
        return None
        # return presenter.PDFViewer()
