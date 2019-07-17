$( document ).ready(function() {
    var animation_end = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
    $(".btn76").click(function() {
        console.log('click');
        $(this).addClass('animated fadeOutUp faster');
        $(this).one(animation_end, function() {
            $(this).removeClass('animated fadeOutUp faster');
        });
    })
    
    var cover_header_class_ =  $('#cover-heading').attr("class")
    $('#cover-heading').one(animation_end, function() {
        $(this).removeClass();
    });

    function set_idea(idea) {
        var header = $('#cover-heading')
        header.text(idea);
        header.addClass(cover_header_class_);
        header.one(animation_end, function() {
            console.log('animation end')
            console.log(this)
            $(this).removeClass();
        });
    }
    
    var cur_idea_index = 0
    $('#skip').click(function() {
        cur_idea_index += 1
        if (cur_idea_index >= ideas.length) {
            return;
        }
        set_idea(ideas[cur_idea_index]); // ideas are firstly initialized in index.html 
    })
});