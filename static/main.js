$( document ).ready(function() {
    var animation_end = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
    $(".btn76").click(function() {
        $(this).addClass('animated fadeOutUp faster');
        $(this).one(animation_end, function() {
            $(this).removeClass('animated fadeOutUp faster');
        });
    })
    
    var cover_header_class_ =  $('#cover-heading').attr("class")
    $('#cover-heading').one(animation_end, function() {
        $(this).removeClass();
    });

    var num_of_ideas = 5;
    var cur = ideas.shift()

    function set_idea(idea) {
        var header = $('#cover-heading')
        header.text(idea);
        header.addClass(cover_header_class_);
        header.one(animation_end, function() {
            $(this).removeClass();
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
    
    $('#skip').click(show_next_idea)
});