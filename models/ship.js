YUI.add('vorsum-ship-model', function (Y) {

    var ENUMS = {
        ENROUTE: 'ENROUTE',
        RETURNING: 'RETURNING',
        ATBASE: 'ATBASE',
        ATTACKING: 'ATTACKING',
        DEFENDING: 'DEFENDING',
        DESTROYED: 'DESTROYED',
        DEPRECATED: 'DEPRECATED',
        DAMAGED: 'DAMAGED',
        REPAIRING: 'REPAIRING',
        ONFIRE: 'ONFIRE',
        POWERLESS: 'POWERLESS',
        UNMANNED: 'UNMANNED'
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
});