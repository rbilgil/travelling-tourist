/**
 * Created by robin on 07/05/15.
 */
var app = angular.module('app', ['autocomplete']).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});;