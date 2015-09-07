/**
 * Created by Jeezy on 06.09.2015.
 */
var myApp = angular.module('myApp', []).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

//Контроллер для логин-формы
myApp.controller('loginCtrl', function ($scope) {
    //
});

//Контроллер для категорий
myApp.controller('categoryCtrl', function ($scope, $http) {
    $scope.cat = {'parent' :'Машины','sub':'BMW,Lexus,ВАЗ'};
    $scope.categories = [];
    $scope.empty = true;
    $scope.clear_not = false;
    $scope.addCategory = function () {

        if($scope.cat.sub !== undefined){
            var sub_str = $scope.cat.sub.toString();
            $scope.cat.sub = sub_str.split(',');
        }

        $scope.categories.push($scope.cat);
        $scope.cat = {};
        $scope.empty = false;

    };

    $scope.clear = function () {

        $scope.categories = [];
        $scope.empty = true;
        $scope.cat = {'parent' :'Города','sub':'Киев,Львов,Запорожье'};
        $scope.clear_not = true;

    };

});


myApp.controller('registrationCtrl', function ($scope) {
    //
});