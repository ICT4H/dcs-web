function initialize() {
    var myLatlng = new google.maps.LatLng(12.960398, 77.604446);
    var mapOptions = {
        zoom: 13,
        center: myLatlng
    }
    var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

    add(map);

}
google.maps.event.addDomListener(window, 'load', initialize);

console.log("submissionDetails: "+submissionDetails);

function add(map) {

    for(var i=0; i<submissionDetails.length; i++) {
        var s = submissionDetails[i];
        var latlng = new google.maps.LatLng(parseFloat(s.long), parseFloat(s.lat));
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(parseFloat(s.long), parseFloat(s.lat)),
            map: map,
            title: "Click!"
        });

        (function(s, marker){
            var infowindow = new google.maps.InfoWindow({
                content: s.complaint
            });

            (function(marker){
                google.maps.event.addListener(marker, 'click', function () {
                    infowindow.open(map, marker);
                });
            })(marker);

        })(s, marker);


    }
}
//    var contentString = '<div id="content">' +
//        '<div id="siteNotice">' +
//        '</div>' +
//        '<h1 id="firstHeading" class="firstHeading">Uluru</h1>' +
//        '<div id="bodyContent">' +
//        '<p><b>Uluru</b>, also referred to as <b>Ayers Rock</b>, is a large ' +
//        'sandstone rock formation in the southern part of the ' +
//        'Northern Territory, central Australia. ' +
//        '</div>';

