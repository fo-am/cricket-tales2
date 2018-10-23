var pop = false;
var events = [];

// in order to sort out translations...
var translated_text = { 
    training_singing: "This cricket is singing, notice it's wings fluttering - click on the right button.",
    training_eating: "The cricket is eating – click the right button",			
    training_in: "The cricket is completely inside its burrow – click the right button",
    training_mid: "The cricket is midway in/out of its burrow – click the right button",
    training_out: "The cricket is completely outside its burrow – click the right button",
    training_sun: "It is sunny – the image is full colour and bright – click the right button",
    training_shade: "It is shady – the image is in colour but it’s a bit dark – click the right button",
    training_night: "It is night time – the infra red cameras are on so the image is black and white – click the right button",
    training_congrats: "Well done!",
    training_finished: "Your training is complete.",
}

function percentage(x, y) {
    var container_w = $('#ourvideo').width();
    var container_h = $('#ourvideo').height();
    
    var percent_x = (x / container_w) * 100;
    var percent_y = (y / container_h) * 100;

    return {'x' : percent_x, 'y' : percent_y};
}

function mouse_pos(e, context) {
    var parentOffset = $(context).parent().offset();
    return percentage(e.pageX - parentOffset.left, e.pageY - parentOffset.top);
}

function change_video(basename) {
    pop.pause();
    $($('video').children()[0]).attr('src','/media/movies/'+basename+'.mp4');
    $($('video').children()[0]).attr('src','/media/movies/'+basename+'.ogv');
    pop.load();
    pop.play();
}

function update_training() {
    switch(state) {
    case "training_singing":
        $('.video-popup').html(translated_text["training_singing"]);
        break;	
    case "training_sing_click":
        $('.video-popup').html(translated_text["training_congrats"]);
	change_video('tutorial/eating');
	setTimeout(function() { state="training_eating"; update_training(); }, 2000);
        break;	

    case "training_eating":
        $('.video-popup').html(translated_text["training_eating"]);
        break;	
    case "training_eating_click":
        $('.video-popup').html(translated_text["training_congrats"]);
	change_video('tutorial/in');
	setTimeout(function() { state="training_in"; update_training(); }, 2000);
        break;	

    case "training_in":
        $('.video-popup').html(translated_text["training_in"]);
        break;	
    case "training_in_click":
        $('.video-popup').html(translated_text["training_congrats"]);
	change_video('tutorial/in');
	setTimeout(function() { state="training_mid"; update_training(); }, 2000);
        break;	

    case "training_mid":
        $('.video-popup').html(translated_text["training_mid"]);
        break;	
    case "training_mid_click":
        $('.video-popup').html(translated_text["training_congrats"]);
	change_video('tutorial/out');
	setTimeout(function() { state="training_out"; update_training(); }, 2000);
        break;	

    case "training_out":
        $('.video-popup').html(translated_text["training_out"]);
        break;	
    case "training_out_click":
        $('.video-popup').html(translated_text["training_congrats"]);
	change_video('tutorial/sun');
	setTimeout(function() { state="training_sun"; update_training(); }, 2000);
        break;	

    case "training_sun":
        $('.video-popup').html(translated_text["training_sun"]);
        break;	
    case "training_sun_click":
        $('.video-popup').html(translated_text["training_congrats"]);
	change_video('tutorial/night');
	setTimeout(function() { state="training_night"; update_training(); }, 2000);
        break;	

    case "training_finished":
        $('.video-popup').html(translated_text["training_finished"]);
        break;	

    }
}

function training_click(button) {
    console.log(button);
    switch(state) {
	case "training_singing":
	if (button==="singing") { state = "training_sing_click"; update_training(); }
	break;
	case "training_eating":
	if (button==="eating") { state = "training_eating_click"; update_training(); }
	break;
	case "training_in":
	if (button==="in") { state = "training_in_click"; update_training(); }
	break;
	case "training_mid":
	if (button==="mid") { state = "training_mid_click"; update_training(); }
	break;
	case "training_out":
	if (button==="out") { state = "training_out_click"; update_training(); }
	break;
	case "training_sun":
	if (button==="sun") { state = "training_sun_click"; update_training(); }
	break;
	case "training_night":
	if (button==="night") { state = "training_finished"; update_training(); }
	break;
    }
}


var state = "training_singing";

function training_video_setup() {
    document.addEventListener("DOMContentLoaded", function () {
	pop = Popcorn("#ourvideo");

        pop.code({
            start: 0,
            end: 0.01,
            onStart: function() {
                update_training();
            }});

	// pop.footnote({
        //     start: 2,
        //     end: 5,
        //     target: "footnote",
        //     text: "Pop!"
        // });

        pop.on("ended", function() {
            pop.currentTime(0);
	    pop.play();
	});


        // scrubbing
        $("#time").draggable({
	    axis:"x",
	    drag: function( event, ui ) {
                var pos = pop.duration() * parseFloat($('#time').css('left')) /
		    parseFloat($('#time').parent().css('width'));
                pop.currentTime(pos);
	    }
        });


        // click on timeline
        $("#timeline").click(function(e) {
	    var offset = $(this).offset();
	    var x = e.clientX - offset.left;
	    var pos = pop.duration() * x / parseFloat($('#timeline').css('width'));
	    pop.currentTime(pos);
        });

        pop.on("timeupdate", function() {
	    var percentage = Math.floor((100 / pop.duration()) *
                                        pop.currentTime());
	    $("#time").css({left: percentage*timeline_fudge+"%"});

        });

	pop.play();


    });
    
}



/////////////////////////////////////////////////////

function video_setup(user_id,movie_id) {
    document.addEventListener("DOMContentLoaded", function () {
	pop = Popcorn("#ourvideo");

        pop.code({
            start: 0,
            end: 0.01,
            onStart: function() {
                //update_training();
            }});

        // scrubbing
        $("#time").draggable({
	    axis:"x",
	    drag: function( event, ui ) {
                var pos = pop.duration() * parseFloat($('#time').css('left')) /
		    parseFloat($('#time').parent().css('width'));
                pop.currentTime(pos);
	    }
        });

        // click on timeline
        $("#timeline").click(function(e) {
	    var offset = $(this).offset();
	    var x = e.clientX - offset.left;
	    var pos = pop.duration() * x / parseFloat($('#timeline').css('width'));
	    pop.currentTime(pos);
        });

        pop.on("timeupdate", function() {
	    var percentage = Math.floor((100 / pop.duration()) *
                                        pop.currentTime());
	    $("#time").css({left: percentage*timeline_fudge+"%"});

        });

	pop.play();
    });
    
}
 
function old_video_setup(cricket_start_id, burrow_start_id, cricket_id_id, cricket_end_id, something_else_id, movie_id, user_id) {
    // Create a popcorn instance by calling Popcorn("#id-of-my-video")
    document.addEventListener("DOMContentLoaded", function () {
        state = "wait-cricket";
        //build_id_keyboard(cricket_id_id,something_else_id, movie_id,user_id);
        pop = Popcorn("#ourvideo");
        play_state = "";
        popvid = document.getElementById("ourvideo");
        popvid.addEventListener( "playing", function( e ) {
            play_state = true;
        }, false );
        popvid.addEventListener( "pause", function( e ) {
            play_state = false;
        }, false );
	
        pop.code({
            start: 0,
            end: 0.01,
            onStart: function() {
                $('.top_layer').css({'z-index' : '-1', 'display' : 'none'});

                //update_infotext();
		
                $("#ourvideo").click(function(e) {
                    var cricketStartPercent = mouse_pos(e, this);
                    add_event(cricket_start_id,movie_id,user_id, cricketStartPercent['x'], cricketStartPercent['y'], null);
                    state = "wait-burrow";
                    $(this).off('click');
                    burrow_event(burrow_start_id,movie_id,user_id);
                });


                $('#no_cricket').click(function() {
                    add_event(cricket_start_id,movie_id,user_id, 0, 0, 'No Cricket');
                    state = "wait-burrow";
                    $("#ourvideo").off('click');
                    burrow_event(burrow_start_id,movie_id,user_id);
                });

            }

        });

        pop.on("ended", function() {

            if (state === "movie-playing") {
                state = "wait-cricket-end";
                update_infotext();

                $('#ourvideo').click(function(e) {
                   $('.top_layer').css({'z-index' : '1', 'display' : 'inline-block'});
                    pop.currentTime(pop.duration());
                    state = "movie-end";
                    update_infotext();
                    pop.pause();
                    var pos = mouse_pos(e, this);
                    add_event(cricket_end_id,movie_id,user_id, pos['x'], pos['y'], null);
                    $("#movie_end").css("visibility", "visible");
                    $(this).off('click');
                });

                $('#no_cricket_end').click(function() {
                    add_event(cricket_end_id,movie_id,user_id, 0, 0, 'No Cricket');
                    $('.top_layer').css({'z-index' : '1', 'display' : 'inline-block'});
                    update_infotext();
                    $("#movie_end").css("visibility", "visible");
                });
            }

        });

        // scrubbing
        $("#time").draggable({
            axis:"x",
            drag: function( event, ui ) {
                var pos = pop.duration() * parseFloat($('#time').css('left')) /
                    parseFloat($('#time').parent().css('width'));
                pop.currentTime(pos);
            }
        });


        // click on timeline
        $("#timeline").click(function(e) {
            var offset = $(this).offset();
            var x = e.clientX - offset.left;
            var pos = pop.duration() * x / parseFloat($('#timeline').css('width'));
            pop.currentTime(pos);
        });

        pop.on("timeupdate", function() {
            var percentage = Math.floor((100 / pop.duration()) *
                                        pop.currentTime());
            $("#time").css({left: percentage*timeline_fudge+"%"});

        });


        pop.on("loadeddata", function () {
            // go through the events we collected earlier...
            events.forEach(function(e) {
                //console.log("rendering event...");
                inner_render_event(e[0],e[1]);
            });
        });

    },false);
};

var timeline_fudge = 0.96;

function play_state_toggle() {
    if (play_state === true) {
        pause_movie();
    } else {
        play_movie();
    }
}

function pause_movie() {
    if (state === 'movie-playing') {
        pop.pause();
        $('.toggle-button').css({
            "background": "url(/media/images/movie_buttons/play.png)",
            "background-size": "100% 100%"
        });
    }
}

function play_movie() {
    if (state === 'movie-playing') {
        pop.play();
        $('.toggle-button').css({
            "background": "url(/media/images/movie_buttons/pause.png)",
            "background-size": "100% 100%"
        });
    }
}

// actually render the event
function inner_render_my_event(start_time) {
    // convert time into %
    var left = (start_time/pop.duration())*100;
    var cricket_image = Math.floor(Math.random() * 10) + 1;
    $("#timeline").append(
        '<div class="callback event small_circle" style="left:'+left*timeline_fudge+'%; margin-top: -1.8em"></div>');
    $('.callback').fadeOut(5000);
}

// sends the event to the server and renders it
function add_event(event_type_id, movie_id,user_id, xpos, ypos, other) {
    //console.log([event_type_id, movie_id,user_id, xpos, ypos, other]);
    // only works if we have a video running of course...
    if (pop!=false) {
        t = pop.currentTime();

        // todo: user_id now comes in as -1 if the player is anonymous
        // not sure what circumstances it can be None now

        // save to django ->
        if (user_id=="None") {
            $.post("/spit_event/", {
                movie: movie_id,
                type: event_type_id,
                user: "",
                start_time: t,
                end_time: t+1,
                x_pos : xpos,
                y_pos: ypos,
                other: other
            });
        } else {
            $.post("/spit_event/", {
                movie: movie_id,
                type: event_type_id,
                user: parseInt(user_id),
                start_time: t,
                end_time: t+1,
                x_pos : xpos,
                y_pos: ypos,
                other: other
            });
        }

        inner_render_my_event(t)
    }

}
