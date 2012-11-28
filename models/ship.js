YUI.add('vorsum-ship-model', function (Y) {

    var E = Y.VorsumEnums;

    Y.VorsumShipModel = Y.Base.create('shipModel', Y.VorsumModel, [], {
        
        sync: Y.LocalStorageSync('ship'),

        initializer: function (config) {
            // tick
            this.on('tick', this.tick, this);
        },

        tick: function () {

        },

    }, {
        ATTRS: {

            base: {
                value: null
            },

            target: {
                value: null
            },

            owner: {
                value: null
            }


        }
    });
});