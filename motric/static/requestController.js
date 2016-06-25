var mo_request = angular.module('requestPage', []);

mo_request.filter('parsehtml', function($sce) {
	return $sce.trustAsHtml;
});

mo_request.controller('requestCtrl', function($scope) {
  $scope.instruction = "Please use this form to request your dedicated device from Mobile Harness Beijing central lab. We will charge the cost of the device (and  <b> device only </b>) at end of each month to your cost center.  For current device parchasing unit price, please refer to <b><a href='http://go/moha-quotation' target='_blank'>go/moha-quotation</a></b>. If your device is not listed, we can send quotation to you before we order the device. Requesting devices from central lab will get lab admin and maintenance for free. <br><br>You can also request lab ops help by <b><a href='http://go/mh-labops-request' target='_blank'>go/mh-labops-request</a></b>.";

  $scope.test = function() {
    // $scope.ison = Date();
    // $scope.ison = angular.toJson($scope.ison, true); // wrong usage -- toJson is used to transform json object to json string. 
    $scope.data = getFormData();
    // $scope.data = angular.toJSON($scope.data, 50);  // incorrect expression.
  }

});