/**
 * Created by Forster on 17.09.16.
 */

angular.module('gardenDesigner').directive('plantUnit', function () {
    return {
        restrict: 'E',
        scope: {
            plantName: '=name',
            imgpath: '=img'
        },
        templateUrl: 'components/plant-units/plant-unit.template.html'
    };
});