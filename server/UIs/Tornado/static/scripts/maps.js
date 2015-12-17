// Define global variables
var ws_connection = "ws://" + ipaddr + ":" + String(port) + "/wsmap";
var ws = new WebSocket(ws_connection);
var map;
var num_pis = 0;
var markers = {};
var lobMarkers = {};
var laptop_pos = new google.maps.LatLng(laptop_lat, laptop_lon);
var laptopMarker;
var bounds = new google.maps.LatLngBounds(laptop_pos, laptop_pos);


function updateMarker(marker_info) {
    var marker_info = JSON.parse(marker_info);

    // Add a marker for a newly attached receiver node
    if (marker_info.action == 'add') {
        // Place marker on map
        var marker_name = marker_info.nodeName;
        var markerX = new google.maps.Marker({
            position: new google.maps.LatLng(marker_info.lat, marker_info.lon),
            map: map,
            title: marker_info.nodeName + "\nLat: " + String(marker_info.lat) + ", Lon: " + String(marker_info.lon),
            icon: "static/images/pi.png",
        }); 
        markers[marker_name] = markerX;
        markerX.setMap(map);

        // Add on-click listener for node info pop-up box
        google.maps.event.addListener(markerX, 'click', function() {
            $('#spectrum-div').toggle(200).html("Node: " + marker_name + "<br/>Lat: " + markerX['position'].d + "<br/>Lon: " + markerX['position'].e);//.fadeOut(10000);
        });

        // Adjust value in pi_info box
        num_pis = 0;
        for (marker in markers) { num_pis = num_pis + 1 };
        $("#pi_info").html("<center>Nodes:<br>" + num_pis + "</center>");
    }

    // Add a marker for a newly attached transmitter node
    if (marker_info.action == 'addTx') {
        // Place marker on map
        var marker_name = marker_info.nodeName;
        var markerX = new google.maps.Marker({
            position: new google.maps.LatLng(marker_info.lat, marker_info.lon),
            map: map,
            title: marker_info.nodeName + "\nLat: " + String(marker_info.lat) + ", Lon: " + String(marker_info.lon),
            icon: "static/images/tx_35px.png",
        }); 
        markers[marker_name] = markerX;
        markerX.setMap(map);
        google.maps.event.addListener(markerX, 'click', function() {
            $('#spectrum-div').toggle(200).html("Node: " + marker_name + "<br/>Lat: " + markerX['position'].d + "<br/>Lon: " + markerX['position'].e);//.fadeOut(10000);
        });

        // Adjust value in pi_info box; I'm leaving this code here in case we decide we'd like a transmitter_info box
        //num_pis = 0;
        //for (marker in markers) { num_pis = num_pis + 1 };
        //$("#pi_info").html("<center>Nodes:<br>" + num_pis + "</center>");
    }

    // Remove a marker for a node that went offline
    else if (marker_info.action == 'remove') {

        // Adjust value in pi_info box
        num_pis = num_pis - 1;
        $("#pi_info").html("<center>Nodes:<br>" + num_pis + "</center>");

        // Place marker on map
        if (markers[marker_info.nodeName]) {
            markers[marker_info.nodeName].setMap(null);
        }; 

        // Adjust value in pi_info box
        num_pis = 0;
        for (marker in markers) { num_pis = num_pis + 1 };
        $("#pi_info").html("<center>Nodes:<br>" + num_pis + "</center>");
    }
    
    // Add a LOB to an existing node marker
    else if (marker_info.action == 'addLob') {
        // Erase previous LOB if there is one
        if (marker_info.name in lobMarkers) {
            lobMarkers[marker_info.name].setMap(null);
        }
        // Get position of node associated with LOB
        var pos = markers[marker_info.nodeName].position;
        // Place LOB on map on appropriate node marker
        var angle = marker_info.angle;
        var lob_image = "static/images/lobs/lob_" + String(angle) + ".png";
        // Offset should be 760 for 270 < angle < 90, 10 otherwise
        var offset = 760;
        if ((angle > 90) && (angle < 270)) { offset = 10 };
        var new_lob_icon = {
            anchor: new google.maps.Point(750, offset),
            url: lob_image,
        }; 
        var lob_marker = new google.maps.Marker({
            position: pos,
            map: map,
            icon: new_lob_icon,
        });
        //lob_marker.setMap(map);
        lobMarkers[marker_info.name] = lob_marker;
    }

    else if (marker_info.action == 'update') {
        markers[marker_info.nodeName].setPosition(new google.maps.LatLng(marker_info.lat, marker_info.lon));
        markers[marker_info.nodeName].setTitle(marker_info.nodeName + "\nLat: " + String(marker_info.lat) + ", Lon: " + String(marker_info.lon));
    }
}


function closeSpectrum() {
    // Called by clicking button in #spectrum-div
    $('#spectrum-div').toggle('slow', function() {});
    $('#audio_stream').get(0).pause();
}


function zoomMarkers() {
    // Set map zoom to show all markers, centered on laptop
    // Called by clicking 'pi-info' div

    // Initialize variables
    var latmin = laptopMarker.position.lat();
    var latmax = laptopMarker.position.lat();
    var lonmin = laptopMarker.position.lng();
    var lonmax = laptopMarker.position.lng();

    //bounds.extend(laptopMarker.position);
    // Find nodes farthest away from laptop and zoom to enclose these
    var diff = 0.0;
    for (marker in markers) {
        // The below four lines center on the pis, not on the laptop
        //if (markers[marker].position.lat() < latmin) { latmin = markers[marker].position.lat() }
        //if (markers[marker].position.lat() > latmax) { latmax = markers[marker].position.lat() }
        //if (markers[marker].position.lng() < lonmin) { lonmin = markers[marker].position.lng() }
        //if (markers[marker].position.lng() > lonmax) { lonmax = markers[marker].position.lng() }

        // The below lines should keep the zoom centered on the laptop marker
        if (markers[marker].position.lat() < latmin) {
            diff = latmin - markers[marker].position.lat();
            latmin = latmin - diff;
            latmax = latmax + diff;
            //alert("latmin1, latmax1, diff: " + latmin + ", " + latmax + ", " + diff);
        }
        if (markers[marker].position.lat() > latmax) {
            diff = markers[marker].position.lat() - latmax;
            latmax = latmax + diff;
            latmin = latmin - diff;
            //alert("latmin2, latmax2, diff: " + latmin + ", " + latmax, + ", " + diff);
            //alert("diff: " + diff);
        }
        if (markers[marker].position.lng() < lonmin) {
            diff = lonmin - markers[marker].position.lng();
            lonmin = lonmin - diff;
            lonmax = lonmax + diff;
            //alert("lonmin1, lonmin1, diff: " + lonmin + ", " + lonmax, + ", " + diff);
        }
        if (markers[marker].position.lng() > lonmax) {
            diff = markers[marker].position.lng() - lonmax;
            lonmax = lonmax + diff;
            lonmin = lonmin - diff;
            //alert("lonmin2, lonmin2, diff: " + lonmin + ", " + lonmax, + ", " + diff);
        }
    }
    // LatLngBounds(southwest_marker, northeast_marker)
    //bounds.extend(new google.maps.LatLng(latmin, lonmin), new google.maps.LatLng(latmax, lonmax));
    bounds.extend(new google.maps.LatLng(latmax, lonmin), new google.maps.LatLng(latmin, lonmax));
    var new_center = bounds.getCenter()
    //alert(new_center);
    map.fitBounds(bounds);

}


function initialize() {
    // Create map using Google Maps API v3
    var mapOptions = { 
        center: laptop_pos,
        zoom: 16, 
        mapTypeId: google.maps.MapTypeId.HYBRID
    };  
    map = new google.maps.Map(document.getElementById("map-canvas"),
        mapOptions);

    // Place marker for laptop; coordinates passed in as server command line options
    laptopMarker = new google.maps.Marker({
        position: new google.maps.LatLng(laptop_lat, laptop_lon),
        map: map,
        title: "Domain Manager\nLat: " + String(laptop_lat) + ", Lon: " + String(laptop_lon),
        icon: "static/images/redhawk_35px.png"
    }); 

    // Clicking laptop icon shows spectrum and plays audio for all pis
    google.maps.event.addListener(laptopMarker, 'click', function() {
        $('#spectrum-div').toggle(200).html("Domain Manager<br/>Lat: " + laptop_lat + "<br/>Lon: " + laptop_lon);//.fadeOut(10000);
    });

    // Call updateMarker on receipt of Websockets message
    ws.onmessage = function(e) {
        updateMarker(JSON.parse(e.data));
    };
}
google.maps.event.addDomListener(window, 'load', initialize);

$("#pi_info").click(function() {
    zoomMarkers();
});
