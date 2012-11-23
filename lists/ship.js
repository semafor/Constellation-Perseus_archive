YUI.add('vorsum-ship-list', function (Y) {

    Y.VorsumShipList = Y.Base.create('shipList', Y.ModelList, [], {
        
        model: Y.VorsumShipModel,

        sync: Y.LocalStorageSync('ship'),

        initializer: function () {
            this.on('tick', this.distributeTick, this);
        },

        distributeTick: function () {
            this.each(function (ship) {

                ship.fire('tick');

                Y.log('updated tick on ship', 'note', 'ShipList.distributeTick');
            });
        },

        getAll: function () {
            return this.toArray();
        },

        getByOwner: function (ownerId) {
            return this.filter(function (ship) {
                return ship.get('owner').getId() === ownerId;
            });
        }
    });
});