$( document ).ready(function() {
    $(".btn76").click(function() {
        console.log('click');
        $(this).addClass('animated fadeOutUp faster');
        $(this).one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            console.log('endanimation');
            $(this).removeClass('animated fadeOutUp faster');
        });
    })
});