/**
 * Created by Forster on 17.09.16.
 */


'use strict';

// Register `phoneList` component, along with its associated controller and template
angular.
module('gardenDesigner').
component('gardenDesigner', {
    templateUrl: 'components/garden-designer/garden-designer.template.html',
    controller: ['$scope', '$rootScope', 'backendService',
        function GardenDesignerController($scope, $rootScope, backendService) {
            $scope.greeting="Blahhhhhhhhhhhhh";
            $scope.controlsMenuTemplate="components/controls-menu/controls-menu.template.html";
            $scope.gardenGridTemplate="components/garden-grid/garden-grid.template.html";

            $scope.plants = {};
            var promise = backendService.getPlants();
            promise.then(function (data) {
                $scope.plants = data;
                //console.log(data);
            });

            $scope.garden = {};
            var promise2 = backendService.getGarden();
            promise2.then(function (data) {
                $scope.garden = data;
                //console.log($scope.garden.data.tiles);
            });

            $scope.getImgPath = function (name) {
                if (name == 'Brokkoli') return "components/img/brokkoli.png";
                if (name == 'Rotkohl') return "components/img/rotkohl.png";
                if (name == 'Kartoffeln') return "components/img/kartoffel.png";
                if (name == 'Moehren') return "components/img/moehre.png";
                if (name == 'Radieschen') return "components/img/radieschen.png";
                if (name == 'Rote Beete') return "components/img/rotebeete.png";
                if (name == 'Feldsalat') return "components/img/feldsalat.png";
                if (name == 'Auberginen') return "components/img/auberginen.png";
                if (name == 'Kuerbis') return "components/img/kuerbis.png";
                if (name == 'Zucchini') return "components/img/zucchini.png";
                if (name == 'Peperoni') return "components/img/peperoni.png";
                if (name == 'Tomaten') return "components/img/tomaten.png";
                if (name == 'Zuckermais') return "components/img/zuckermais.png";
                if (name == 'Lauch') return "components/img/lauch.png";
                if (name == 'Zwiebeln') return "components/img/zwiebeln.png";
                if (name == 'Knoblauch') return "components/img/knoblauch.png";
                if (name == 'Weisser Spargel') return "components/img/spargel.png";
            };

            $scope.events = {};
            var promise3 = backendService.getEvents();
            promise3.then(function(data) {
              $scope.events = data;
              var currentDate = new Date();
              var dateString = currentDate.toISOString().slice(0,10);
              console.log($scope.events.data.length);
              console.log(dateString);
              for (var i = 0; i < $scope.events.data.length; i++) {
                if ($scope.events.data[i].date.replace('/-','/') < dateString){
                  $scope.events.data[i].rowClass = "danger";
                }
                else if ($scope.events.data[i].date.replace('/-','/') == dateString){
                  $scope.events.data[i].rowClass = "success";
                }
                else {
                  $scope.events.data[i].rowClass = "";
                }
              }
              console.log(data);
            });

            $scope.getRowClass = function(event) {
              return event.rowClass;
            };

            $scope.getRainAmount = function(event) {
              if (event.rain_amount == undefined) {
                return "";
              }
              else {
                return event.rain_amount + "mm";
              }
            }

            // Date Picker ------------------------------------------------

            $scope.model = {dt: new Date(2016,0,1,0,0,0,0)};

            $scope.$watch('model.dt', function () {
                $rootScope.$emit('dateChanged', $scope.model.dt);
            });

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
                minDate: new Date(2016,0,1),
                startingDay: 1
            };

            $scope.altInputFormats = ['M!/d!/yyyy'];

            // ------------------------------------------------

        }
    ]
});
