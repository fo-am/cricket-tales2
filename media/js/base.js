

var pop = false;
var current_user_id = 0;
var current_movie_id = 0;
var current_cricket_id = 0;
var timeline_fudge = 0.96;
var state = "none";
var csrftoken = "none";
var current_movie = 0;

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
    training_pause: "Click the pause button if you need time to think, and the play button when you’re ready to start again",
    training_pause: "Click the pause button if you need time to think, and the play button when you’re ready to start again",
    training_restart: "Click the restart button if you make a mistake and want to start the video again",
    training_congrats: "Well done!",
    training_finished: "Your training is complete.",

    watching_burrow_start: "Please click on the burrow first.",
    watching_cricket_start: "Now click on the cricket if it's visible, or click: ",
    watching_video: "Video playing...",
    watching_cricket_end: "Click on the cricket one more time, or click: ",    
    watching_no_cricket: "No cricket",
    watching_finished: "Thank you for your help! Loading video ",
}

function percentage(x, y) {
    var container_w = $('#ourvideo').width();
    var container_h = $('#ourvideo').height();    
    var percent_x = (x / container_w) * 100;
    var percent_y = (y / container_h) * 100;
    return {'x' : percent_x, 'y' : percent_y};
}

function mouse_pos(e, context) {
    var parentOffset = $('#ourvideo').parent().offset();
    return percentage(e.pageX - parentOffset.left, e.pageY - parentOffset.top);
}

function change_video(basename) {
    pop.pause();
    $('video').attr('poster','/media/movies/'+basename+'.jpg');
    $($('video').children()[0]).attr('src','/media/movies/'+basename+'.mp4');
    $($('video').children()[0]).attr('src','/media/movies/'+basename+'.ogv');
    pop.load();
    pop.play();
}

function play_state_toggle() {
    if (!pop.paused()) {
        pause_movie();
    } else {
        play_movie();
    }
}

function pause_movie() {
    if (!pop.paused()) {
        pop.pause();
        $('.toggle-button').css({
            "background": "url(/media/images/movie_buttons/play.png)",
            "background-size": "100% 100%"
        });
    }
}

function play_movie() {
    if (pop.paused()) {
        pop.play();
        $('.toggle-button').css({
            "background": "url(/media/images/movie_buttons/pause.png)",
            "background-size": "100% 100%"
        });
    }
}

/////////////////////////////////////////////////////////////////

function update_training() {
    switch(state) {
    case "training_singing":
        $('#popup-text').html(translated_text["training_singing"]);
        break;	
    case "training_sing_click":
        $('#popup-text').html(translated_text["training_congrats"]);
	change_video('tutorial/eating');
	setTimeout(function() { state="training_eating"; update_training(); }, 1000);
        break;	

    case "training_eating":
        $('#popup-text').html(translated_text["training_eating"]);
        break;	
    case "training_eating_click":
        $('#popup-text').html(translated_text["training_congrats"]);
	change_video('tutorial/in');
	setTimeout(function() { state="training_in"; update_training(); }, 1000);
        break;	

    case "training_in":
        $('#popup-text').html(translated_text["training_in"]);
        break;	
    case "training_in_click":
        $('#popup-text').html(translated_text["training_congrats"]);
	change_video('tutorial/in');
	setTimeout(function() { state="training_mid"; update_training(); }, 1000);
        break;	

    case "training_mid":
        $('#popup-text').html(translated_text["training_mid"]);
        break;	
    case "training_mid_click":
        $('#popup-text').html(translated_text["training_congrats"]);
	change_video('tutorial/out');
	setTimeout(function() { state="training_out"; update_training(); }, 1000);
        break;	

    case "training_out":
        $('#popup-text').html(translated_text["training_out"]);
        break;	
    case "training_out_click":
        $('#popup-text').html(translated_text["training_congrats"]);
	change_video('tutorial/sun');
	setTimeout(function() { state="training_sun"; update_training(); }, 1000);
        break;	

    case "training_sun":
        $('#popup-text').html(translated_text["training_sun"]);
        break;	
    case "training_sun_click":
        $('#popup-text').html(translated_text["training_congrats"]);
	change_video('tutorial/shade');
	setTimeout(function() { state="training_shade"; update_training(); }, 1000);
        break;	

    case "training_shade":
        $('#popup-text').html(translated_text["training_shade"]);
        break;	
    case "training_shade_click":
        $('#popup-text').html(translated_text["training_congrats"]);
	change_video('tutorial/night');
	setTimeout(function() { state="training_night"; update_training(); }, 1000);
        break;	

    case "training_night":
        $('#popup-text').html(translated_text["training_night"]);
        break;	
    case "training_night_click":
        $('#popup-text').html(translated_text["training_congrats"]);
	setTimeout(function() { state="training_pause"; update_training(); }, 1000);
        break;	

    case "training_pause":
        $('#popup-text').html(translated_text["training_pause"]);
	setTimeout(function() { state="training_restart"; update_training(); }, 4000);
        break;	

    case "training_restart":
        $('#popup-text').html(translated_text["training_restart"]);
	setTimeout(function() { state="training_finished"; update_training(); }, 4000);
        break;	

    case "training_finished":
        $('#popup-text').html(translated_text["training_finished"]);
	setTimeout(function() { window.location.href='/choose/'; }, 2000);
        break;	

    }
}

function training_click(button) {
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
    case "training_shade":
	if (button==="shade") { state = "training_shade_click"; update_training(); }
	break;
    case "training_night":
	if (button==="night") { state = "training_night_click"; update_training(); }
	break;
    }
}

function training_video_setup() {
    document.addEventListener("DOMContentLoaded", function () {
	pop = Popcorn("#ourvideo");
	state = "training_singing";

	// loop
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

        update_training();
	pop.play();
    });
}

/////////////////////////////////////////////////////

function update_watching() {
    switch(state) {
    case "watching_burrow_start":
        $('#popup-text').html(translated_text[state]);
	pop.currentTime(0);
	pop.pause();
	$("#popup").show();
        break;	
    case "watching_cricket_start":
        $('#popup-text').html(translated_text[state]+"<button class='micro' onclick='no_cricket_click();'>"+translated_text["watching_no_cricket"]+"</button>");
        break;	
    case "watching_video":
        $('#popup-text').html(translated_text[state]);
	pop.play();
	setTimeout(function() { $("#popup").hide(); }, 2000);
        break;	
    case "watching_cricket_end":
        $('#popup-text').html(translated_text[state]+"<button class='micro' onclick='no_cricket_click();'>"+translated_text["watching_no_cricket"]+"</button>");
	$("#popup").show();
        break;	
    case "watching_finished":
        $('#popup-text').html(translated_text[state]+" "+(current_movie+2)+"/5");
	$("#popup").show();
	setTimeout(function() {
	    current_movie+=1; 
	    if (current_movie>4) {
		// finished finished...
		window.location.href='/keyboard/'
	    }
	    change_video(movies[current_movie].path+"/"+movies[current_movie].name)
	    current_movie_id = movies[current_movie].movie_id;
	    state = "watching_burrow_start";
	    $('#video-num').html((current_movie+1)+"/5");
	    update_watching();	    
	    pop.pause(); 
	}, 2000);
        break;	
    }
}

function restart_click() {
    add_event("video_restart", 0, 0, null);
    state = "watching_burrow_start";
    update_watching();    
}

function no_cricket_click() {
    switch(state) {
    case "watching_cricket_start":
	add_event("no_cricket_start", 0, 0, null);
	state = "watching_video";
	update_watching();
	break;
    case "watching_cricket_end":
	add_event("no_cricket_end", 0, 0, null);
	state = "watching_finished";
	update_watching();
	break;
    }
}

function watching_click(button,e) {
    switch(state) {
    case "watching_burrow_start":
	if (button=="video") {
	    var pos = mouse_pos(e, this);
            add_event("burrow_start", pos['x'], pos['y'], null);
	    state = "watching_cricket_start";
	    update_watching();
	}
	break;
    case "watching_cricket_start":
	if (button=="video") {
	    var pos = mouse_pos(e, this);
            add_event("cricket_start", pos['x'], pos['y'], null);
	    state = "watching_video";
	    update_watching();
	}
	break;
    case "watching_video": // normal situation, just pass through
	add_event(button, 0, 0, null);
	break;
    case "watching_cricket_end":
	if (button=="video") {
	    var pos = mouse_pos(e, this);
            add_event("cricket_end", pos['x'], pos['y'], null);
	    state = "watching_finished";
	    update_watching();
	}
	break;
    }
}

var movies = [];
function register_movie(movie_id,name,path) {
    movies.push({ movie_id: movie_id, name: name, path: path });
}

function video_setup(user_id, csrf) {
    csrftoken=csrf;
    current_user_id = user_id;
    current_movie_id = movies[0].movie_id;
    current_movie = 0;

    document.addEventListener("DOMContentLoaded", function () {
	pop = Popcorn("#ourvideo");
	state = "watching_burrow_start";

	// loop
        pop.on("ended", function() {
	    state = "watching_cricket_end";
	    update_watching();
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

	$("#ourvideo").click(function(e) {
	    // click on burrow/cricket
	    // pass through same thing as buttons
            watching_click("video",e);
	});
	// start paused
	pop.pause();
	update_watching()
    });    
}

// sends the event to the server and renders it
function add_event(event_type, xpos, ypos, other) {
    // only works if we have a video running of course...
    if (pop!=false) {
        t = pop.currentTime();
        // save to django ->
        $.post("/event/", {
            movie: current_movie_id,
            event_type: event_type,
            user: 1,
            start_time: t,
            end_time: t+1,
            x_pos : xpos,
            y_pos: ypos,
            other: other,
	    csrfmiddlewaretoken: csrftoken
        });
    }

}
