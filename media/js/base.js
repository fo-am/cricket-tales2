var pop = false;
var events = [];

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

function video_setup(cricket_start_id, burrow_start_id, cricket_id_id, cricket_end_id, something_else_id, movie_id, user_id) {
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
