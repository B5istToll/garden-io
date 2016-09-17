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
                console.log($scope.garden.data.tiles);
            });

            $scope.getImgPath = function (name) {
                if (name == 'Brokkoli') return "components/img/brokkoli.png";
                if (name == 'Rotkohl') return "components/img/rotkohl.png";
                if (name == 'Kartoffeln') return "components/img/kartoffel.png";
                if (name == 'Möhren') return "components/img/moehre.png";
                if (name == 'Radieschen') return "components/img/radieschen.png";
                if (name == 'Rote Beete') return "components/img/rotebeete.png";
                if (name == 'Feldsalat') return "components/img/feldsalat.png";
                if (name == 'Auberginen') return "components/img/auberginen.png";
                if (name == 'Kürbis') return "components/img/kuerbis.png";
                if (name == 'Zucchini') return "components/img/zucchini.png";
                if (name == 'Peperoni') return "components/img/peperoni.png";
                if (name == 'Tomaten') return "components/img/tomaten.png";
                if (name == 'Zuckermais') return "components/img/zuckermais.png";
                if (name == 'Lauch') return "components/img/lauch.png";
                if (name == 'Zwiebeln') return "components/img/zwiebeln.png";
                if (name == 'Knoblauch') return "components/img/knoblauch.png";
                if (name == 'Weisser Spargel') return "components/img/spargel.png";
            }

            // Date Picker ------------------------------------------------

            $scope.today = function() {
                $scope.dt = new Date();
            };
            $scope.today();
            
            $scope.datepopup = {
                opened: false
            };

            $scope.openDatePicker = function() {
                $scope.datepopup.opened = true;
            };

            $scope.dateOptions = {
                //dateDisabled: disabled,
                formatYear: 'yy',
                maxDate: new Date(2020, 5, 22),
                minDate: new Date(),
                startingDay: 1
            };

            $scope.altInputFormats = ['M!/d!/yyyy'];

            function disabled(data) {
                var date = data.date,
                    mode = data.mode;
                return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
            }

            // ------------------------------------------------

        }
    ]
});
