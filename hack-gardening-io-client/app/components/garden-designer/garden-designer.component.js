/**
 * Created by Forster on 17.09.16.
 */


'use strict';

// Register `phoneList` component, along with its associated controller and template
angular.
module('gardenDesigner').
component('gardenDesigner', {
    templateUrl: 'components/garden-designer/garden-designer.template.html',
    controller: ['$scope',
        function GardenDesignerController($scope) {
            $scope.greeting="Blahhhhhhhhhhhhh";
        }
    ]
});
