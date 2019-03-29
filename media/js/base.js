

var pop = false;
var current_user_id = 0;
var current_movie_id = 0;
var current_cricket_id = 0;
var needs_keyboard = 0;
var timeline_fudge = 1.0;
var state = "none";
var csrftoken = "none";
var current_movie = 0;
var weather_recorded = false;

// in order to sort out translations...
var translated_text = {}

function iphone() {
  var idevices = [
    'iPhone',
    'iPod'
  ];

  if (!!navigator.platform) {
    while (idevices.length) {
      if (navigator.platform === idevices.pop()){ return true; }
    }
  }

  return false;
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
//    $('video').attr('poster','/media/movies/'+basename+'.jpg');
    $($('video').children()[0]).attr('src','/media/movies/'+basename+'.mp4');
    $($('video').children()[1]).attr('src','/media/movies/'+basename+'.ogv');

    pop.load();
    
    pop.on("canplay", function() {
	switch (state) {
	case "watching_wait_load":
	    state="watching_burrow_start";
	    update_watching();
	    break;

	case "training_loading_singing":
	    state="training_singing";
	    pop.play();
	    update_training();
	    break;
	case "training_loading_eating":
	    state="training_eating";
	    pop.play();
	    update_training();
	    break;
	case "training_loading_in":
	    state="training_in";
	    pop.play();
	    update_training();
	    break;
	case "training_loading_out":
	    state="training_out";
	    pop.play();
	    update_training();
	    break;
	case "training_loading_mid":
	    state="training_mid";
	    pop.play();
	    update_training();
	    break;
	case "training_loading_sun":
	    state="training_sun";
	    pop.play();
	    update_training();
	    break;
	case "training_loading_shade":
	    state="training_shade";
	    pop.play();
	    update_training();
	    break;
	case "training_loading_night":
	    state="training_night";
	    pop.play();
	    update_training();
	    break;
	}
	pop.off("canplay");
    });
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

function update_helper(new_state,video) {
    state=new_state; 
    update_training();
    if (video!="undefined") {
	change_video(video);
    }
}

function update_button(new_state,video) {
    return "<button class='micro' onclick='update_helper(\""+new_state+"\",\""+video+"\");'>"+
	translated_text["next"]+
	"</button>";
}

function highlight_button(button) {
    $("#"+button).addClass("highlight");
}

function unhighlight_button(button) {
    $("#"+button).removeClass("highlight");
}

function update_training() {
    switch(state) {
    case "training_start":
        $('#popup-text').html(translated_text["training_start"]+
			      update_button("training_start2"));
        break;	
    case "training_start2":
        $('#popup-text').html(translated_text["training_start2"]+
			      update_button("training_start3"));
        break;	
    case "training_start3":
        $('#popup-text').html(translated_text["training_start3"]+
			      update_button("training_loading_singing","tutorial/singing"));
        break;	
    case "training_singing":
	play_movie();
	highlight_button("singing");
        $('#popup-text').html(translated_text["training_singing"]);
        break;	
    case "training_sing_click":
        $('#popup-text').html(translated_text["training_congrats"]);
	setTimeout(function() { state="training_loading_eating"; update_training(); change_video('tutorial/eating');}, 1000);
        break;	

    case "training_eating":
        $('#popup-text').html(translated_text["training_eating"]);
	highlight_button("eating");
        break;	
    case "training_eating_click":
        $('#popup-text').html(translated_text["training_eating2"]+
			      update_button("training_loading_in","tutorial/in"));
        break;	

    case "training_in":
        $('#popup-text').html(translated_text["training_in"]);
	highlight_button("in");
        break;	
    case "training_in_click":
        $('#popup-text').html(translated_text["training_congrats"]);
	setTimeout(function() { state="training_loading_mid"; update_training(); change_video('tutorial/mid');}, 1000);
        break;	

    case "training_mid":
        $('#popup-text').html(translated_text["training_mid"]);
	highlight_button("mid");
        break;	
    case "training_mid_click":
        $('#popup-text').html(translated_text["training_congrats"]);
	setTimeout(function() { state="training_loading_out"; update_training(); change_video('tutorial/out');}, 1000);
        break;	

    case "training_out":
        $('#popup-text').html(translated_text["training_out"]);
	highlight_button("out");
        break;	
    case "training_out_click":
        $('#popup-text').html(translated_text["training_out2"]+
			      update_button("training_loading_sun","tutorial/sun"));
        break;	

    case "training_sun":
        $('#popup-text').html(translated_text["training_sun"]);
	highlight_button("sun");
        break;	
    case "training_sun_click":
        $('#popup-text').html(translated_text["training_congrats"]);
	setTimeout(function() { state="training_loading_shade"; update_training(); change_video('tutorial/shade'); }, 1000);
        break;	

    case "training_shade":
        $('#popup-text').html(translated_text["training_shade"]);
	highlight_button("shade");
        break;	
    case "training_shade_click":
        $('#popup-text').html(translated_text["training_congrats"]);
	setTimeout(function() { state="training_loading_night"; update_training(); change_video('tutorial/night'); }, 1000);
        break;	

    case "training_night":
        $('#popup-text').html(translated_text["training_night"]);
	highlight_button("night");
        break;	
    case "training_night_click":
        $('#popup-text').html(translated_text["training_night2"]+
			      update_button("training_overview"));
        break;	

    case "training_overview":
        $('#popup-text').html(translated_text["training_overview"]+
			      update_button("training_pause"));
        break;	
	
    case "training_pause":
	// move popup out of the way of the pause button
	$('.video-popup').css("top","33vw");
        $('#popup-text').html(translated_text["training_pause"]+
			      update_button("training_restart"));
        break;	

    case "training_restart":
        $('#popup-text').html(translated_text["training_restart"]+
			      update_button("training_finished"));
        break;	

    case "training_finished":
        $('#popup-text').html(translated_text["training_finished"]);
	setTimeout(function() { window.location.href='/choose/'; }, 2000);
        break;	

    default:    
	// for all the loading messages
        $('#popup-text').html(translated_text[state]);
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

    do_radio_buttons(button);
}

function training_video_setup() {
    document.addEventListener("DOMContentLoaded", function () {
	pop = Popcorn("#ourvideo");
	state = "training_start";

	// loop
        pop.on("ended", function() {
            pop.currentTime(0);
	    pop.play();
	});

        // scrubbing
        $("#time").draggable({
	    axis:"x",
	    containment:"#timeline",
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
	pop.pause();
    });
}

/////////////////////////////////////////////////////

function update_watching() {
    switch(state) {
    case "watching_wait_load":
        $('#popup-text').html(translated_text[state]);
	break;
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
    case "watching_weather_prompt":
	$('#popup-text').html(translated_text[state]);
	$("#popup").show();
	break;
    case "watching_cricket_end":
        $('#popup-text').html(translated_text[state]+"<button class='micro' onclick='no_cricket_click();'>"+translated_text["watching_no_cricket"]+"</button>");
	$("#popup").show();
        break;	
    case "watching_finished":
	if (current_movie<4) {
            $('#popup-text').html(translated_text[state]+" "+(current_movie+2)+"/5");
	}
	$("#popup").show();
	setTimeout(function() {
	    current_movie+=1; 
	    if (current_movie>4) {
		// finished finished...
		if (needs_keyboard) {
		    window.location.href='/keyboard/'+current_cricket_id;
		} else {
		    window.location.href='/personality/'+current_cricket_id;
		}
	    }
	    change_video(movies[current_movie].path+"/"+movies[current_movie].name)
	    current_movie_id = movies[current_movie].movie_id;
	    state = "watching_wait_load";
	    clear_radio_buttons();
	    weather_recorded=false;
	    $('#video-num').html((current_movie+1)+"/5");
	    update_watching();	    
	}, 2000);
        break;	
    }
}

function restart_click() {
    add_event("video_restart", 0, 0, null);
    // reset everything...
    clear_radio_buttons();
    $('.toggle-button').css({
        "background": "url(/media/images/movie_buttons/pause.png)",
        "background-size": "100% 100%"
    });
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
	if (button!="video") {
	    add_event(button, 0, 0, null);
	    do_radio_buttons(button);
	}
	// remember the fact we've recorded the weather
	if (button=="sun" || button=="shade" || button=="night") {
	    weather_recorded=true;
	}
	break;
    case "watching_weather_prompt":
	// only interested in the weather!
	if (button=="sun" || button=="shade" || button=="night") {
	    add_event(button, 0, 0, null);
	    do_radio_buttons(button);
	    state="watching_cricket_end";
	    update_watching();
	}
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

function clear_radio_buttons() {
    $("#sun").css("background-color","");
    $("#shade").css("background-color","");
    $("#night").css("background-color","");
    $("#in").css("background-color","");
    $("#mid").css("background-color","");
    $("#out").css("background-color","");
    $("#eating").css("background-color","");
    $("#singing").css("background-color","");
}

function do_radio_buttons(button) {
    unhighlight_button(button);
    if (["sun","shade","night"].indexOf(button)>=0) {
	$("#sun").css("background-color","");
	$("#shade").css("background-color","");
	$("#night").css("background-color","");
    }
    if (["in","mid","out"].indexOf(button)>=0) {
	$("#in").css("background-color","");
	$("#mid").css("background-color","");
	$("#out").css("background-color","");
    }
    // turn off eating or singing button after a few seconds
    if (["eating","singing"].indexOf(button)>=0) {
	setTimeout(function() {$("#"+button).css("background-color",""); }, 5000);
    }
    $("#"+button).css("background-color","#ededf0");
}

var movies = [];

function register_movie(movie_id,name,path) {
    movies.push({ movie_id: movie_id, name: name, path: path });
}

function register_csrf(token) {
    csrftoken=token;
}

function video_setup(user_id, cricket_id, done_keyboard) {
    current_user_id = user_id;
    current_cricket_id = cricket_id;
    current_movie_id = movies[0].movie_id;
    current_movie = 0;
    needs_keyboard = 0;
    if (done_keyboard=="False") needs_keyboard=1;

    document.addEventListener("DOMContentLoaded", function () {
	pop = Popcorn("#ourvideo");
	state = "watching_wait_load";
	change_video(movies[current_movie].path+"/"+movies[current_movie].name);

        pop.on("ended", function() {
	    if (weather_recorded) {
		state = "watching_cricket_end";
	    } else {
		state = "watching_weather_prompt";
	    }	    
	    update_watching();
	    pop.pause();
	});

        // scrubbing
        $("#time").draggable({
	    axis:"x",
	    containment:"#timeline",
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

var kb_pos=0;
var kb_txt="???";

String.prototype.replaceAt=function(index, replacement) {
    return this.substr(0, index) + replacement+ this.substr(index + replacement.length);
}

// keyboard stuff
function kb(pressed) {
    if (kb_pos<3) {
	kb_txt=kb_txt.replaceAt(kb_pos++,pressed);
	$("#kb-text").html(kb_txt);
    }
}

function kb_delete() {
    if (kb_pos>0) {
	kb_pos--;
	kb_txt=kb_txt.replaceAt(kb_pos,"?");
	$("#kb-text").html(kb_txt);
    }
}

function kb_send(cricket_id) {
    $.post("/player_name/", {
        name: kb_txt,
	csrfmiddlewaretoken: csrftoken
    }, function(result) {
	window.location.href='/personality/'+cricket_id;
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
            user: current_user_id,
            video_time: t,
            x_pos : xpos,
            y_pos: ypos,
            other: other,
	    csrfmiddlewaretoken: csrftoken
        });
    }

}

function runtimeout(exhib) {
    if (exhib) {
	document.addEventListener("DOMContentLoaded", function () {
	    var time = new Date().getTime();
	    $(document.body).bind("mousemove keypress", function(e) {
		time = new Date().getTime();
	    });
	    
	    function refresh() {
		if(new Date().getTime() - time >= 60000) {
		    if (exhib) window.location="/exhib_reset_lang";
		    else window.location="/";
		} else { 
		    setTimeout(refresh, 10000);
		}
	    }
	    
	    setTimeout(refresh, 10000);
	});
    }
}
