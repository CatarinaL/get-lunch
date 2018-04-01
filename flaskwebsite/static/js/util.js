window.onload = getLocation;

function getLocation() {
    var user_pos = document.getElementById("user-pos");
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        user_pos.innerHTML = " Geolocation is not supported by this browser. Results in Dublin, Ireland. ";
    }
}

function showPosition(position) {
    var buttonNewBusiness = document.getElementById("get-new-business")
    var user_pos = document.getElementById("user-pos");
    var latlong = " Latitude: " + position.coords.latitude +
    ", Longitude: " + position.coords.longitude;
    user_pos.innerHTML = latlong;
    //user_pos.insertAdjacentHTML( 'beforeend', latlong );
    buttonNewBusiness.href += "?latitude=" + position.coords.latitude +
    "&longitude=" + position.coords.longitude;

}
