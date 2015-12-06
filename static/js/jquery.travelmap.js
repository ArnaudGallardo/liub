/**
 * Travelmap - jQuery Plugin
 * Pin anything on Google map with jQuery
 *
 * Examples and documentation at: https://github.com/microtroll/jquery-travel
 *
 * Copyright (c) 2014 microtroll
 *
 * Version: 1.9.7
 * Requires: jQuery v2+
 *
 * Dual licensed under the MIT and GPL licenses:
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.gnu.org/licenses/gpl.html
 */

(function($) {
  'use strict';

  $.fn.travelmap = function(settings) {

    var o = {
      data: 'cities.json',
      center: [0, 0], // lat, lng
      width: 550,
      height: 500,
      zoom: 1,
      markImage: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsSAAALEgHS3X78AAAACXZwQWcAAAAQAAAAEABcxq3DAAABgklEQVQ4y42Sv0sCYRjHP+97GhFU1OCiQUQ0yhXOaVtzexTNWUFroP0BLrVH0CrObRU0Rl4NDiJy4NHQUCgh1yHv23BnnYcnPfDC8/Pzfl+eV2itGZoQAoALkwJQBvJB6QEoF+v6noiJKODCpDylKJkClqWftxVYGjzJebGuy7GAy3VRmFLcmQKUHr1Jil/IVliJjCgqDYfncnmy1Rey1RfmcnmUBtN/YWkEHAEUUoGzVqmRTKVJptKsVWoABLXCJAAzoczg22Xw7Y6txQFanvKd5ukOfadN32nTPN0BIKi1wgOJCODRVqwuaOg9PfC+twnAtIRZBbYADB4nKThpCLrzBqwYkJH+WTFg3oCGoAucxAKOLLqe5PgtiJX+W+cb4EmOi3Xdjf0Hw594bdLZFmQ+/JBFDbcaZ99iKdw/dgsAPTizFQy0f2zl58b1jlUAcGXS2YAMwDM4BxZLAP9SAPAFh64Hruf7cX2xCgBustQBdl9ZH+aiChJMsE85urLoMMAPnKWcG4TKFSgAAAAldEVYdGNyZWF0ZS1kYXRlADIwMTItMDUtMTVUMDk6MDE6MTIrMDA6MDDHBWYEAAAAFXRFWHRDcmVhdGlvbiBUaW1lADIvMTcvMDggnKpYAAAAJXRFWHRtb2RpZnktZGF0ZQAyMDEyLTA1LTE1VDA5OjAxOjEyKzAwOjAwmLQQMAAAABx0RVh0U29mdHdhcmUAQWRvYmUgRmlyZXdvcmtzIENTM5jWRgMAAAGrelRYdFhNTDpjb20uYWRvYmUueG1wAAB42tVSTWvbQBC9+1cM22ul/ZBiRYukUGxMCLiU2NDS20q7UoSt3WW1QRv/+h7suI4JPQRy6DsO72PmMcVdsKLZKQ+16npdIgBA0MsS/bxZk7VdqKf+/uDU5vB92xx2TS7RXTUrAg+DHZQXEIa9HnkokZCmVlyPfFBeYASBh8H6XYm+SVMr+LX+AQvjFKQxjRqSpJDOY5axPJt/hY3w8CA0sAwYIRkwxinlKYUTUDUDgMLJlj8uV6dMJ9sSPXlvOcbTNMVTEhvXYZrnOSYMMxY52Ubji/YiRHr8cjR59VmqsXG99b3R4GTLRW2efYnQDC5wOk7Yc5AeYyFNreLGDDgIi2lM8NkZAIogLF84JbxxW2P21fH8Ve/UZNxuhMUmKfA16T29WgqvKkbIbURYRLMtYTyZ8/Tm94X+SLqSr43s25cLeRKxdEtzTghP2Ul+QXrtBV8V89HCZHPuyz67fWxch2WD1V4NSvsR05i+7Uw2vDVuEL7qB9EpbHVX4L/Df+53nD4uV9WswOe/rN6s9Vn470P+AMIj+zIH4sBMAAAAAElFTkSuQmCC',
      markShadow: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAQEAYAAABVX8OsAAAABmJLR0T///////8JWPfcAAAACXBIWXMAAABIAAAASABGyWs+AAACc0lEQVRIx+2WO2hTYRiG/1yanrYxibaREluLlrZWUQriBXGRugkOXasg9bYUQYp4mUTqooKg4KCok4u6KCg4COJSOlQ3J6W1tMa0Nk2apKkJSTq8zxGMBJPSbPmWh5Pzn+9/3+/7LzGmFrWoRS2qGK51yuOADbATDvPaJzrvM60H3hDdbp63Me4UHCdPn1B4wfNHGIeFahXICVvgVQy9R/h50foi+reKwSVxy1GxPQHfiqFBsfmZ2DhFAT4xzxvoLypwSYGVhp0wCBHiWsBQjxh4Lrb2YaBb3P5S7Poq9pwTuzeKnTkKwPgA33sOMX2yaP6S4V6jwSZIx1x0oHGPuGmX2HwSgV18doYCsLQ8D6kzRvIYWbnN71ExeYTnOeY9Dq8XFfyfpVrpHrQ7voO8CLToRHBIbLslhh5gGGFelqZFgeqekics5g5g8K4YaxOjdC7VyzjmMfMwVUpwpR20C7IPv7MI3iwGpsQWKu6bwAh7y3EBgT/EzAcxjdDEtLjIHp6jI0uWmL0iFt6hg71d+pBZq8F2BEdI80Ss92JojOH7xfwIAjn90nQuwWER+4wxxsevicmQ+PsxeSiUeQWz5Qr+X9hLsx4e5mf2nkXH/MfEDRgyO4XUZTHKNRD5JobZm5E63t9jPAayFzE2QL6bsOzrodxT1N7ECDEZ8p8VcyzRFa6L+AzCGTdNpSdPiN8RGkbgInswfRBj/RjbzXx3YKxcY3ZU2kHbYCu+O3hNZx0ISF8SF16L83mMLIsprpMM10huFN0sVfMIzvxd0OqF3UH+gfw5Rffi+7TY9FP0Mb7hF+8pjJPDwnAPGr433qJCrlusAobpnIN3kn13AAAAAElFTkSuQmCC',
      markAnimation: null,
      mapTypeId: 'ROADMAP',
      mapTypeControl: false,
      mapTypeControlOptions: 'DEFAULT',
      zoomControl: false,
      zoomControlOptions: 'DEFAULT',
      panControl: false,
      scaleControl: false,
      overviewMapControl: false,
      streetViewControl: false,
      geoLocCheck: false,
      geoLocMessage: 'You are here',
      scrollwheel: true,
      draggable: true,
      theme: null
    };
    settings = $.extend(o, settings);

    // map types
    var mapTypeId = google.maps.MapTypeId.ROADMAP;
    if (o.mapTypeId === 'HYBRID') {
      mapTypeId = google.maps.MapTypeId.HYBRID;
    } else if (o.mapTypeId === 'SATELLITE') {
      mapTypeId = google.maps.MapTypeId.SATELLITE;
    } else if (o.mapTypeId === 'TERRAIN') {
      mapTypeId = google.maps.MapTypeId.TERRAIN;
    }

    // map controls
    var mapTypeControlOptions = google.maps.MapTypeControlStyle.DEFAULT;
    if (o.mapTypeControlOptions === 'DROPDOWN_MENU') {
      mapTypeControlOptions = google.maps.MapTypeControlStyle.DROPDOWN_MENU;
    } else if (o.mapTypeControlOptions === 'HORIZONTAL_BAR') {
      mapTypeControlOptions = google.maps.MapTypeControlStyle.HORIZONTAL_BAR;
    }

    // map zoom
    var zoomControlOptions = google.maps.ZoomControlStyle.DEFAULT;
    if (o.zoomControlOptions === 'LARGE') {
      zoomControlOptions = google.maps.ZoomControlStyle.LARGE;
    } else if (o.zoomControlOptions === 'SMALL') {
      zoomControlOptions = google.maps.ZoomControlStyle.SMALL;
    }

    // marker animation
    var markAnimation;
    if (o.markAnimation === 'DROP') {
      markAnimation = google.maps.Animation.DROP;
    } else if (o.markAnimation === 'BOUNCE') {
      markAnimation = google.maps.Animation.BOUNCE;
    }

    // set center to users location if enabled
    var pos = new google.maps.LatLng(o.center[0], o.center[1]);

    if (navigator.geolocation && o.geoLocCheck === true) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var geocoder = new google.maps.Geocoder();
        pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        if (geocoder) {
          geocoder.geocode({
            'latLng': pos
          }, function(resp, status) {
            if (status === google.maps.GeocoderStatus.OK) {
              var infowindow = new google.maps.InfoWindow({
                map: map,
                position: resp[0].geometry.location,
                content: o.geoLocMessage
              });
              map.setCenter(resp[0].geometry.location);
            } else {
              throw new Error("Geocoding failed: " + status);
            }
          });
        }
      });
    }

    // themes
    var theme;
    // themes from http://snazzymaps.com/
    if (o.theme === 'neutral-blue') {
      theme = [{
        "featureType": "water",
        "elementType": "geometry",
        "stylers": [{
          "color": "#193341"
        }]
      }, {
        "featureType": "landscape",
        "elementType": "geometry",
        "stylers": [{
          "color": "#2c5a71"
        }]
      }, {
        "featureType": "road",
        "elementType": "geometry",
        "stylers": [{
          "color": "#29768a"
        }, {
          "lightness": -37
        }]
      }, {
        "featureType": "poi",
        "elementType": "geometry",
        "stylers": [{
          "color": "#406d80"
        }]
      }, {
        "featureType": "transit",
        "elementType": "geometry",
        "stylers": [{
          "color": "#406d80"
        }]
      }, {
        "elementType": "labels.text.stroke",
        "stylers": [{
          "visibility": "on"
        }, {
          "color": "#3e606f"
        }, {
          "weight": 2
        }, {
          "gamma": 0.84
        }]
      }, {
        "elementType": "labels.text.fill",
        "stylers": [{
          "color": "#ffffff"
        }]
      }, {
        "featureType": "administrative",
        "elementType": "geometry",
        "stylers": [{
          "weight": 0.6
        }, {
          "color": "#1a3541"
        }]
      }, {
        "elementType": "labels.icon",
        "stylers": [{
          "visibility": "off"
        }]
      }, {
        "featureType": "poi.park",
        "elementType": "geometry",
        "stylers": [{
          "color": "#2c5a71"
        }]
      }];
    } else if (o.theme === 'midnight-commander') {
      theme = [{
        "featureType": "water",
        "stylers": [{
          "color": "#021019"
        }]
      }, {
        "featureType": "landscape",
        "stylers": [{
          "color": "#08304b"
        }]
      }, {
        "featureType": "poi",
        "elementType": "geometry",
        "stylers": [{
          "color": "#0c4152"
        }, {
          "lightness": 5
        }]
      }, {
        "featureType": "road.highway",
        "elementType": "geometry.fill",
        "stylers": [{
          "color": "#000000"
        }]
      }, {
        "featureType": "road.highway",
        "elementType": "geometry.stroke",
        "stylers": [{
          "color": "#0b434f"
        }, {
          "lightness": 25
        }]
      }, {
        "featureType": "road.arterial",
        "elementType": "geometry.fill",
        "stylers": [{
          "color": "#000000"
        }]
      }, {
        "featureType": "road.arterial",
        "elementType": "geometry.stroke",
        "stylers": [{
          "color": "#0b3d51"
        }, {
          "lightness": 16
        }]
      }, {
        "featureType": "road.local",
        "elementType": "geometry",
        "stylers": [{
          "color": "#000000"
        }]
      }, {
        "elementType": "labels.text.fill",
        "stylers": [{
          "color": "#ffffff"
        }]
      }, {
        "elementType": "labels.text.stroke",
        "stylers": [{
          "color": "#000000"
        }, {
          "lightness": 13
        }]
      }, {
        "featureType": "transit",
        "stylers": [{
          "color": "#146474"
        }]
      }, {
        "featureType": "administrative",
        "elementType": "geometry.fill",
        "stylers": [{
          "color": "#000000"
        }]
      }, {
        "featureType": "administrative",
        "elementType": "geometry.stroke",
        "stylers": [{
          "color": "#144b53"
        }, {
          "lightness": 14
        }, {
          "weight": 1.4
        }]
      }];
    } else if (o.theme === 'gowalla') {
      theme = [{
        "featureType": "road",
        "elementType": "labels",
        "stylers": [{
          "visibility": "simplified"
        }, {
          "lightness": 20
        }]
      }, {
        "featureType": "administrative.land_parcel",
        "elementType": "all",
        "stylers": [{
          "visibility": "off"
        }]
      }, {
        "featureType": "landscape.man_made",
        "elementType": "all",
        "stylers": [{
          "visibility": "off"
        }]
      }, {
        "featureType": "transit",
        "elementType": "all",
        "stylers": [{
          "visibility": "off"
        }]
      }, {
        "featureType": "road.local",
        "elementType": "labels",
        "stylers": [{
          "visibility": "simplified"
        }]
      }, {
        "featureType": "road.local",
        "elementType": "geometry",
        "stylers": [{
          "visibility": "simplified"
        }]
      }, {
        "featureType": "road.highway",
        "elementType": "labels",
        "stylers": [{
          "visibility": "simplified"
        }]
      }, {
        "featureType": "poi",
        "elementType": "labels",
        "stylers": [{
          "visibility": "off"
        }]
      }, {
        "featureType": "road.arterial",
        "elementType": "labels",
        "stylers": [{
          "visibility": "off"
        }]
      }, {
        "featureType": "water",
        "elementType": "all",
        "stylers": [{
          "hue": "#a1cdfc"
        }, {
          "saturation": 30
        }, {
          "lightness": 49
        }]
      }, {
        "featureType": "road.highway",
        "elementType": "geometry",
        "stylers": [{
          "hue": "#f49935"
        }]
      }, {
        "featureType": "road.arterial",
        "elementType": "geometry",
        "stylers": [{
          "hue": "#fad959"
        }]
      }];
    } else if (o.theme === 'bright-and-bubbly') {
      theme = [{
        "featureType": "water",
        "stylers": [{
          "color": "#19a0d8"
        }]
      }, {
        "featureType": "administrative",
        "elementType": "labels.text.stroke",
        "stylers": [{
          "color": "#ffffff"
        }, {
          "weight": 6
        }]
      }, {
        "featureType": "administrative",
        "elementType": "labels.text.fill",
        "stylers": [{
          "color": "#e85113"
        }]
      }, {
        "featureType": "road.highway",
        "elementType": "geometry.stroke",
        "stylers": [{
          "color": "#efe9e4"
        }, {
          "lightness": -40
        }]
      }, {
        "featureType": "road.arterial",
        "elementType": "geometry.stroke",
        "stylers": [{
          "color": "#efe9e4"
        }, {
          "lightness": -20
        }]
      }, {
        "featureType": "road",
        "elementType": "labels.text.stroke",
        "stylers": [{
          "lightness": 100
        }]
      }, {
        "featureType": "road",
        "elementType": "labels.text.fill",
        "stylers": [{
          "lightness": -100
        }]
      }, {
        "featureType": "road.highway",
        "elementType": "labels.icon"
      }, {
        "featureType": "landscape",
        "elementType": "labels",
        "stylers": [{
          "visibility": "off"
        }]
      }, {
        "featureType": "landscape",
        "stylers": [{
          "lightness": 20
        }, {
          "color": "#efe9e4"
        }]
      }, {
        "featureType": "landscape.man_made",
        "stylers": [{
          "visibility": "off"
        }]
      }, {
        "featureType": "water",
        "elementType": "labels.text.stroke",
        "stylers": [{
          "lightness": 100
        }]
      }, {
        "featureType": "water",
        "elementType": "labels.text.fill",
        "stylers": [{
          "lightness": -100
        }]
      }, {
        "featureType": "poi",
        "elementType": "labels.text.fill",
        "stylers": [{
          "hue": "#11ff00"
        }]
      }, {
        "featureType": "poi",
        "elementType": "labels.text.stroke",
        "stylers": [{
          "lightness": 100
        }]
      }, {
        "featureType": "poi",
        "elementType": "labels.icon",
        "stylers": [{
          "hue": "#4cff00"
        }, {
          "saturation": 58
        }]
      }, {
        "featureType": "poi",
        "elementType": "geometry",
        "stylers": [{
          "visibility": "on"
        }, {
          "color": "#f0e4d3"
        }]
      }, {
        "featureType": "road.highway",
        "elementType": "geometry.fill",
        "stylers": [{
          "color": "#efe9e4"
        }, {
          "lightness": -25
        }]
      }, {
        "featureType": "road.arterial",
        "elementType": "geometry.fill",
        "stylers": [{
          "color": "#efe9e4"
        }, {
          "lightness": -10
        }]
      }, {
        "featureType": "poi",
        "elementType": "labels",
        "stylers": [{
          "visibility": "simplified"
        }]
      }];
    } else if (o.theme === 'greyscale') {
      theme = [{
        "featureType": "all",
        "stylers": [{
          "saturation": -100
        }, {
          "gamma": 0.5
        }]
      }];
    } else if (o.theme === 'red-alert') {
      theme = [{
        "featureType": "water",
        "elementType": "geometry",
        "stylers": [{
          "color": "#ffdfa6"
        }]
      }, {
        "featureType": "landscape",
        "elementType": "geometry",
        "stylers": [{
          "color": "#b52127"
        }]
      }, {
        "featureType": "poi",
        "elementType": "geometry",
        "stylers": [{
          "color": "#c5531b"
        }]
      }, {
        "featureType": "road.highway",
        "elementType": "geometry.fill",
        "stylers": [{
          "color": "#74001b"
        }, {
          "lightness": -10
        }]
      }, {
        "featureType": "road.highway",
        "elementType": "geometry.stroke",
        "stylers": [{
          "color": "#da3c3c"
        }]
      }, {
        "featureType": "road.arterial",
        "elementType": "geometry.fill",
        "stylers": [{
          "color": "#74001b"
        }]
      }, {
        "featureType": "road.arterial",
        "elementType": "geometry.stroke",
        "stylers": [{
          "color": "#da3c3c"
        }]
      }, {
        "featureType": "road.local",
        "elementType": "geometry.fill",
        "stylers": [{
          "color": "#990c19"
        }]
      }, {
        "elementType": "labels.text.fill",
        "stylers": [{
          "color": "#ffffff"
        }]
      }, {
        "elementType": "labels.text.stroke",
        "stylers": [{
          "color": "#74001b"
        }, {
          "lightness": -8
        }]
      }, {
        "featureType": "transit",
        "elementType": "geometry",
        "stylers": [{
          "color": "#6a0d10"
        }, {
          "visibility": "on"
        }]
      }, {
        "featureType": "administrative",
        "elementType": "geometry",
        "stylers": [{
          "color": "#ffdfa6"
        }, {
          "weight": 0.4
        }]
      }, {
        "featureType": "road.local",
        "elementType": "geometry.stroke",
        "stylers": [{
          "visibility": "off"
        }]
      }];
    } else if (o.theme !== null) {
      // user defined
      theme = o.theme;
    } else {
      theme = null;
    }

    // basic options
    var mapOptions = {
        zoom: o.zoom,
        center: pos,
        useCurrentLocation: true,
        mapTypeId: mapTypeId,
        mapTypeControl: o.mapTypeControl,
        mapTypeControlOptions: {
          style: mapTypeControlOptions
        },
        zoomControl: o.zoomControl,
        zoomControlOptions: {
          style: zoomControlOptions
        },
        panControl: o.panControl,
        scaleControl: o.scaleControl,
        overviewMapControl: o.overviewMapControl,
        streetViewControl: o.streetViewControl,
        scrollwheel: o.scrollwheel,
        draggable: o.draggable,
        styles: theme
      },
      map = new google.maps.Map(document.getElementById(this.get(0).getAttribute('id')), mapOptions);




    $(this).css({
      width: o.width,
      height: o.height
    });

    return map;
  };

})(jQuery);
