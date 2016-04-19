//main js file, initilized the app to be used on all sub-pages
//NOTE that we use angular without the routing

var app = angular.module('wbc', ['checklist-model', 'ngAnimate']);

app.config(['$httpProvider', '$interpolateProvider', '$locationProvider', function($httpProvider, $interpolateProvider, $locationProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
}]);

app.controller('DefaultController', function() {
});


// load the modal and redirection hhandle for subscribe button
$(document).ready(function(){
    loadModal('#modal', '.modal-button')

    $('.subscribe-button').on('click', function(){
        $.get($(this).data('url'), function(data) {
            if (data.redirect){
                window.location.href = data.redirect;
                window.location.reload();
            }
        });
    })
}); 