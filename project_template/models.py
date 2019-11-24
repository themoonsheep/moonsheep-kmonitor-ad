from django.db import models
from django.utils.translation import ugettext_lazy as _

from moonsheep.models import DocumentModel
from .fields import AmountField, MyCharField, MyIntegerField, PercentField
from .managers import MyManager


class Relative(models.Model):
    name = models.CharField(_('Full name'), max_length=128)
    spouse_of = models.OneToOneField(
        "Declaration", related_name='spouse', null=True, blank=True, on_delete=models.SET_NULL
    )
    child_of = models.ForeignKey(
        "Declaration", related_name='children', null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class Politician(models.Model):  # crowdataapp_politician.json
    name = models.CharField(_('Full name'), max_length=128)  # crowdataapp_politician.json [name]
    """
    Used in most of the urls of parliamentary website
    """
    parliamentary_id = models.CharField(_('Parliamentary website ID'), max_length=24)  # crowdataapp_politician.json [parliamentary_id]
    image_url = models.URLField(_('Image URL'), max_length=256)  # crowdataapp_politician.json [image_url]
    party = models.ForeignKey(
        "Party", related_name='members', verbose_name='Current MPs party', on_delete=models.PROTECT,
        null=True, blank=True
    )  # crowdataapp_politician.json [party_id]
    parldata_id = models.CharField(_('External ParlData API ID'), max_length=64)  # crowdataapp_politician.json [parldata_id]

    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # crowdataapp_politician.json [created_at]
    updated_at = models.DateTimeField(auto_now=True)  # crowdataapp_politician.json [updated_at]

    objects = MyManager()

    def __str__(self):
        return self.name

    def create_asset_declaration_url(self, year):
        template = 'http://www.parlament.hu/internet/cplsql/ogy_vagyonpub.vagyon_kiir_egys' \
                   + '?P_FNEV=/{year}/{id}_j0{date}k.pdf&p_cont=application/pdf'
        # working example: 'http://www.parlament.hu/aktiv-kepviseloi-nevsor'
        # '?FP_FNEV=/2015/v050_j0151231k.pdf&p_cont=application/pdf'

        from datetime import date, timedelta
        date_filled = date(int(year) + 1, 1, 1) - timedelta(days=1)  # last day of the year

        return template.format(
            id=self.parliamentary_id,
            date=date_filled.strftime('%y%m%d'),
            year=year
        ), date_filled

    class Meta:
        verbose_name = _('Politician')
        verbose_name_plural = _('Politicians')


class Party(models.Model):  # crowdataapp_party.json
    name = models.CharField(_('Full name'), max_length=128)
    short_name = models.CharField(_('Short name'), max_length=128)
    parldata_id = models.CharField(_('External ParlData API ID'), max_length=64)

    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Political Party')
        verbose_name_plural = _('Political Parties')


class Declaration(DocumentModel):  # crowdataapp_document.json
    # DocumentModel fields:
    # url
    # progress

    # crowdataapp_document.json [name] [politician_id]
    politician = models.ForeignKey("Politician", related_name='declarations', on_delete=models.PROTECT)

    for_year = models.IntegerField()  # crowdataapp_document.json [name]

    # Personal Data
    # spouse and children foreign link exists in Relative class

    # Properties: reverse link

    # Financial
    """
    Financial - other [egyéb közlendője]
    """
    financial_other = models.TextField(_('Egyéb közlendők'))  # form input name: comment

    def __str__(self):
        return '{} - {}'.format(self.politician.name, self.for_year)


class Property(models.Model):
    declaration = models.ForeignKey("Declaration", on_delete=models.CASCADE, related_name='properties')

    location = models.CharField(max_length=256)
    area = models.CharField(max_length=128)
    area_unit = models.CharField(max_length=32)

    cultivation_belterulet = models.BooleanField(_('belterület/művelés alól kivett'))
    cultivation_kulterulet = models.BooleanField(_('külterület'))
    cultivation_lakas = models.BooleanField(_('lakás/lakóház'))
    cultivation_other = models.CharField(_('cultivation: other'), max_length=128)

    building_nature_garazs = models.BooleanField(_('garázs'))
    building_nature_lakohaz = models.BooleanField(_('lakóház'))
    building_nature_udulo = models.BooleanField(_('üdülő/nyaraló'))
    building_nature_other = models.CharField(max_length=128)

    building_area = models.CharField(max_length=128)
    building_area_unit = models.CharField(max_length=32)

    legal_designation_csaladi_haz = models.BooleanField(_('családi ház'))
    legal_designation_tarsashaz = models.BooleanField(_('társasház'))
    legal_designation_garazs = models.BooleanField(_('garázs'))
    legal_designation_other = models.CharField(max_length=128)

    legal_status_tulajdonos = models.BooleanField(_('tulajdonos'))
    legal_status_haszonelvezo = models.BooleanField(_('haszonélvező'))
    legal_status_berlo = models.BooleanField(_('bérlő'))
    legal_status_other = models.CharField(max_length=128)

    ownership_ratio_numerator = MyIntegerField()
    ownership_ratio_denominator = MyIntegerField()
    ownership_ratio_percent = PercentField()

    # acquisition_titles are in a separate model: PropertyAcquisitionTitle

    def __str__(self):
        return '[ {} ] {}'.format(self.declaration, self.location)


class PropertyAcquisitionTitle(models.Model):
    property = models.ForeignKey("Property", on_delete=models.CASCADE, related_name='acquisition_titles')

    title = MyCharField()
    year = MyIntegerField()
    month = MyIntegerField()
    day = MyIntegerField()


class Vehicle(models.Model):
    declaration = models.ForeignKey("Declaration", on_delete=models.CASCADE, related_name='vehicles')

    type_general = MyCharField(choices=(('motor', 'motor'), ('water_or_air', 'water_or_air')))
    type = MyCharField(_('Gépjármű jellege'))
    subtype = MyCharField(_('Típusa'))

    acquisition_type = MyCharField(_('Szerzés jogcíme'))  # acq acq_other
    acquisition_year = MyIntegerField()
    acquisition_month = MyIntegerField()


class ArtWork(models.Model):
    declaration = models.ForeignKey("Declaration", on_delete=models.CASCADE, related_name='artwork')

    type = MyCharField(_('Védett műalkotás, védett gyűjtemény, egyéb értékes ingóság jellege'))
    name = MyCharField(_('Megnevezés'))
    pieces = MyCharField(_('db'))

    acquisition_type = MyCharField(_('Szerzés jogcíme'))  # acq acq_other
    acquisition_year = MyIntegerField()
    acquisition_month = MyIntegerField()


class Security(models.Model):
    """
    Értékpapír vagy egyéb befektetés
    """
    declaration = models.ForeignKey("Declaration", on_delete=models.CASCADE, related_name='securities')

    """
    Értékpapírban elhelyezett megtakarítás, vagy egyéb befektetés
    """
    name = MyCharField(_('Értékpapír'))  # form: inv_name
    value = AmountField(_('Névérték'))
    currency = MyCharField(_('pénznem'))


class Savings(models.Model):
    """
    Takarék
    """
    declaration = models.ForeignKey("Declaration", on_delete=models.CASCADE, related_name='savings')

    name = MyCharField(_('Takarékbetétben elhelyezett megtakarítás'))  # form: sec_name
    value = AmountField(_('összeg'))
    currency = MyCharField(_('pénznem'))


class Cash(models.Model):
    """
    Készpénz
    """
    declaration = models.ForeignKey("Declaration", on_delete=models.CASCADE, related_name='cash')

    value = AmountField(_('összeg'))
    currency = MyCharField(_('pénznem'))


class Obligation(models.Model):
    """
    Pénzintézeti számlakövetelés vagy más pénzkövetelés
    """
    declaration = models.ForeignKey("Declaration", on_delete=models.CASCADE, related_name='onligations')

    type = MyCharField()
    value = AmountField(_('összeg'))
    currency = MyCharField(_('pénznem'))


class Debt(models.Model):
    declaration = models.ForeignKey("Declaration", on_delete=models.CASCADE, related_name='debts')

    type = MyCharField(_('Tartozás típusa'))
    description = models.TextField(_('Megnevezés'))
    value = AmountField(_('összeg'))
    currency = MyCharField(_('pénznem'))


class Income(models.Model):
    declaration = models.ForeignKey("Declaration", on_delete=models.CASCADE, related_name='incomes')

    profession = MyCharField(_('Foglalkozás'))
    employer = MyCharField(_('Munkahelye/kifizető'))
    active = models.BooleanField(_('Szünetelteti?'))

    income = MyCharField(_('Jövedelme'))
    currency = MyCharField(_('pénznem'))
    regularity = MyCharField(_('gyakoriság'))


class EconomicInterest(models.Model):
    declaration = models.ForeignKey("Declaration", on_delete=models.CASCADE, related_name='economic_interests')

    name = MyCharField(_('Gazdasági társaság neve'))
    location = MyCharField(_('Székhelye'))
    type = MyCharField(_('Formája'))

    role_beg = MyCharField(_('Érdekeltség formája keletkezéskor'))  # int_beginning, in the beginning
    role_now = MyCharField(_('Érdekeltség formája jelenleg'))  # int_now

    ownership_ratio_beg_numerator = MyIntegerField()
    ownership_ratio_beg_denominator = MyIntegerField()
    ownership_ratio_beg_percent = PercentField()

    ownership_ratio_now_numerator = MyIntegerField()
    ownership_ratio_now_denominator = MyIntegerField()
    ownership_ratio_now_percent = PercentField()

    profit_share = PercentField(_('Nyereségből részesedés'))

    position = MyCharField(_('Tisztség'))


class Benefit(models.Model):
    """
    Juttatás
    """
    declaration = models.ForeignKey("Declaration", on_delete=models.CASCADE, related_name='benefits')

    date = MyCharField(_('ideje'))
    name = MyCharField(_('megnevezése'))
    value = AmountField(_('értéke'))
    currency = MyCharField(_('pénznem'))


class Present(models.Model):
    """
    Ajándék
    """
    declaration = models.ForeignKey("Declaration", on_delete=models.CASCADE, related_name='presents')

    date = MyCharField(_('ideje'))
    name = MyCharField(_('megnevezése'))
    value = AmountField(_('értéke'))
    currency = MyCharField(_('pénznem'))


class Subsidy(models.Model):
    """
    Támogatások
    """
    declaration = models.ForeignKey("Declaration", on_delete=models.CASCADE, related_name='subsidies')

    recipient = MyCharField(_('Támogatás jogosultja'))
    legal = MyCharField(_('Megszerzés jogcíme'))
    date = MyCharField(_('Időpontja'))
    provider = MyCharField(_('Támogatást nyújtó'))
    purpose = MyCharField(_('Célja'))
    value = AmountField(_('Értéke'))
    currency = MyCharField(_('pénznem'))
