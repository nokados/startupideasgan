$( document ).ready(function() {
    console.log( "ready!" );

    $( ".entry" ).each(function( index ) {
      console.log( index + ": " + $( this ).text() );
    });
    
    $('.entry').on('click', function() {
      console.log('click')
      var entry = this;
      var post_id = $(this).find('h2').attr('id');
      $.ajax({
        type:'GET',
        url: '/delete' + '/' + post_id,
        context: entry,
        success:function(result) {
          if(result.status === 1) {
            $(this).remove();
            console.log(result);
          }
        }
      });
    });

});