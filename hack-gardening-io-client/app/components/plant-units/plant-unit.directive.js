/**
 * Created by Forster on 17.09.16.
 */

angular.module('gardenDesigner').directive('plantUnit', function () {
    return {
        restrict: 'E',
        scope: {
            plantObj: '=plant',
            imgpath: '=img',
            currentDate: '=date'
        },
        templateUrl: 'components/plant-units/plant-unit.template.html',
        controller: 'plantUnitController'
    };
}).controller('plantUnitController', function ($scope) {
    $scope.plantName = plantObj.plant.name;
    $scope.plantState = plantObj.state;

    $scope.seedDate = new Date(plantObj.plant_date);
    console.log("seed: ",$scope.seedDate);
    
    $scope.setFlags = function () {
        $scope.change = false;
        $scope.confirm = false;
        $scope.abort = false;
        $scope.seed = false;
        $scope.yield = false;
    };
    $scope.setFlags();

    if ($scope.plantState == 'suggestion') {
        $scope.change = true;
        $scope.confirm = true;
    } else if ($scope.plantState == 'scheduled') {

        $scope.abort = true;
    } else if ($scope.plantState == 'scheduled') {
        $scope.abort = true;
    }
});