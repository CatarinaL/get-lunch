$.mynamespace = {};

$(document).ready(function() {
  var position;
  if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position){
        $.mynamespace.latitude = position.coords.latitude;
        $.mynamespace.longitude = position.coords.longitude;
        getBusiness();
        $("#get-new-business").click(getBusiness);
      });
  } else {
      $("#user-location").innerHTML = " Geolocation is not supported by this browser. Results in Dublin, Ireland. ";
  }

});

function getBusiness() {
   $.getJSON("/getbusiness/",
         {
           latitude: $.mynamespace.latitude,
           longitude: $.mynamespace.longitude
         }
       ).done(function(data) {
           //var name = data['name'];
           //document.getElementById("user-location");
           $(".business-name").text(data["name"]);
           $("#business-photo").attr("src", data["image_url"]);
           var mapsOrigin = "&origin=" + $.mynamespace.latitude + "," + $.mynamespace.longitude;
           var mapsDestination = "&destination=" + data["coordinates"]["latitude"] + "," + data["coordinates"]["longitude"];
           var mapsPath = "https://www.google.com/maps/dir/?api=1" + mapsOrigin + mapsDestination;
           $("#user-location").text("your location.");
           $("#user-distance").text(Math.round(data["distance"]));
           $("#directions-maps").attr("href", mapsPath);
         });
}




// function showPosition(position) {
//     var buttonNewBusiness = document.getElementById("get-new-business")
//     var user_pos = document.getElementById("user-pos");
//     var latlong = " Latitude: " + position.coords.latitude +
//     ", Longitude: " + position.coords.longitude;
//     user_pos.innerHTML = latlong;
//     //user_pos.insertAdjacentHTML( 'beforeend', latlong );
//     buttonNewBusiness.href += "?latitude=" + position.coords.latitude +
//     "&longitude=" + position.coords.longitude;
//
// }
