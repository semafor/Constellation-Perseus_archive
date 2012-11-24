YUI.add('vorsum-planet-model', function (Y) {

    Y.VorsumPlanetModel = Y.Base.create('planetModel', Y.VorsumModel, [], {
        
        sync: Y.LocalStorageSync('planet'),


    }, {
        ATTRS: {
            ownerId: {
                value: null
            },
            name: {
                value: 'Unnamed planet'
            }
        }
    });
});