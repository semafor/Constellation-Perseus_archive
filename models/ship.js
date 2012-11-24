YUI.add('vorsum-ship-model', function (Y) {

    var ENUMS = {

    };

    Y.VorsumShipModel = Y.Base.create('shipModel', Y.VorsumModel, [], {
        
        sync: Y.LocalStorageSync('ship'),

        initializer: function (config) {
            // tick
            this.on('tick', this.tick, this);
        },

        tick: function () {

        },

        getStatus: function () {

        },

        setStatus: function (val) {
            console.info(this, val);
        },

        getOwner: function () {
            return this.get('owner');
        },

        setOwner: function (ownerId) {
            this.set('owner', ownerId);
        },

    }, {
        ATTRS: {
            
            status: {
                value: [],
                getter: 'getStatus',
                setter: 'setStatus'
            },
            
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
}, '0.0.1', {
    use: [
        'vorsum-enums'
    ]
});