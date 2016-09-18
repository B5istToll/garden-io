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
    };

    this.getEvents = function() {
      var deferred = $q.defer();
      var oneWeekAgo = new Date();
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
      var isoString = oneWeekAgo.getFullYear()+'-' + (oneWeekAgo.getMonth()+1) + '-'+oneWeekAgo.getDate();//prints expected format.
      $http.get('http://localhost:6677/api/garden/events?date=' + isoString).then(function (data) {
          deferred.resolve(data);
      });
      return deferred.promise;
    };

    this.updatePlant = function (data) {
        $http.post('http://localhost:6677/api/garden/update_plant', data);
        // TODO post not possible, change backend code
    };

});
