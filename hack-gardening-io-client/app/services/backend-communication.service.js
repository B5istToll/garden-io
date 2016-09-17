/**
 * Created by Forster on 17.09.16.
 */


angular.
module('gardenDesigner').service('backendService', function ($http, $q) {
    this.getPlants = function () {
        var deferred = $q.defer();
        $http.get('http://localhost:6677/api/plants').then(function (data) {
            deferred.resolve(data);
        });
        return deferred.promise;
    };

    this.getGarden = function () {
        var deferred = $q.defer();
        $http.get('http://localhost:6677/api/garden').then(function (data) {
            deferred.resolve(data);
        });
        return deferred.promise;
    }
});
