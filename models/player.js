YUI.add('vorsum-player-model', function (Y) {

    Y.VorsumPlayerModel = Y.Base.create('playerModel', Y.VorsumModel, [], {
        sync: Y.LocalStorageSync('player'),

        initializer: function (config) {
            
        }

    }, {
        ATTRS: {
            assumedPlanets: {
                value: []
            },
            name: {
                value: 'Unnamed player'
            }
        }
    });
});