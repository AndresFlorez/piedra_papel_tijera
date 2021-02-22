var chatApp = angular.module('chatApp', ['ngCookies', 'Alertify']);
chatApp.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

chatApp.run(function ($http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.get('csrftoken');
});

chatApp.controller('main_app_controller', function ($scope) {
    //
});

chatApp.controller('game_controller', function ($scope, $http, Alertify, $q) {
    $scope.user_active = {};
    $scope.current_user_id = null;
    $scope.entities_list = [];
    $scope.ranking_users = [];

    $scope.challenge = function(user){
        
        $http({
            url: '/api/1/game/challenge/',
            method: "POST",
            data: user.game,
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            transformRequest: function(obj) {
                var str=[];
                for(var p in obj){
                    str.push(encodeURIComponent(p) + "=" + obj[p])
                }
                return str.join("&"); 
            },
        }).then(function (response) {
            if(response.data.status && response.data.winner==$scope.current_user_id){
                Alertify.success('Has ganado');
                user.game = {};
            } else if (response.data.status && response.data.winner!=$scope.current_user_id){
                Alertify.error('Has perdido');
                user.game = {};
            } else {
                user.game = response.data;
            }
        }, function errorCallback(response) {
        });
    };

    $scope.get_game = function(user){
        $http({
            url: '/api/1/game/get_match/',
            method: "POST",
            data: {
                'user_id': user.id
            },
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            transformRequest: function(obj) {
                var str=[];
                for(var p in obj){
                    str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]))
                }
                return str.join("&"); 
            },
        }).then(function (response) {
            user.game = response.data;
            if (user.game.player_1 == $scope.current_user_id) Alertify.success('Ya has retado a este usuario');
            else Alertify.success('Este usuario te ha retado');
            $scope.user_active = user;
        }, function errorCallback(response) {
            user.game = {};
            $scope.user_active = user;
        });
    };

    $scope.select_entity = function(user, entity){
        if(user.game.id && $scope.current_user_id == user.game.player_1){
            Alertify.error('No puede modificar su elección');
            return
        }
        if(! (user.game.entity_1 && user.game.player_1) || ( user.game.player_1 == $scope.current_user_id ) ) {
            user.game.entity_1 = entity.id;
            user.game.player_1 = $scope.current_user_id;
            user.game.player_2 = user.id;
        } else {
            user.game.entity_2 = entity.id;
            user.game.player_2 = $scope.current_user_id;
        }
    };

    $scope.load_data = function(url, scope_var, concat=false) {
        if(!url) return;
        $scope['loading_' + scope_var] = true;
        $http({
            url: url,
            method: "GET",
            data: {},
            headers: {'Content-Type': 'application/json'},
        }).then(function (response) {
            if(concat){
                $scope[scope_var] = $scope[scope_var].concat(response.data.results);
            } else {
                $scope[scope_var] = response.data.results;
            }
            $scope['next_' + scope_var] = response.data.next;
            $scope['previous_' + scope_var] = response.data.previous;
            $scope['loading_' + scope_var] = false;
        }, function errorCallback(response) {
            $scope['loading_' + scope_var] = false;
        });
    }
    
    angular.element(document).ready(function () {
        // setInterval($scope.load_data, 20000, '/api/1/auth_user/', 'users_list');
        $scope.load_data('/api/1/auth_user/', 'users_list');
        $scope.load_data('/api/1/game/', 'entities_list');
        $scope.load_data('/api/1/ranking/', 'ranking_users');
    });
});
