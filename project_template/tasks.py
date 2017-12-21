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


class S1PersonalData(AbstractTask):
    """
    Személyes információk
    """
    task_form_template = 'tasks/personal_data.html'

    create_mocked_task = create_mocked_task

    def save_verified_data(self, vd: dict):
        d = Declaration.objects.get(url=self.url)

        if vd['spouse'].strip():
            Relative.objects.get_or_create(spouse_of=d, name=vd['spouse'].strip())

        for child in vd['children']:
            if child.strip():
                Relative.objects.get_or_create(child_of=d, name=child.strip())


class S2Properties(AbstractTask):
    """
    Ingatlanok
    """
    task_form_template = 'tasks/properties.html'

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


class S3Movables(AbstractTask):
    """
    Nagy értékű ingóságok
    """
    task_form_template = 'tasks/movables.html'

    create_mocked_task = create_mocked_task

    def save_verified_data(self, vd: dict):
        d = Declaration.objects.get(url=self.url)

        # TODO assuming this declarations has not been verified
        # otherwise we need to get existing objects, order them by how they were saved (additional field)
        # and update their properties!

        for i in range(len(vd['vehicle_type'])):
            m = ModelMapper(Vehicle, vd, getter=lambda param_name: vd[param_name][i])
            m.map(rename={
                'type': 'vehicle_type',
                'subtype': 'subtype',
                'acquisition_type': 'acq',
                'acquisition_year': 'classic-vehicle-year',
                'acquisition_month': 'classic-vehicle-month'
            })

            # Overwrite _other fields if they are set
            m.map_one('acq', 'acq_other')

            m.create(declaration=d, type_general='motor').save()

        for i in range(len(vd['vehicle_type'])):
            m = ModelMapper(Vehicle, vd, getter=lambda param_name: vd[param_name][i])
            m.map(rename={
                'type': 'water_aero_type',
                'subtype': 'wa_subtype',
                'acquisition_type': 'wa_acq',
                'acquisition_year': 'aw-vehicle-year',
                'acquisition_month': 'aw-vehicle-month'
            })

            # Overwrite _other fields if they are set
            m.map_one('wa_acq', 'wa_acq_other')

            m.create(declaration=d, type_general='water_or_air').save()

        for i in range(len(vd['artwork_type'])):
            m = ModelMapper(ArtWork, vd, getter=lambda param_name: vd[param_name][i])
            m.map(rename={
                'type': 'artwork_type',
                'name': 'artwork_name',
                'pieces': 'artwork_pieces',
                'acquisition_type': 'artwork_acq',
                'acquisition_year': 'art-year',
                'acquisition_month': 'art-month'
            })

            # Overwrite _other fields if they are set
            m.map_one('artwork_acq', 'artwork_acq_other')

            m.create(declaration=d).save()


class S4FinancialAndOther(AbstractTask):
    """
    tartozások ?
    megtakarításról, befektetésről, pénzkövetelésről, tartozásokról
    savings, investments, money claims, debts

    egyéb közlendők (other)
    """
    task_form_template = 'tasks/financial.html'

    create_mocked_task = create_mocked_task

    def save_verified_data(self, vd: dict):
        d = Declaration.objects.get(url=self.url)

        # TODO assuming this declarations has not been verified
        # otherwise we need to get existing properties, order them by how they were saved (additional field)
        # and update their properties!

        for i in range(len(vd['inv_name'])):
            m = ModelMapper(Security, vd, getter=lambda field_name: vd['inv_' + field_name][i])
            m.map()
            # Changed fields
            # inv_curr -> inv_currency

            # Overwrite _other fields if they are set
            m.map_one('currency', 'currency_other').create(declaration=d).save()

        for i in range(len(vd['sec_name'])):
            m = ModelMapper(Savings, vd, getter=lambda field_name: vd['sec_' + field_name][i])
            m.map()
            # Changed fields
            # sec_curr -> sec_currency + other

            # Overwrite _other fields if they are set
            m.map_one('currency', 'currency_other').create(declaration=d).save()

        for i in range(len(vd['cash_value'])):
            m = ModelMapper(Cash, vd, getter=lambda field_name: vd['cash_' + field_name][i])
            m.map()
            # Changed fields:
            # cash_curr -> cash_currency + other;
            # cash -> cash_value

            # Overwrite _other fields if they are set
            m.map_one('currency', 'currency_other').create(declaration=d).save()

        for i in range(len(vd['obligation_type'])):
            m = ModelMapper(Obligation, vd, getter=lambda param_name: vd['obligation_' + param_name][i])
            m.map()

            # Changed fields: obligation_curr -> obligation_currency + other

            # Overwrite _other fields if they are set
            m.map_one('currency', 'currency_other').create(declaration=d).save()

        for i in range(len(vd['debt_type'])):
            m = ModelMapper(Debt, vd, getter=lambda field_name: vd['debt_' + field_name][i])
            m.map()

            # Changed fields
            # debt_curr -> debt_curency
            # debt_desc -> debt_desciption

            # Overwrite _other fields if they are set
            m.map_one('currency', 'debt_currency').create(declaration=d).save()

        if vd['financial_other'].strip():
            d.financial_other = vd['financial_other'].strip()


class S5Income(AbstractTask):
    """
    Jövedelemnyilatkozat
    """
    task_form_template = 'tasks/income.html'

    create_mocked_task = create_mocked_task

    def save_verified_data(self, vd: dict):
        d = Declaration.objects.get(url=self.url)

        # TODO assuming this declarations has not been verified
        # otherwise we need to get existing properties, order them by how they were saved (additional field)
        # and update their properties!

        for i in range(len(vd['profession'])):
            m = ModelMapper(Income, vd, getter=lambda param_name: vd[param_name][i])
            m.map()

            # Changed fields
            # income_curr -> currency

            # Overwrite _other fields if they are set
            m.map_one('currency', 'currency_other')

            m.create(declaration=d).save()


class S6EconomicInterest(AbstractTask): # TODO continue THIS
    """
    érdekeltségi
    """
    task_form_template = 'tasks/economic_interest.html'

    create_mocked_task = create_mocked_task

    def save_verified_data(self, vd: dict):
        d = Declaration.objects.get(url=self.url)

        # TODO assuming this declarations has not been verified
        # otherwise we need to get existing properties, order them by how they were saved (additional field)
        # and update their properties!
        # TODO
        for i in range(len(vd['name'])):
            m = ModelMapper(EconomicInterest, vd, getter=lambda param_name: vd[param_name][i])
            m.map()

            # Changes from previous version
            # co_name -> name
            # co_location -> location
            # co_type -> type
            # int_beginning -> role_beg + other
            # int_now -> role_now + other
            # ownership_ratio_beg1 -> ownership_ratio_beg_numerator  + now
            # ownership_ratio_beg2-> ownership_ratio_beg_denominator  +now
            # profitshare -> profit_share

            # Overwrite _other fields if they are set
            m.map_one('type', 'type_other')\
                .map_one('role_beg', 'role_beg_other')\
                .map_one('role_now', 'role_now_other')\
                .map_one('position', 'position_other')

            m.create(declaration=d).save()


class S7Benefits(AbstractTask):
    """
    juttatásról, ajándékról, támogatásról
    benefits, gifts, or subsidies
    """
    task_form_template = 'tasks/benefits.html'

    create_mocked_task = create_mocked_task

    def save_verified_data(self, vd: dict):
        d = Declaration.objects.get(url=self.url)

        # TODO assuming this declarations has not been verified
        # otherwise we need to get existing properties, order them by how they were saved (additional field)
        # and update their properties!

        for i in range(len(vd['benefit_date'])):
            m = ModelMapper(Benefit, vd, getter=lambda fld_name: vd['benefit_' + fld_name][i])
            m.map().create(declaration=d).save()

            # Changed
            # benefit_curr -> benefit_currency

        for i in range(len(vd['present_date'])):
            m = ModelMapper(Present, vd, getter=lambda fld_name: vd['present_' + fld_name][i])
            m.map().create(declaration=d).save()

        for i in range(len(vd['subs_recipient'])):
            m = ModelMapper(Subsidy, vd, getter=lambda fld_name: vd['subs_' + fld_name][i])
            m.map().create(declaration=d).save()

            # Changed fields
            # subs_reci -> subs_recipient
            # subs_curr -> subs_currency + other
