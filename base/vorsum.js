YUI.add('vorsum', function (Y) {

}, '0.0.1', {
    requires: [
        'app',
        'localstorage-sync',

        // vorsum core
        'vorsum-controller',
        'vorsum-model',
        'vorsum-list',

        // game core
        'vorsum-game',
        'vorsum-game-data',
        
        // player
        'vorsum-player',
        'vorsum-player-model',
        'vorsum-player-list',

        // planet
        'vorsum-planet',
        'vorsum-planet-model',
        'vorsum-planet-list',

        // ship
        'vorsum-ship-model',
        'vorsum-ship-list',

        // actions
        'vorsum-action',
        'vorsum-action-models',
        'vorsum-action-list'
    ]
});