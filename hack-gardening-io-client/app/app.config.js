'use strict';

angular.
  module('gardenIOapp').
  config(['$locationProvider' ,'$routeProvider',
    function config($locationProvider, $routeProvider) {
      $locationProvider.hashPrefix('!');

      $routeProvider.
        when('/garden', {
          template: '<garden-designer></garden-designer>'
        }).
        //when('/phones/:phoneId', {
        //  template: '<phone-detail></phone-detail>'
        //}).
        otherwise('/garden');
    }
  ]);
