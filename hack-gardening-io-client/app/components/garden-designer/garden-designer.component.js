/**
 * Created by Forster on 17.09.16.
 */


'use strict';

// Register `phoneList` component, along with its associated controller and template
angular.
module('gardenDesigner').
component('gardenDesigner', {
    templateUrl: 'components/garden-designer/garden-designer.template.html',
    controller: ['$scope', 'backendService',
        function GardenDesignerController($scope, backendService) {
            $scope.greeting="Blahhhhhhhhhhhhh";
            $scope.controlsMenuTemplate="components/controls-menu/controls-menu.template.html";

            $scope.plants = {};
            var promise = backendService.getPlants();
            promise.then(function (data) {
                $scope.plants = data;
                console.log(data);
            });

            $scope.garden = {};
            var promise2 = backendService.getGarden();
            promise2.then(function (data) {
                $scope.garden = data;
                console.log(data);
            });
        }
    ]
});
