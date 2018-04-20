from _datetime import datetime
import dateutil.parser
import json
from pytz import timezone

from .models import (
    Relative, Politician, Party, Declaration, Property, PropertyAcquisitionTitle,
    ArtWork, Security, Savings, Cash, Obligation, Debt, Income, EconomicInterest,
    Benefit, Present, Subsidy,
)


def import_data():
    document_pks = []
    with open('shared/json/dbdata_2018-02-02_0300.json') as data_file:
        data = json.load(data_file)
        # Run 1st time to import parties
        for record in data:
            if record['model'] == 'crowdataapp.party':
                # it was UTC originally
                created_at = dateutil.parser.parse(record['fields']['created_at']).replace(tzinfo=timezone("Europe/London"))
                updated_at = dateutil.parser.parse(record['fields']['updated_at']).replace(tzinfo=timezone("Europe/London"))
                party, created = Party.objects.get_or_create(
                    pk=record['pk'],
                    name=record['fields']['name'],
                    short_name=record['fields']['short_name'],
                    parldata_id=record['fields']['parldata_id'],
                )
                party.created_at=created_at
                party.updated_at=updated_at
                party.save()

        # Run 2nd time to import politicians
        for record in data:
            if record['model'] == 'crowdataapp.politician':
                # it was UTC originally
                created_at = dateutil.parser.parse(record['fields']['created_at']).replace(tzinfo=timezone("Europe/London"))
                updated_at = dateutil.parser.parse(record['fields']['updated_at']).replace(tzinfo=timezone("Europe/London"))
                politician, created = Politician.objects.get_or_create(
                    pk=record['pk'],
                    name=record['fields']['name'],
                    parliamentary_id=record['fields']['parliamentary_id'],
                    image_url=record['fields']['image_url'],
                    party_id=record['fields']['party'],
                    parldata_id=record['fields']['parldata_id'],
                )
                politician.created_at=created_at
                politician.updated_at=updated_at
                politician.save()

        # Run 3rd time to import declarations (old documents)
        for record in data:
            if record['model'] == 'crowdataapp.document':
                for_year = record['fields']['name'].split(' ')[-1].split('-')[0]
                document_pks.append(record['pk'])
                declaration, created = Declaration.objects.get_or_create(
                    pk=record['pk'],
                    url=record['fields']['url'],
                    politician_id=record['fields']['politician'],
                    for_year=for_year,
                    # financial_other
                )

        # Run 4th time to import declarations (old documents)
        entries = {}
        for record in data:
            # ???????????
            # 1 => newsletter_email (Newsletter Email)

            # Relative
            # 2 => spouse (Házas-/élettárs)
            # 3 => children (Gyermek)

            # Property
            # 4 => location (Település)                         # Property.location
            # 5 => area (Az ingatlan teljes területe:)          # Property.area
            # 6 => area_unit ( Ingatlan terület mértékegység)   # Property.area_unit

            # 7 => cultivation_checkbox1 (Ingatlan műv belterület/művelés alól kivett)# Property.cultivation_belterulet
            # 8 => cultivation_checkbox2 (Ingatlan műv külterület)      # Property.cultivation_kulterulet
            # 9 => cultivation_checkbox3 (Ingatlan műv lakás/lakóház)   # Property.cultivation_lakas
            # 10 => cultivation_other (Ingatlan műv egyéb)              # Property.cultivation_other

            # 11 => building_nature1 (Ing rend garázs)          # Property.building_nature_garazs
            # 12 => building_nature2 (Ing rend lakóház)         # Property.building_nature_lakohaz
            # 13 => building_nature3 (Ing rend üdülő/nyaraló)   # Property.building_nature_udulo
            # 14 => building_nature_other (Ing rend egyéb)      # Property.building_nature_other

            # 15 => legal_designation1 (Ing jog családi ház)    # Property.legal_designation_csaladi_haz
            # 16 => legal_designation2 (Ing jog társasház)      # Property.legal_designation_tarsashaz
            # 17 => legal_designation3 (Ing jog garázs)         # Property.legal_designation_garazs
            # 18 => legal_designation_other (Ing jog egyéb)     # Property.legal_designation_other

            # 19 => legal_status1 (Ing jogá tulajdonos )        # Property.legal_status_tulajdonos
            # 20 => legal_status2 (Ing jogá haszonélvező)       # Property.legal_status_haszonelvezo
            # 21 => legal_status3 (Ing jogá bérlő)              # Property.legal_status_berlo
            # 22 => legal_status_other (Ing jogá egyéb)         # Property.legal_status_other

            # 23 => ownership_ratio1 (Tul hány 1)               # Property.ownership_ratio_numerator
            # 24 => ownership_ratio2 (Tul hány 1)               # Property.ownership_ratio_denominator
            # 25 => ownership_ratio_percent (Tul hány %)        # Property.ownership_ratio_percent

            # ???????????
            # 26 => acquisition1 (Szerzés jogcíme)              # Property.legal_designation_other
            # 33 => acquisition_date (Szerzés ideje)            # Property.legal_designation_other
            # 34 => property_category ( )                       # Property.legal_designation_other
            # 37 => something_wrong (Megjegyzés)                # Property.legal_designation_other

            # Vehicle
            # 38 => vehicle_type (Gépjármű jellege)             # Property.type_general / type ???
            # 39 => subtype (G jTípusa)                         # Property.subtype
            # 40 => acq_time (Gj Szerzés ideje)                 # Property.legal_designation_other
            # 41 => acq (Gj Szerzés jogcíme)                    # Property.legal_designation_other
            # 42 => water_aero_type (Vízi vagy légi jármű jellege)
            # 43 => wa_subtype (Vízi Típus)
            # 44 => wa_acq_time (Vízi Szerzés ideje)
            # 45 => wa_acq (Vízi Szerzés jogcíme)

            # ArtWork
            # 46 => artwork_type (Védett műalkotás, védett gyűjtemény, egyéb értékes ingóság jellege)
            # 47 => artwork_name (Védmű Megnevezés)             # ArtWork.name
            # 48 => artwork_pieces (Védmű db)                   # ArtWork.pieces
            # 49 => artwork_acq_time (Védmű Szerzés ideje)
            # 50 => artwork_acq (Védmű Szerzés jogcíme)


            # 51 => inv_name (Értékpapírban elhelyezett megtakarítás, vagy egyéb befektetés)
            # 52 => inv_value (Értékp Névérték)
            # 53 => inv_curr (Értékp pénznem)

            # Security
            # 54 => sec_name (Takarékban elhelyezett megtakarítás)  # Security.name
            # 55 => sec_value (Takarék Névérték)                # Security.value
            # 56 => sec_curr (Takarék pénznem)                  # Security.currency

            # Cash
            # 57 => cash (Készpénz)
            # 58 => cash_curr (Kp pénznem)

            # Obligation
            # 59 => obligation_type (Számla- vagy pénzkövetelés)
            # 60 => obligation_value (Szla összeg)
            # 61 => obligation_curr (Szla pénznem)
            # 62 => obligation_other (Más jelentősebb értékű vagyontárgy)

            # Debt
            # 63 => debt_type (Tartozás típusa)
            # 64 => debt_desc (Tartozás Megnevezés)
            # 65 => debt_value (Tartozás összeg)
            # 66 => debt_curr (Tartozás pénznem)

            # ?????????????
            # 67 => comment (Egyéb közlendők)

            # Income
            # 68 => profession (Foglalkozás)
            # 69 => employer (Fogl Munkahelye/kifizető)
            # 70 => active (Fogl Szünetelteti)
            # 71 => income (Fogl Jövedelme)
            # 72 => income_curr (Fogl pénznem)
            # 73 => regularity (Fogl Rendszeresség)

            # EconomicInterest
            # 74 => co_name (Gazdasági társaság neve)
            # 75 => co_location (Gt Székhelye)
            # 76 => co_type (Gt Formája)
            # 77 => int_beginning (Gt Érdekeltség formája keletkezéskor)
            # 78 => int_now (Gt Érdekeltség formája jelenleg)

            # 79 => ownership_ratio_beg1 (Gt érd kel 1)
            # 80 => ownership_ratio_beg2 (Gt érd kel 2)
            # 81 => ownership_ratio_beg_percent (Gt érd kel %)
            # 82 => ownership_ratio_now1 (Gt érd most 1)
            # 83 => ownership_ratio_now2 (Gt érd most 2)
            # 84 => ownership_ratio_now_percent (Gt érd most %)

            # 85 => profitshare (Gt Nyereségből részesedés)
            # 86 => position (Gt Tisztség)
            # 87 => benefit_date (Juttatás ideje)
            # 88 => benefit_name (Juttatás megnevezése)
            # 89 => benefit_value (Juttatás értéke)
            # 91 => present_date (Ajándék ideje)
            # 92 => present_name (Ajándék megnevezése)
            # 93 => present_value (Ajándék értéke)
            # 94 => present_currency (Ajándék pénznem)
            # 95 => subs_reci (Támogatás jogosultja)
            # 96 => subs_legal (Támogatás Megszerzés jogcíme)
            # 97 => subs_date (Támogatás Időpontja)
            # 98 => subs_provider (Támogatást nyújtó)
            # 99 => subs_purpose (Támogatás Célja)
            # 100 => subs_value (Támogatás Értéke)
            # 101 => subs_curr (Támogatás pénznem)
            # 102 => benefit_curr (Támogatás törvényben meghatározott érték)
            # 104 => building_area (Ing ép ter building area)
            # 105 => building_area_unit (Ing ép ter mérték building area unit)
            # 107 => building_area_unit_other (Ing ép ter egyéb épület terület egyéb)
            # 108 => area_unit_other (Ing terület egyéb)
            # 109 => acq_other (jogcím egyéb)
            # 110 => wa_acq_other (Vízi- légi- egyéb)
            # 111 => artwork_acq_other (műtárgy jogcím egyéb)
            # 112 => sec_curr_other (biztosítás)
            # 113 => cash_curr_other (készpénz pénznem egyéb )
            # 114 => inv_curr_other (befektetés)
            # 115 => obligation_curr_other (pénzkövetelés pénznem egyéb)
            # 116 => debt_curr_other (tartozás pénznem egyéb)
            # 117 => income_curr_other (bevétel pénznem egyéb)
            # 118 => co_type_other (Gt társaság típus egyéb)
            # 119 => int_beginning_other (Gt érdekeltség kezdetekkor egyéb)
            # 120 => int_now_other (Gt érdekeltség jelenleg egyéb)
            # 121 => position_other (Gt tisztség egyéb)
            # 122 => subs_curr_other (támogatás pénznem egyéb)
            # 123 => acquisition-other (acquisition-other)
            # 124 => art_date (art_date)
            # 125 => aw-vehicle_date (aw-vehicle_date)
            # 126 => classic-vehicle_date (classic-vehicle_date)
            # 127 => other_valuable_asset (other_valuable_asset)

            if record['model'] == 'crowdataapp.documentsetfieldentry':
                # print(record)
                if record['fields']['value'] and record['fields']['verified']:
                    # print(record)
                    try:
                        val = json.loads(record['fields']['value'])
                        if type(val) == list:
                            # explained here: https://stackoverflow.com/a/3845453/4018857
                            val = list(filter(None, val))
                            if not len(val):
                                val = None
                    except json.JSONDecodeError:
                        val = record['fields']['value']
                    if val and val != ' ':
                        entry_id = record['fields']['entry']
                        field_id = record['fields']['field_id']
                        if entry_id not in entries:
                            entries[entry_id] = {}
                        if field_id not in entries[entry_id]:
                            entries[entry_id][field_id] = []
                        if type(val) == list:
                            entries[entry_id][field_id] += val
                        else:
                            entries[entry_id][field_id].append(val)

        # for record in data:
        #     if record['model'] not in [
        #         # done
        #         'crowdataapp.party', 'crowdataapp.politician', 'crowdataapp.document',
        #         'crowdataapp.documentsetformfield', # descriptor for forms (important!!!!)
        #         # not yet
        #         'crowdataapp.feedback', # TODO: what to do with this? -> this should be feedback for document
        #
        #         'crowdataapp.documentsetfieldentry',
        #         # nope
        #         'crowdataapp.documentsetformentry', # who filled what
        #         'crowdataapp.documentsetform', # form ID
        #         'crowdataapp.documentset', # this is some event descriptor
        #
        #         'auth.user',
        #         'admin.logentry', 'auth.permission', 'sessions.session', 'south.migrationhistory', 'sites.site',
        #         'contenttypes.contenttype'
        #     ]:
        #         # if record['model'] == 'crowdataapp.documentsetfieldentry':
        #         #     record_key = record['fields']['field_id']
        #         #     if record_key not in form_fields:
        #         #         form_fields[record_key] = 0
        #         #     form_fields[record_key] += 1
        #
        #         # if record['model'] == 'crowdataapp.documentsetformfield':
        #         #     print('{0} => {1} ({2})'.format(record['pk'], record['fields']['slug'], record['fields']['label']))
        #                 # print(record)
        #         # print(record['model'])
        for key, entry in sorted(entries.items()):
            try:
                declaration = Declaration.objects.get(pk=key)
                print('::::::::::::::DECLARATION: {}::::::::::::::'.format(declaration))
                for f_id, vals in sorted(entry.items()):
                    print(f_id, vals)
            except Declaration.DoesNotExist:
                pass
        # print(verified)
        # print(len(entries))

        # print(sorted(list(form_fields.keys())))

        # print(sorted(entries.keys()))
        # print(len(entries.keys()))
        # print(sorted(document_pks))
