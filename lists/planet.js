YUI.add('vorsum-planet-list', function (Y) {

    Y.VorsumPlanetList = Y.Base.create('planetList', Y.VorsumList, [], {
        
        model: Y.VorsumPlanetModel,

        sync: Y.LocalStorageSync('planet'),

        initializer: function () {
            
            // on load
            this.load(Y.bind(this.createPlanetsFromRecords, this));
        },

        createPlanetsFromRecords: function (err, res) {

            if(err) {
                throw new Error('createPlanetsFromRecords: failed to fetch planets, reason: ' + err);
            } else {
                Y.log('Got ' + res.length + ' planets', 'info', 'VorsumPlayerList.createPlanetsFromRecords');
            }

            this.setInstances(this.map(function (item) {
                return new Y.VorsumPlanet({
                    model: item
                });
            }));

        },

    });
});