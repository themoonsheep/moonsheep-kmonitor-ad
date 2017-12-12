from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404
from django.utils.translation import ugettext_lazy as _


# TODO cleaning: is it needed?
class MyManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def get_or_404(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            raise Http404('No %s matches the given query.' % self.model._meta.object_name)


# TODO make sure it is used
class MyCharField(models.CharField):
    """
    By default can be blank and null. Default length: 128
    """

    def __init__(self, *args, **kwargs):
        if not 'blank' in kwargs:
            kwargs['blank'] = True
        if not 'null' in kwargs:
            kwargs['null'] = True
        if not 'max_length' in kwargs:
            kwargs['max_length'] = 128

        super().__init__(*args, **kwargs)


class Person(models.Model):
    name = models.CharField(_('Full name'), max_length=128, )
    child_in_declaration = models.ForeignKey("Declaration", related_name='children', null=True, blank=True,
                                             on_delete=models.SET_NULL)


class Politician(Person):
    """
    Used in most of the urls of parliamentary website
    """
    parliamentary_id = models.CharField(_('Parliamentary website ID'), max_length=24, )
    image_url = models.URLField(_('Image URL'), max_length=256, )
    party = models.ForeignKey("Party", related_name='members',
                              null=True, blank=True,
                              verbose_name='Current MPs party', on_delete=models.PROTECT)
    parldata_id = models.CharField(_('External ParlData API ID'), max_length=64, )

    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyManager()

    def create_asset_declaration_url(self, year):
        template = 'http://www.parlament.hu/internet/cplsql/ogy_vagyonpub.vagyon_kiir_egys?P_FNEV=/{year}/{id}_j0{date}k.pdf&p_cont=application/pdf'
        # other link; working, but longer
        # template = 'http://www.parlament.hu/aktiv-kepviseloi-nevsor?p_p_id=pairproxy_WAR_pairproxyportlet_INSTANCE_9xd2Wc9jP4z8&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&_pairproxy_WAR_pairproxyportlet_INSTANCE_9xd2Wc9jP4z8_pairAction=%2Finternet%2Fcplsql%2Fogy_vagyonpub.vagyon_kiir_egys%3FP_FNEV%3D%2F2015%2Fv050_j0151231k.pdf%26p_cont%3Dapplication%2Fpdf'

        from datetime import date, timedelta
        date_filled = date(int(year) + 1, 1, 1) - timedelta(days=1)  # last day of the year

        return (template.format(id=self.parliamentary_id,
                                date=date_filled.strftime('%y%m%d'),
                                year=year), date_filled)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Politician')
        verbose_name_plural = _('Politicians')


class Party(models.Model):
    name = models.CharField(_('Full name'), max_length=128, )
    short_name = models.CharField(_('Short name'), max_length=128, )
    parldata_id = models.CharField(_('External ParlData API ID'), max_length=64, )

    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Political Party')
        verbose_name_plural = _('Political Parties')


class Declaration(models.Model):
    politician = models.ForeignKey("Politician", related_name='declarations',
                                   null=True, blank=True, on_delete=models.PROTECT)
    party = models.ForeignKey("Party",
                              null=True, blank=True,
                              verbose_name='MPs party at the time of declaration import',
                              on_delete=models.PROTECT)
    for_year = models.IntegerField()

    # Personal Data
    spouse = models.ForeignKey("Person", related_name='declaration_mentions', null=True, blank=True,
                               on_delete=models.PROTECT)
    # children foreign link exists in Person

    # Properties: reverse link


class Property(models.Model):
    location = models.CharField(max_length=256)
    area = models.CharField(max_length=128)
    area_unit = models.CharField(max_length=32)

    cultivation_belterulet = models.BooleanField(_('belterület/művelés alól kivett'), required=False)
    cultivation_kulterulet = models.BooleanField(_('külterület'), required=False)
    cultivation_lakas = models.BooleanField(_('lakás/lakóház'), required=False)
    cultivation_other = models.CharField(_('cultivation: other'), max_length=128)

    building_nature_garazs = models.BooleanField(_('garázs'), required=False)
    building_nature_lakohaz = models.BooleanField(_('lakóház'), required=False)
    building_nature_udulo = models.BooleanField(_('üdülő/nyaraló'), required=False)
    building_nature_other = models.CharField(max_length=128)

    building_area = models.CharField(max_length=128)
    building_area_unit = models.CharField(max_length=32)

    legal_designation_csaladi_haz = models.BooleanField(_('családi ház'), required=False)
    legal_designation_tarsashaz = models.BooleanField(_('társasház'), required=False)
    legal_designation_garazs = models.BooleanField(_('garázs'), required=False)
    legal_designation_other = models.CharField(max_length=128)

    legal_status_tulajdonos = models.BooleanField(_('tulajdonos'), required=False)
    legal_status_haszonelvezo = models.BooleanField(_('haszonélvező'), required=False)
    legal_status_berlo = models.BooleanField(_('bérlő'), required=False)
    legal_status_other = models.CharField(max_length=128)

    ownership_ratio_percent = models.DecimalField()

    category = MyCharField()

    # acquisition_titles are in a separate model: PropertyAcquisitionTitle


class PropertyAcquisitionTitle(models.Model):
    property = models.ForeignKey("Property", on_delete=models.CASCADE, related_name='acquisition_titles')

    title = MyCharField()
    date = models.DateField()




# 			   <input type="radio" id="radio1-v" name="__radio1v" value="yes" class="box-toggler" data-toggle-target=".vehicles"> Igen
# 				<input type="radio" id="radio2-v" name="__radio1v" value="no"  class="box-toggler" data-toggle-target=".vehicles"> Nem
# 				<select class="form-control" name="vehicle_type[]" title="type">
# 			  <input class="form-control" name="subtype[]" type="text" placeholder="Típusa">
# 			  <select class="form-control" name="acq[]" title="Szerzés jogcíme">
# 			  <input type="text" name="acq_other[]" class="form-control hidden other-input">
# 				<input class="form-control" name="classic-vehicle-year[]" type="number" placeholder="év" maxlength="4" min="1800" max="2017"></div>
# 			  <select name="classic-vehicle-month[]" class="form-control selectpicker" placeholder="month" title="month" data-live-search="true">
# 			  <input class="form-control" name="water_aero_type[]" placeholder="Vízi vagy légi jármű jellege">
# 			  <input class="form-control" name="wa_subtype[]" type="text" placeholder="Típus">
# 			  <select class="form-control" name="wa_acq[]" title="Szerzés jogcíme">
# 			  <input type="text" name="wa_acq_other[]" class="form-control hidden other-input">
# 			<div class="col-md-3"><label>&Egrave;v</label><input name="aw-vehicle-year[]" class="form-control" type="number" placeholder="év" maxlength="4" min="1800" max="2017"></div>
# 			  <select class="form-control selectpicker" name="aw-vehicle-month[]" placeholder="month" title="month" data-live-search="true">
# 			  <select class="form-control" name="artwork_type[]" title="Védett műalkotás, védett gyűjtemény, egyéb értékes ingóság jellege">
# 			  <input class="form-control" name="artwork_name[]" placeholder="Megnevezés" type="text">
# 			  <input class="form-control" name="artwork_pieces[]" placeholder="db" type="text">
# 			  <select class="form-control" name="artwork_acq[]" title="Szerzés jogcíme">
# 			  <input type="text" name="artwork_acq_other[]" class="form-control hidden other-input">
# 			<div class="col-md-3"><label >&Egrave;v</label><input name="art-year[]" class="form-control" type="number" placeholder="év" maxlength="4" min="1800" max="2017"></div>
# 			  <select class="form-control selectpicker" name="art-month[]" placeholder="month" title="month" data-live-search="true">
# 		  <input type="radio" id="radio2-1" name="__radio2" value="yes" class="box-toggler" data-toggle-target=".contents-2"> Igen
# 		  <input type="radio" id="radio2-2" name="__radio2" value="no"  class="box-toggler" data-toggle-target=".contents-2"> Nem
#                   <input type="text" name="inv_name[]" class="form-control" title="Értékpapírban elhelyezett megtakarítás, vagy egyéb befektetés" placeholder="Értékpapírban elhelyezett megtakarítás, vagy egyéb befektetés">
#                   <input type="text" name="inv_value[]" class="form-control" title="Névérték" placeholder="Névérték">
#                   <select class="form-control" name="inv_curr[]" title="pénznem">
# 			  <input type="text" class="form-control hidden other-input " name="inv_curr_other[]">
#               <input type="text" name="sec_name[]" class="form-control" placeholder="Takarékbetétben elhelyezett megtakarítás"/>
#               <input type="text" name="sec_value[]" class="form-control" placeholder="Névérték"/>
#               <select class="form-control" name="sec_curr[]" title="pénznem">
# 		  <input type="text" class="form-control hidden other-input " name="sec_curr_other[]">
#               <input type="text" name="cash[]" class="form-control">
#               <select class="form-control" name="cash_curr[]" title="pénznem">
# 		  <input type="text" class="form-control hidden other-input " name="cash_curr_other[]">
# 			<select class="form-control" name="obligation_type[]" title="Számla- vagy pénzkövetelés">
# 			<input type="text" name="obligation_value[]" class="form-control">
# 			<select class="form-control" name="obligation_curr[]" title="pénznem">
# 			<input type="text" class="form-control hidden other-input " name="obligation_curr_other[]">
#               <input type="radio" id="radio3-1" name="__radio3" value="yes" class="box-toggler" data-toggle-target=".contents-3"> Igen
#               <input type="radio" id="radio3-2" name="__radio3" value="no"  class="box-toggler" data-toggle-target=".contents-3"> Nem
#                 <select class="form-control" name="debt_type[]" title="Tartozás típusa">
#                 <input type="text" name="debt_desc[]" class="form-control" placeholder="Megnevezés">
#                 <input type="text" name="debt_value[]" class="form-control" placeholder="összeg">
#                 <select class="form-control" name="debt_curr[]" title="pénznem">
# 			<input type="text" class="form-control hidden other-input " name="debt_curr_other[]">
#               <input type="radio" id="radio4-1" name="__radio4" value="yes" class="box-toggler" data-toggle-target=".contents-4"> Igen
#               <input type="radio" id="radio4-2" name="__radio4" value="no"  class="box-toggler" data-toggle-target=".contents-4"> Nem
#                 <textarea name="comment" class="form-control" placeholder="Egyéb közlendők" rows="6"></textarea>
#               <input type="radio" id="radio5-1" name="__radio5" value="yes" class="box-toggler" data-toggle-target=".contents-5"> Igen
#               <input type="radio" id="radio5-2" name="__radio5" value="no"  class="box-toggler" data-toggle-target=".contents-5"> Nem
#                 <input type="text" name="profession[]" class="form-control" placeholder="Foglalkozás">
#                 <input type="text" name="employer[]" class="form-control" placeholder="Munkahelye/kifizető">
#                 <select class="form-control" name="active[]" title="Szünetelteti?">
#               <div class="col-md-3"><input type="text" name="income[]" class="form-control" placeholder="Jövedelme"></div>
#                 <select class="form-control" name="income_curr[]" title="pénznem">
# 			<input type="text" class="form-control hidden other-input " name="income_curr_other[]">
#               <div class="col-md-3"><input type="text" name="regularity[]" class="form-control" placeholder="gyakoriság"></div>
#               <input type="radio" id="radio6-1" name="__radio6" value="yes" class="box-toggler" data-toggle-target=".contents-6"> Igen
#               <input type="radio" id="radio6-2" name="__radio6" value="no"  class="box-toggler" data-toggle-target=".contents-6"> Nem
#                 <input class="form-control" name="co_name[]" placeholder="Gazdasági társaság neve">
#                 <input class="form-control" name="co_location[]" placeholder="Székhelye">
#                 <select class="form-control" name="co_type[]" title="Formája">
# 			<input type="text" class="form-control hidden other-input " name="co_type_other[]">
#                 <select class="form-control" name="int_beginning[]" title="Érdekeltség formája keletkezéskor">
# 			<input type="text" class="form-control hidden other-input " name="int_beginning_other[]">
#                 <select class="form-control" name="int_now[]" title="Érdekeltség formája jelenleg">
# 			<input type="text" class="form-control hidden other-input " name="int_now_other[]">
#                     <input class="form-control" name="ownership_ratio_beg1[]" type="text">
#                     <input class="form-control" type="text" name="ownership_ratio_beg2[]">
#                       <input type="text" class="form-control" name="ownership_ratio_beg_percent[]" placeholder="százalék..." aria-describedby="percent-addon">
#                     <input class="form-control" name="ownership_ratio_now1[]" type="text">
#                     <input class="form-control" type="text" name="ownership_ratio_now2[]">
#                       <input type="text" class="form-control" name="ownership_ratio_now_percent[]" placeholder="százalék..." aria-describedby="percent-addon">
#                   <input type="text" class="form-control" name="profitshare[]" placeholder="%..." aria-describedby="percent-addon">
#                 <select class="form-control" name="position[]" title="Tisztség">
# 			<input type="text" class="form-control hidden other-input " name="position_other[]">
#               <input type="radio" id="radio7-1" name="__radio7" value="yes" class="box-toggler" data-toggle-target=".contents-7"> Igen
#               <input type="radio" id="radio7-2" name="__radio7" value="no"  class="box-toggler" data-toggle-target=".contents-7"> Nem
#                 <input type="text" name="benefit_date[]" class="form-control" placeholder="Juttatás ideje">
# 			<input type="text" class="form-control" name="benefit_name[]" title="Juttatás megnevezése">
#                 <input type="text" name="benefit_value[]" class="form-control" placeholder="értéke">
#                 <select class="form-control" name="benefit_curr[]" title="pénznem">
#                 <input type="text" name="present_date[]" class="form-control" placeholder="Ajándék ideje">
#                 <input class="form-control" name="present_name[]" title="Ajándék megnevezése" placeholder="Ajándék megnevezése"/>
#                 <input type="text" name="present_value[]" class="form-control" placeholder="Ajándék értéke">
#                 <select class="form-control" name="present_currency[]" title="pénznem">
#                 <input type="text" name="subs_reci[]" class="form-control" placeholder="Támogatás jogosultja">
#                 <input type="text" name="subs_legal[]" class="form-control" placeholder="Megszerzés jogcíme">
#                 <input type="text" name="subs_date[]" class="form-control" placeholder="Időpontja">
#                 <input type="text" name="subs_provider[]" class="form-control" placeholder="Támogatást nyújtó">
#                 <input type="text" name="subs_purpose[]" class="form-control" placeholder="Célja">
#                 <input type="text" name="subs_value[]" class="form-control" placeholder="Értéke">
#                 <select class="form-control" name="subs_curr[]" title="pénznem">
# 			<input type="text" class="form-control hidden other-input " name="subs_curr_other[]">
# <p> Instantly verify this document: <input type="checkbox" name="staff_force_verification"><br/>
#
