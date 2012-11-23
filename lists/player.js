YUI.add('vorsum-player-list', function (Y) {

    Y.VorsumPlayerList = Y.Base.create('playerList', Y.VorsumList, [], {

        model: Y.VorsumPlayerModel,

        sync: Y.LocalStorageSync('player'),

        initializer: function () {

            // on load
            this.load(Y.bind(this.createPlayersFromRecords, this));
        },

        createPlayersFromRecords: function (err, res) {

            if(err) {
                throw new Error('createPlayersFromRecords: failed to fetch players, reason: ' + err);
            } else {
                Y.log('Got ' + res.length + ' players', 'info', 'VorsumPlayerList.createPlayersFromRecords');
            }

            this.setInstances(this.map(function (item) {
                return new Y.VorsumPlayer({
                    model: item
                });
            }));
        },

        // aliases
        removePlayer: function (ref) {
            this.removeInstance(player);
        },
        addPlayer: function (player) {
            this.addInstance(player);
        },



    });
});