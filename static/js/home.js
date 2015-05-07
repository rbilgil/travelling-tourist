"use strict";

function mapHeight() {
    $("#map").height($(window).height());
}

$(function() {

    mapHeight();

    $(window).resize(function() {
        mapHeight();
    });

    $("#searchBox").focus(function() {
        $('.slider').addClass("closed");
    });
});

function getPlaceNames(places) {
    var names = [];
    angular.forEach(places, function(value, index) {
        names.push(displayName(value));
    });

    return names;
}

function displayName(place, long) {
    var name = place["name"] + ", " + place["location"]["formattedAddress"][0];

    if (long) {
        angular.forEach(place["location"]["formattedAddress"], function(value, index) {
            if (index > 0) {
                name += ", " + value
            }
        });
    }
    return name;
}

function refreshMarkers(map, places) {
    map.removeMarkers();
    angular.forEach(places, function(place) {
       map.addMarker({
            lat: place["location"]["lat"],
            lng: place["location"]["lng"],
            title: place["name"],
            infoWindow: {
                content: '<p>' + displayName(place, true) + '</p>'
            }
        });
    });
}

app.controller("SearchController", function($scope, $http) {
    $scope.search_query = "";
    $scope.placeNames = [];
    $scope.places = [];
    $scope.selectedPlaces = [];

    var map = new GMaps({
        div: '#map',
        lat: 51.500152,
        lng: -0.126236,
        zoom: 12
    });

    $scope.searchPlaces = function() {
        $http.get("/places/search?query=" + $scope.search_query).success(function(data) {
            $scope.places = data["suggestions"];
            $scope.placeNames = getPlaceNames($scope.places);
        });
    };

    $scope.addPlace = function(placeName) {
        var index = $scope.placeNames.indexOf(placeName);
        $scope.selectedPlaces.push($scope.places[index]);
        $scope.search_query = "";
        refreshMarkers(map, $scope.selectedPlaces);
        $( "#searchBox" ).focus();
    };

    $scope.removePlace = function(index) {
        $scope.selectedPlaces.splice(index, 1);
        refreshMarkers(map, $scope.selectedPlaces);
    };

    $scope.getRoute = function() {
        var values = $scope.selectedPlaces.map( function(val) {
           return [val["name"], val["location"]["lat"], val["location"]["lng"]]
        });

        console.log(values);

        $http({
            url: "/route",
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            data: JSON.stringify({ "places": values })
        }).success(function(data) {
          console.log(data)
        });
    };

    $scope.routingDisabled = function() {
        return $scope.selectedPlaces.length < 2
    };

});

