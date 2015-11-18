$(function(){
	
	$('.demo1').craftmap({
		image: {
			width: 1652,
			height: 1221
		}
	});

});

$(window).ready(function() {
	var h = $('.navbar').outerHeight()+40+$('.footer').outerHeight()+20;
	h = $(window).height() - h;
	var w = $('.col-md-12').width();
	$('.demo1').width(w);
	$('.demo1').height(h);
	$('#content').height(h);
	$('#content').width(w);
	$('.imgMap').width(1652);

});

$(window).resize(function() {
	var h = $('.navbar').outerHeight()+40+$('.footer').outerHeight()+20;
	h = $(window).height() - h;
	var w = $('.col-md-12').width();
	$('.demo1').width(w);
	$('.demo1').height(h);
	$('#content').height(h);
	$('#content').width(w);
});