/**
 * Created by Forster on 17.09.16.
 */

angular.module('gardenDesigner').directive('plantUnit', function () {
    return {
        restrict: 'E',
        scope: {
            plantObj: '=plant',
            imgpath: '=img',
            currentDate: '=date',
            posX: '=x',
            posY: '=y'
        },
        templateUrl: 'components/plant-units/plant-unit.template.html',
        controller: 'plantUnitController'
    };
}).controller('plantUnitController', function ($scope, $rootScope, $uibModal, backendService) {

    var changeRequested;

    $scope.setFlags = function () {
        $scope.change = false;
        $scope.confirm = false;
        $scope.abort = false;
        $scope.seed = false;
        $scope.yield = false;
        $scope.progressBar = false;
        $scope.progress = 0;
        if ($scope.plantState === 'suggestion') {
            $scope.change = true;
            $scope.confirm = true;
        } else if ($scope.plantState === 'scheduled') {
            //console.log("Dates. Current: ", $scope.currentDate, "  Seed: ", $scope.seedDate);
            if ($scope.currentDate < $scope.seedDate) {
                $scope.abort = true;
            } else {
                $scope.abort = true;
                $scope.seed = true;
            }
        } else if ($scope.plantState === 'in_progress') {
            //console.log("Dates. Current: ", $scope.currentDate, "  Harvest: ", $scope.harvestDate);
            $scope.abort = true;
            $scope.progressBar = true;
            var daysElapsed = ($scope.currentDate - $scope.seedDate)/1000/60/60/24;
            var daysToGrow = ($scope.harvestDate - $scope.seedDate)/1000/60/60/24;
            $scope.progress = daysElapsed/daysToGrow*100;
            if ($scope.progress >=100) {
                $scope.plantState='ready_to_harvest';
            }
            //console.log("Fortschritt: ",$scope.progress);
            //console.log("Schon vergangen: ",daysElapsed);
            //console.log("Tage insgesamt: ",daysToGrow);
        } else if ($scope.plantState === 'ready_to_harvest') {
            $scope.yield = true;
        }
    };

    $scope.initTile = function () {
        $scope.plantName = $scope.plantObj.plant.name;
        $scope.plantState = $scope.plantObj.state;

        $scope.seedDate = new Date($scope.plantObj.plant_date);
        $scope.harvestDate = new Date($scope.plantObj.crop_date);

        $scope.detailPopoverContent =  $scope.seedDate.toISOString().slice(0,10) + ' bis ' + $scope.harvestDate.toISOString().slice(0,10);

        changeRequested = false;

        $scope.setFlags();
    };
    $scope.initTile();

    $rootScope.$on('dateChanged', function (event, dt) {
        $scope.currentDate = dt;
        if ($scope.currentDate >= $scope.harvestDate && $scope.plantState === 'in_progress') {
            $scope.plantState = 'ready_to_harvest';
        }
        //console.log("Dates. Current: ", $scope.currentDate, "  Seed: ", $scope.seedDate);
        $scope.setFlags();
    });
    
    $scope.confirmClicked = function () {
        $scope.plantState = 'scheduled';
        $scope.setFlags();
        //console.log("Dates. Current: ", $scope.currentDate, "  Seed: ", $scope.seedDate);
        // TODO inform backend
    };

    $scope.seedClicked = function () {
        $scope.plantState = 'in_progress';
        $scope.setFlags();
        // TODO inform backend
    };

    $scope.harvestClicked = function () {
        $scope.plantState = 'suggestion';
        $scope.setFlags();
        // TODO inform backend
        // TODO get new suggestion from backend
    };
    
    $scope.changeClicked = function () {
        changeRequested = true;
        $ctrl.open('sm');
    };

    $rootScope.$on('replacementPlant', function (event, plantName) {
        if (changeRequested) {
            var data = {
                location: {
                    x: $scope.posX,
                    y: $scope.posY,
                    z: 0
                },
                plant: plantName
            };
            backendService.updatePlant(data).then(function (res) {
                console.log("Server res: ", res);
                $scope.plantObj = res;
                $scope.initTile();
            });
        }
        changeRequested = false;
    });

    // Modal ----------------------------------------------------

    var $ctrl = this;

    $scope.plants = {};
    var promise = backendService.getPlants();
    promise.then(function (data) {
        $scope.plants = data;
        //console.log("dara: ", data);
        $ctrl.items = $scope.plants.data.plants;
    });


    $ctrl.animationsEnabled = true;

    $ctrl.open = function (size) {
        var modalInstance = $uibModal.open({
            animation: $ctrl.animationsEnabled,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'myModalContent.html',
            controller: 'plantModalCtrl',
            controllerAs: '$ctrl',
            size: size,
            resolve: {
                items: function () {
                    return $ctrl.items;
                }
            }
        });

        modalInstance.result.then(function (selectedItem) {
            $ctrl.selected = selectedItem;
        }, function () {
            console.log('Modal dismissed at: ' + new Date());
        });
    };

});

angular.module('gardenDesigner').controller('plantModalCtrl', function ($uibModalInstance, items, $scope, $rootScope) {
    var $ctrl = this;
    $ctrl.items = items;
    $ctrl.selected = {
        item: $ctrl.items[0]
    };

    $ctrl.ok = function () {
        $rootScope.$emit('replacementPlant',$ctrl.selected.item.name);
        $uibModalInstance.close($ctrl.selected.item);
    };

    $ctrl.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };

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

});