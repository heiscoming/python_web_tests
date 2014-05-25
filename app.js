angular.module('YmapsDemo', ['ymaps']).controller('MapCtrl', function ($scope, $http) {
    function generateMarkers(tlCorner, brCorner, count) {
        var deltaLat = tlCorner[0] - brCorner[0],
            deltaLon = brCorner[1] - tlCorner[1],
            markers = [];
        for(var i = 0; i < count; i++) {
            var lat = brCorner[0] + Math.random()*deltaLat,
                lon = tlCorner[1] + Math.random()*deltaLon;
            markers.push({coordinates: [lat, lon]});
        }
        return markers;
    }
    function get() {
        m = [];
        $http.get("http://127.0.0.1:5000/position")
          .then(function(result) {
            for (i = 0; i < result.data.positions.length; ++i) {
                m.push({coordinates: [
                    result.data.positions[i].lat, 
                    result.data.positions[i].long,
                    result.data.positions[i]._id
                ]});
            }
        });
        return m;     
    }
    $scope.removeMarker = function(id) {
        $http.delete("http://127.0.0.1:5000/position?id=" + id)
          .then(function(result) {
            $scope.markers = get();
        });
    };
    $scope.deleteAll = function() {
        $http.delete("http://127.0.0.1:5000/position")
          .then(function(result) {
            $scope.markers = get();
        });
    };
    $scope.submitMarker = function(lat, lon) {
        if(lat && lon) {
            $http({
                url: "http://127.0.0.1:5000/position",
                method: "POST",
                data: JSON.stringify({lat:lat, lon:lon}),
                headers: {'Content-Type': 'application/json'}
                })
              .then(function(result) {
                $scope.addingMarker = false;
                $scope.markers = get();
            });
            // $scope.markers.push({coordinates: [lat, lon]});
            
        }
    };
    $scope.addMarker = function() {
        $scope.addingMarker = true;
    };
	$scope.map = {
		center:[55.76, 37.64], // Москва
        zoom:10
	};
    // $scope.markers = generateMarkers([57.18, 35.55], [52.43, 40.23], 10);
    $scope.markers = get();
});