from . import vpapi
from ..models import Party, Politician, Declaration


class obj(object):
    def __init__(self, d, none_if_missing=False):
        self.__none_if_missing = none_if_missing
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, obj(b) if isinstance(b, dict) else b)


vpapi.parliament('hu/orszaggyules')


def get_chambers():
    items = vpapi.getall('organizations', where={'classification': 'chamber'})
    return items


def get_parties():
    items = vpapi.getall('organizations', where={'classification': 'party'})
    return items


def import_declarations(chamber_id, year):
    # chamber_id = '550303bc273a39033bab34df'
    parties = {party.parldata_id: party for party in Party.objects.all()}

    politicians_imported = 0
    politicians_existing = 0
    docs_imported = 0
    docs_existing = 0

    chamber = vpapi.get('organizations', chamber_id, embed=["memberships"])
    chamber = obj(chamber, True)

    for related in chamber.memberships:
        if related.person_id:
            politician = Politician.objects.get_or_none(parldata_id=related.person_id)

            if not politician:
                mp = vpapi.get('people', related.person_id, projection={
                    "identifiers.identifier": 1,
                    "image": 1,
                    "name": 1
                }, embed=["memberships.organization"])
                mp = obj(mp, True)

                # create party if needed
                party_obj = None
                for relation in mp.memberships:
                    if hasattr(relation, 'end_date'):
                        continue  # old membership

                    if hasattr(relation, 'organization') and relation.organization.classification == 'party':
                        party = relation.organization
                        if not party.id in parties:
                            party_obj, created = Party.objects.get_or_create(parldata_id=party.id, defaults={
                                'name': party.other_names[0].name if len(party.other_names) else None,
                                'short_name': party.name})
                            parties[party.id] = party_obj
                        else:
                            party_obj = parties[party.id]

                # create MP if needed
                politician, created = Politician.objects.get_or_create(parldata_id=mp.id, defaults={
                    'name': mp.name,
                    'parliamentary_id': mp.identifiers[0].identifier,
                    'image_url': mp.image
                })
                politicians_imported += 1

            else:
                politicians_existing += 1

            # create doc
            document_url, date_filled = politician.create_asset_declaration_url(year)

            doc, created = Declaration.objects.get_or_create(url=document_url, defaults={
                'for_year': year,
                'politician': politician
            })
            if created:
                docs_imported += 1
            else:
                docs_existing += 1

    return {
        'docs_imported': docs_imported,
        'docs_existing': docs_existing,
        'politicians_imported': politicians_imported,
        'politicians_existing': politicians_existing
    }
