$( document ).ready(function() {
    var animation_end = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
    $(".btn76").click(function() {
        $(this).addClass('animated fadeOutUp faster');
        $(this).one(animation_end, function() {
            $(this).removeClass('animated fadeOutUp faster');
        });
    })
    
    var cover_header_classes_ =  $('#cover-heading').attr("class").split(' ')
    var cover_animated = cover_header_classes_.slice(cover_header_classes_.indexOf('animated')).join(' ');
    $('#cover-heading').one(animation_end, function() {
        $(this).removeClass(cover_animated);
    });

    var num_of_ideas = 5;
    var cur = ideas.shift()

    function set_idea(idea) {
        var header = $('#cover-heading')
        header.text(idea['text']);
        $('#idea_id').val(idea['id'])
        header.addClass(cover_animated);
        header.one(animation_end, function() {
            $(this).removeClass(cover_animated);
        });
    }
    
    var is_runned = false;
    function get_ideas() {
        if (is_runned) {
            console.log('Already runned.')
            setTimeout(function() {
                console.error('timeout error. running is allowed again');
                is_runned = false;
            }, 500);
            return
        }
        is_runned = true;
        $.post('/get_ideas').done(function(response) {
                console.log('Ideas has gotten!')
                var new_ideas = response['ideas'];
                ideas.push(...new_ideas)
                is_runned = false;
            }).fail(function() {
                console.error('Error while getting ideas from the server');
                is_runned = false
            });
    }
    
    function loading_loop() {
        console.log('Loading...')
        get_ideas()
        if (ideas.length < num_of_ideas) {
            setTimeout(loading_loop, 300)
        } else {
            $('#loading').hide()
            $('#cover-heading').show()
            show_next_idea()
        }
    }

    function loading_ideas() {
        $('#cover-heading').hide()
        $('#loading').show()
        setTimeout(loading_loop(), 1)
    }
    
    function show_next_idea() {
        if (ideas.length < num_of_ideas) {
            console.log('Getting new ideas...')
            get_ideas()
        }
        if (ideas.length === 0) {
            loading_ideas()
            return;
        }
        cur = ideas.shift()
        set_idea(cur); // ideas are firstly initialized in index.html 
    }
    
    function rate(field) {
        var idea_id = parseInt($('#idea_id').val());
        $.post('/rate', {'id': idea_id, 'field': field}).done(function(response) {
                console.log('Rate request status:', response['status']);
            }).fail(function() {
                console.error('Error during rating');
            });
    }
    
    $(".btn76").click(show_next_idea)
    $('#thumbs_up').click(function() {rate('likes')})
    $('#thumbs_down').click(function() {rate('dislikes')})
    $('#skip').click(function() {rate('skips')})
});