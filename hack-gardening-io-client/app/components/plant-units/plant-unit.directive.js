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
    $scope.plantName = $scope.plantObj.plant.name;
    $scope.plantState = $scope.plantObj.state;

    $scope.seedDate = new Date($scope.plantObj.plant_date);
    $scope.harvestDate = new Date($scope.plantObj.crop_date);

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
        if ($scope.currentDate < $scope.seedDate) {
            $scope.abort = true;
        } else {
            $scope.abort = true;
            $scope.seed = true;
        }
    } else if ($scope.plantState == 'in_progress') {
        $scope.abort = true;
    } else if ($scope.plantState = 'ready_to_harvest') {
        $scope.yield = true;
    }
});