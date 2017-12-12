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

class Person(models.Model):
    name = models.CharField(_('Full name'), max_length='128', )


class Politician(Person):
    """
    Used in most of the urls of parliamentary website
    """
    parliamentary_id = models.CharField(_('Parliamentary website ID'), max_length='24', )
    image_url = models.URLField(_('Image URL'), max_length='256', )
    party = models.ForeignKey("Party", related_name='members',
                              null=True, blank=True,
                              verbose_name='Current MPs party', )
    parldata_id = models.CharField(_('External ParlData API ID'), max_length='64', )

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
    name = models.CharField(_('Full name'), max_length='128', )
    short_name = models.CharField(_('Short name'), max_length='128', )
    parldata_id = models.CharField(_('External ParlData API ID'), max_length='64', )

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
                                   null=True, blank=True)
    party = models.ForeignKey("Party",
                              null=True, blank=True,
                              verbose_name='MPs party at the time of declaration import')
    for_year = models.IntegerField()

<form name="elForma" id="elForm" action="{{ form.get_absolute_url }}" method="post" {% if form_for_form.is_multipart %}enctype="multipart/form-data"{% endif %} role="form" class="center-block">
    <input type="hidden" name="__document_id" value="{{ document.id }}"/>
                          <input class="form-control" type="text" id="spouse" name="spouse" class="form-control">
                          <input class="form-control" type="text" id="child" name="children[]" class="form-control">
									   <input type="radio" id="radio1-1" name="__radio1" value="yes" class="box-toggler" data-toggle-target=".contents-1"> Igen
								 <input type="radio" id="radio1-2" name="__radio1" value="no"  class="box-toggler" data-toggle-target=".contents-1"> Nem
								<input class="form-control" type="text" name="location[]" class="form-control">
								 <input class="form-control" type="text" name="area[]" class="form-control">
								<select class=" form-control" name="area_unit[]" title="unit">
								<input type="text" class="form-control hidden other-input" name="area_unit_other[]" >
									<input type="checkbox" name="cultivation_checkbox1[]"> belterület/művelés alól kivett
									<input type="checkbox" name="cultivation_checkbox2[]"> külterület
									<input type="checkbox" name="cultivation_checkbox3[]"> lakás/lakóház
									<input type="text" name="cultivation_other[]" class="form-control" placeholder="Egyéb">
									   <input type="checkbox" name="building_nature1[]"> garázs
									   <input type="checkbox" name="building_nature2[]"> lakóház
									   <input type="checkbox" name="building_nature3[]"> üdülő/nyaraló
									   <input type="text" name="building_nature_other[]" class="form-control" placeholder="Egyéb">
									  <input type="text" class="form-control" name="building_area[]">
									  <select class=" form-control" name="building_area_unit[]" title="unit">
									  <input type="text" class="form-control hidden other-input" name="building_area_unit_other[]" >
									   <input type="checkbox" name="legal_designation1[]"> családi ház
									   <input type="checkbox" name="legal_designation2[]"> társasház
									   <input type="checkbox" name="legal_designation3[]"> garázs
									   <input type="text" name="legal_designation_other[]" class="form-control" placeholder="Egyéb">
									   <input type="checkbox" name="legal_status1[]"> tulajdonos
									   <input type="checkbox" name="legal_status2[]"> haszonélvező
									   <input type="checkbox" name="legal_status3[]"> bérlő
									   <input type="text" name="legal_status_other[]" class="form-control" placeholder="Egyéb">
								  <input class="form-control" type="text" name="ownership_ratio1[]">
								  <input class="form-control" type="text" name="ownership_ratio2[]">
									<input type="text" name="ownership_ratio_percent[]" class="form-control" placeholder="százalék" aria-describedby="percent-addon">
										  <select id="select1" class=" form-control" name="acquisition1[0][]" data-live-search="true" title="Enter value" placeholder="">
										  <input type="text" name="acquisition-other[0][]" id="select1-other" class="hidden form-control other-input" placeholder="Enter value for the selection here">
									<input class="form-control" name="acquisition-year[0][]" type="number" placeholder="év" maxlength="4" min="1800" max="2017">
									<select class="form-control "  name="acquisition-month[0][]" placeholder="month" title="month" data-live-search="true">
										<input class="form-control"  name="acquisition-day[0][]" type="number" placeholder="nap" maxlength="2" min="1" max="31">
									  <input type="radio" id="property_category" name="property_category[]" value="home">
									  <input type="radio" name="property_category[]" value="map">
									  <input type="radio" name="property_category[]" value="asterisk">
									<textarea class="feedback-flag form-control" rows="4" name="something_wrong[]" placeholder="Láttál valami gyanúsat? Volt valami, ami nem tiszta?"></textarea>
							   <input type="radio" id="radio1-v" name="__radio1v" value="yes" class="box-toggler" data-toggle-target=".vehicles"> Igen
								<input type="radio" id="radio2-v" name="__radio1v" value="no"  class="box-toggler" data-toggle-target=".vehicles"> Nem
								<select class="form-control" name="vehicle_type[]" title="type">
							  <input class="form-control" name="subtype[]" type="text" placeholder="Típusa">
							  <select class="form-control" name="acq[]" title="Szerzés jogcíme">
							  <input type="text" name="acq_other[]" class="form-control hidden other-input">
								<input class="form-control" name="classic-vehicle-year[]" type="number" placeholder="év" maxlength="4" min="1800" max="2017"></div>
							  <select name="classic-vehicle-month[]" class="form-control selectpicker" placeholder="month" title="month" data-live-search="true">
							  <input class="form-control" name="water_aero_type[]" placeholder="Vízi vagy légi jármű jellege">
							  <input class="form-control" name="wa_subtype[]" type="text" placeholder="Típus">
							  <select class="form-control" name="wa_acq[]" title="Szerzés jogcíme">
							  <input type="text" name="wa_acq_other[]" class="form-control hidden other-input">
							<div class="col-md-3"><label>&Egrave;v</label><input name="aw-vehicle-year[]" class="form-control" type="number" placeholder="év" maxlength="4" min="1800" max="2017"></div>
							  <select class="form-control selectpicker" name="aw-vehicle-month[]" placeholder="month" title="month" data-live-search="true">
							  <select class="form-control" name="artwork_type[]" title="Védett műalkotás, védett gyűjtemény, egyéb értékes ingóság jellege">
							  <input class="form-control" name="artwork_name[]" placeholder="Megnevezés" type="text">
							  <input class="form-control" name="artwork_pieces[]" placeholder="db" type="text">
							  <select class="form-control" name="artwork_acq[]" title="Szerzés jogcíme">
							  <input type="text" name="artwork_acq_other[]" class="form-control hidden other-input">
							<div class="col-md-3"><label >&Egrave;v</label><input name="art-year[]" class="form-control" type="number" placeholder="év" maxlength="4" min="1800" max="2017"></div>
							  <select class="form-control selectpicker" name="art-month[]" placeholder="month" title="month" data-live-search="true">
						  <input type="radio" id="radio2-1" name="__radio2" value="yes" class="box-toggler" data-toggle-target=".contents-2"> Igen
						  <input type="radio" id="radio2-2" name="__radio2" value="no"  class="box-toggler" data-toggle-target=".contents-2"> Nem
                              <input type="text" name="inv_name[]" class="form-control" title="Értékpapírban elhelyezett megtakarítás, vagy egyéb befektetés" placeholder="Értékpapírban elhelyezett megtakarítás, vagy egyéb befektetés">
                              <input type="text" name="inv_value[]" class="form-control" title="Névérték" placeholder="Névérték">
                              <select class="form-control" name="inv_curr[]" title="pénznem">
							  <input type="text" class="form-control hidden other-input " name="inv_curr_other[]">
                          <input type="text" name="sec_name[]" class="form-control" placeholder="Takarékbetétben elhelyezett megtakarítás"/>
                          <input type="text" name="sec_value[]" class="form-control" placeholder="Névérték"/>
                          <select class="form-control" name="sec_curr[]" title="pénznem">
						  <input type="text" class="form-control hidden other-input " name="sec_curr_other[]">
                          <input type="text" name="cash[]" class="form-control">
                          <select class="form-control" name="cash_curr[]" title="pénznem">
						  <input type="text" class="form-control hidden other-input " name="cash_curr_other[]">
							<select class="form-control" name="obligation_type[]" title="Számla- vagy pénzkövetelés">
							<input type="text" name="obligation_value[]" class="form-control">
							<select class="form-control" name="obligation_curr[]" title="pénznem">
							<input type="text" class="form-control hidden other-input " name="obligation_curr_other[]">
                          <input type="radio" id="radio3-1" name="__radio3" value="yes" class="box-toggler" data-toggle-target=".contents-3"> Igen
                          <input type="radio" id="radio3-2" name="__radio3" value="no"  class="box-toggler" data-toggle-target=".contents-3"> Nem
                            <select class="form-control" name="debt_type[]" title="Tartozás típusa">
                            <input type="text" name="debt_desc[]" class="form-control" placeholder="Megnevezés">
                            <input type="text" name="debt_value[]" class="form-control" placeholder="összeg">
                            <select class="form-control" name="debt_curr[]" title="pénznem">
							<input type="text" class="form-control hidden other-input " name="debt_curr_other[]">
                          <input type="radio" id="radio4-1" name="__radio4" value="yes" class="box-toggler" data-toggle-target=".contents-4"> Igen
                          <input type="radio" id="radio4-2" name="__radio4" value="no"  class="box-toggler" data-toggle-target=".contents-4"> Nem
                            <textarea name="comment" class="form-control" placeholder="Egyéb közlendők" rows="6"></textarea>
                          <input type="radio" id="radio5-1" name="__radio5" value="yes" class="box-toggler" data-toggle-target=".contents-5"> Igen
                          <input type="radio" id="radio5-2" name="__radio5" value="no"  class="box-toggler" data-toggle-target=".contents-5"> Nem
                            <input type="text" name="profession[]" class="form-control" placeholder="Foglalkozás">
                            <input type="text" name="employer[]" class="form-control" placeholder="Munkahelye/kifizető">
                            <select class="form-control" name="active[]" title="Szünetelteti?">
                          <div class="col-md-3"><input type="text" name="income[]" class="form-control" placeholder="Jövedelme"></div>
                            <select class="form-control" name="income_curr[]" title="pénznem">
							<input type="text" class="form-control hidden other-input " name="income_curr_other[]">
                          <div class="col-md-3"><input type="text" name="regularity[]" class="form-control" placeholder="gyakoriság"></div>
                          <input type="radio" id="radio6-1" name="__radio6" value="yes" class="box-toggler" data-toggle-target=".contents-6"> Igen
                          <input type="radio" id="radio6-2" name="__radio6" value="no"  class="box-toggler" data-toggle-target=".contents-6"> Nem
                            <input class="form-control" name="co_name[]" placeholder="Gazdasági társaság neve">
                            <input class="form-control" name="co_location[]" placeholder="Székhelye">
                            <select class="form-control" name="co_type[]" title="Formája">
							<input type="text" class="form-control hidden other-input " name="co_type_other[]">
                            <select class="form-control" name="int_beginning[]" title="Érdekeltség formája keletkezéskor">
							<input type="text" class="form-control hidden other-input " name="int_beginning_other[]">
                            <select class="form-control" name="int_now[]" title="Érdekeltség formája jelenleg">
							<input type="text" class="form-control hidden other-input " name="int_now_other[]">
                                <input class="form-control" name="ownership_ratio_beg1[]" type="text">
                                <input class="form-control" type="text" name="ownership_ratio_beg2[]">
                                  <input type="text" class="form-control" name="ownership_ratio_beg_percent[]" placeholder="százalék..." aria-describedby="percent-addon">
                                <input class="form-control" name="ownership_ratio_now1[]" type="text">
                                <input class="form-control" type="text" name="ownership_ratio_now2[]">
                                  <input type="text" class="form-control" name="ownership_ratio_now_percent[]" placeholder="százalék..." aria-describedby="percent-addon">
                              <input type="text" class="form-control" name="profitshare[]" placeholder="%..." aria-describedby="percent-addon">
                            <select class="form-control" name="position[]" title="Tisztség">
							<input type="text" class="form-control hidden other-input " name="position_other[]">
                          <input type="radio" id="radio7-1" name="__radio7" value="yes" class="box-toggler" data-toggle-target=".contents-7"> Igen
                          <input type="radio" id="radio7-2" name="__radio7" value="no"  class="box-toggler" data-toggle-target=".contents-7"> Nem
                            <input type="text" name="benefit_date[]" class="form-control" placeholder="Juttatás ideje">
							<input type="text" class="form-control" name="benefit_name[]" title="Juttatás megnevezése">
                            <input type="text" name="benefit_value[]" class="form-control" placeholder="értéke">
                            <select class="form-control" name="benefit_curr[]" title="pénznem">
                            <input type="text" name="present_date[]" class="form-control" placeholder="Ajándék ideje">
                            <input class="form-control" name="present_name[]" title="Ajándék megnevezése" placeholder="Ajándék megnevezése"/>
                            <input type="text" name="present_value[]" class="form-control" placeholder="Ajándék értéke">
                            <select class="form-control" name="present_currency[]" title="pénznem">
                            <input type="text" name="subs_reci[]" class="form-control" placeholder="Támogatás jogosultja">
                            <input type="text" name="subs_legal[]" class="form-control" placeholder="Megszerzés jogcíme">
                            <input type="text" name="subs_date[]" class="form-control" placeholder="Időpontja">
                            <input type="text" name="subs_provider[]" class="form-control" placeholder="Támogatást nyújtó">
                            <input type="text" name="subs_purpose[]" class="form-control" placeholder="Célja">
                            <input type="text" name="subs_value[]" class="form-control" placeholder="Értéke">
                            <select class="form-control" name="subs_curr[]" title="pénznem">
							<input type="text" class="form-control hidden other-input " name="subs_curr_other[]">
            <p> Instantly verify this document: <input type="checkbox" name="staff_force_verification"><br/>

