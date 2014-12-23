(function(angular) {
  'use strict';

var myApp = angular.module('a1', ['ngResource']);

myApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

myApp.controller('c1', ['$scope', '$resource', '$timeout',function($scope, $resource, $timeout) {
	$scope.text = {
		title: 'Динамическая схема',
		tlist: 'Список таблиц',
		tcurr: 'Текущая таблица:',
		no: '№',
		notable: 'Не выбрана',
	};
	$scope.model = {
		shinfo: {},
		active: NaN,
		rows: {},
		edit:{},
		format: 'yyyy-MM-dd',
		dateopt:{
			
		},
	};
  var Sh = $resource('/api/list',{}, {
	  read: {method:'GET'}
	});
	var Rows = $resource('/api/rows/:model/:pk', {model: '@model', pk: '@pk'}, {
	  read: {
	  	method: 'GET', isArray:true
	  },
	  write: {
	  	method: 'POST'
	  },
	});
  $scope.model.shinfo = Sh.read();
  $scope.selSh = function (key) {
    $scope.model.active = key;
		$scope.model.shinfo[key].fc = $scope.model.shinfo[key].fields.length;
    $scope.model.rows[key] = Rows.read({'model':key});    
  };
  $scope.selRow = function (key) {
    $scope.model.arow = key;
  };
  $scope.editRow = function (key,field,value) {
  	$scope.selRow(key);
  	$scope.model.edit = {
  		model: $scope.model.active,
  		key: key,
  		tip: field.type,
  		col: field.id,
  		value: value,
  	};  	
  	if ($scope.model.edit.tip=='date'){
  		$scope.model.edit.d = new Date($scope.model.edit.value[$scope.model.edit.col]+'T00:00:00');
  	}
  };
  $scope.imEdit = function (key, field) {
    return key==$scope.model.edit.key && field.id ==$scope.model.edit.col;
  };
  $scope.open = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.opened = true;
  };
  $scope.addRow = function(key){
  	Rows.write({model: key});
  };  	
  $scope.updRow = function(doc){
  	if ($scope.model.edit.tip=='date'){
  		$scope.model.edit.value[$scope.model.edit.col] = $scope.model.edit.d.toISOString().substr(0,10);
  	}  	
  	if ($scope.stime){
  		$timeout.cancel($scope.stime);
  	};
  	$scope.model.sdoc = doc;
  	$scope.stime = $timeout(function () {Rows.write($scope.model.sdoc);}, 600);
  };	  
}]);

})(window.angular);