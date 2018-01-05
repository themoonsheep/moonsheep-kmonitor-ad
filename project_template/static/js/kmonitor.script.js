/** functions **/

/** add lines for multiple values in data entry **/
function sectionRepeat(){
  var repeatBlock = [];
  $('button.repeater').each(function( i ){
    repeatBlock.push( $(this).prev().clone() );
  });

  $('button.repeater').click(function(e){
    e.preventDefault();

    var repeaterClone = $(this).prev().clone();
    /** reset inputs and selects **/
    repeaterClone.find('input').val('');
    repeaterClone.find('select').val('choose');
    repeaterClone.find('input[type="checkbox"]').attr('checked', false);
    repeaterClone.find('select + input[type="text"]').addClass('hidden').removeClass('show');

    if ($(this).hasClass('have-nested-repeats')) {
        // index nested multiline items
        nested = $(repeaterClone).find("*[name*='][]']");
        nested.each(function(input) {
            var g = $(this).attr('name').match(/([\w-_]+)\[(\d+)\]\[\]/);
            var incremented = g[1] + '[' + (parseInt(g[2])+1) + '][]';

            $(this).attr('name', incremented);
        });

        // TODO nice-to-have is that cloned nested multiline have just one position
        // even if in previous section user has added two or more
        // (hidden template out of form to be copied? or deleting uneccessary here based on some classes)
    }

    $(repeaterClone).insertAfter($(this).prev());

    /** bind recursively to newly generated elements **/
    $(repeaterClone).on('click', 'button.repeater', function(){ sectionRepeat(); });
    $(repeaterClone).on('change', 'select', function(){ otherInput(); });
  });
}

/** display input field to enter "other" value **/
function otherInput(){
  $('select').change(function(){
    if($(this).val() == 'egyeb' || $(this).val() == 'egyéb'){
      $(this).next('input[type="text"]').addClass('show').removeClass('hidden').focus();
    }
    else {
      $(this).next('input[type="text"]').addClass('hidden').removeClass('show');
    }
  });
}
/** main js script **/
$(document).ready(function(){

  console.log('started...');

  /** section repeat/add lines **/
  sectionRepeat();
  /** the "other" input field for selects **/
  otherInput();

  /** box toggling **/
  $('.box-toggler:radio').change(function(){
    if($(this).val() == 'yes'){
      $($(this).data('toggle-target')).removeClass('hidden').addClass('show');
      $($(this).data('toggle-target') + ' + button.hidden').removeClass('hidden').addClass('show');
    }
    else {
      $($(this).data('toggle-target')).addClass('hidden').removeClass('show');
      $($(this).data('toggle-target') + ' + button.repeater').addClass('hidden').removeClass('show');
    }
  });

});
