"use strict"

function selectorize(className) {
	return "." + className;
}

var classes = {
	searchBox: "searchBox",
	place: "place",
	shopList: "shopList",
};

function addPlace(selector, place) {
	var inputAttrs = {
		type: 'hidden',
		name: place.id,
		"data-placeName": place.name
	}

	var input = $("<input>");
	// Apply each attribute to the hidden input 
	$.each(inputAttrs, function(key, val) {
		input.attr(key, val);
	});

	var label = $("<label></label>").addClass(classes.place)
									.text(place.name);

	var child = $(selector + ":last-child");
	console.log(child);
	child.after(label).after(input);
};

$(function() {

	$(selectorize(classes.searchBox)).autocomplete(
		{
			lookupLimit: 5,
		    serviceUrl: '/places/search',
		    onSelect: function (suggestion) {
		        addPlace(selectorize(classes.shopList), suggestion)
		    }
		}
	);
});