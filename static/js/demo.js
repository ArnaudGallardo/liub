
$(document).ready(init);

function init() {
	var rotation = 180;
	$(".plane").rotate(rotation);
	/* ========== DRAWING THE PATH AND INITIATING THE PLUGIN ============= */
	$.fn.center();
	$.fn.scrollPath("getPath")
		// Move to 'start' element
		.moveTo(400, 50, {name: "start"})
		// Line to 'description' element
		.lineTo(400, 800, {
			callback: function() {
    			$(".plane").rotate(270,0);
			}, name: "description"})
		// Arc down and line to 'syntax'
		.arc(200, 1200, 400, -Math.PI/2, Math.PI/2, true, {rotate: Math.PI })
		.lineTo(600, 1600, {
			callback: function() {
				highlight($(".settings"));
			},
			name: "syntax"
		})
		// Continue line to 'scrollbar'
		.lineTo(1750, 1600, {
			callback: function() {
				highlight($(".sp-scroll-handle"));
			},
			name: "scrollbar"
		}).rotate(Math.PI/2, {
			callback: function() {
				$(".plane").rotate(270,0);
				$(".plane").toggleImg();
			}})
		// Arc up while rotating
		.arc(1800, 1000, 600, Math.PI/2, 0, true, {rotate: Math.PI/2 })
		// Line to 'rotations'
		.lineTo(2400, 750, {
			name: "rotations"
		})
		// Rotate in place
		.rotate(3*Math.PI/2, {
			name: "rotations-rotated"
		})
		// Continue upwards to 'source'
		.lineTo(2400, -700, {
			name: "source"
		})
		// Small arc downwards
		.arc(2250, -700, 150, 0, -Math.PI/2, true)

		//Line to 'follow'
		.lineTo(1350, -850, {
			name: "follow"
		})
		// Arc and rotate back to the beginning.
		.arc(1300, 50, 900, -Math.PI/2, -Math.PI, true, {rotate: Math.PI*2, name: "end"});

	// We're done with the path, let's initate the plugin on our wrapper element
	$(".wrapper").scrollPath({drawPath: true, wrapAround: true,scrollBar: true});

	// Add scrollTo on click on the navigation anchors
	$("nav").find("a").each(function() {
		var target = $(this).attr("href").replace("#", "");
		$(this).click(function(e) {
			//e.preventDefault();
			
			// Include the jQuery easing plugin (http://gsgd.co.uk/sandbox/jquery/easing/)
			// for extra easing functions like the one below
			$.fn.scrollPath("scrollTo", target, 1000, "easeInOutSine");
		});
	});

	/* ===================================================================== */

	$(".settings .show-path").click(function(e) {
		//e.preventDefault();
		$(".sp-canvas").toggle();
	}).toggle(function() {
		$(this).text("Hide Path");
	}, function() {
		$(this).text("Show Path");
	});

	}


function highlight(element) {
	if(!element.hasClass("highlight")) {
		element.addClass("highlight");
		setTimeout(function() { element.removeClass("highlight"); }, 2000);
	}
}
function ordinal(num) {
	return num + (
		(num % 10 == 1 && num % 100 != 11) ? 'st' :
		(num % 10 == 2 && num % 100 != 12) ? 'nd' :
		(num % 10 == 3 && num % 100 != 13) ? 'rd' : 'th'
	);
}
jQuery.fn.center = function () {
	console.log('');
    $( ".plane" ).css("top", $( ".plane" ).position().top - ($( ".plane" ).height() / 2) + "px");
    $( ".plane" ).css("left", $( ".plane" ).position().left - ($( ".plane" ).width() / 2) + "px");
    return this;
}

jQuery.fn.rotate = function(str,end) {
	var rotation = getRotationDegrees($(this));
	if (rotation==str)
		rotation = end
	else
		rotation = str
    $(this).css({'-webkit-transform' : 'rotate('+ rotation +'deg)',
                 '-moz-transform' : 'rotate('+ rotation +'deg)',
                 '-ms-transform' : 'rotate('+ rotation +'deg)',
                 'transform' : 'rotate('+ rotation +'deg)'});
    return $(this);
};

jQuery.fn.toggleImg = function() {
	var img = $(this).find("img");
    var src = img.attr('src');
	if (src == "/liub/static/images/plane.svg")
		img.attr("src", "/liub/static/images/boat.svg");
	else
		img.attr("src", "/liub/static/images/plane.svg");
	return $(this);
};

function getRotationDegrees(obj) {
    var matrix = obj.css("-webkit-transform") ||
    obj.css("-moz-transform")    ||
    obj.css("-ms-transform")     ||
    obj.css("-o-transform")      ||
    obj.css("transform");
    if(matrix !== 'none') {
        var values = matrix.split('(')[1].split(')')[0].split(',');
        var a = values[0];
        var b = values[1];
        var angle = Math.round(Math.atan2(b, a) * (180/Math.PI));
    } else { var angle = 0; }
    return (angle < 0) ? angle + 360 : angle;
}