YUI.add('vorsum-action-list', function (Y) {

    Y.VorsumActionList = Y.Base.create('actionList', Y.VorsumList, [], {
        
        model: Y.VorsumActionModel,

        sync: Y.LocalStorageSync('actions'),

        initializer: function () {

            this.model = Y.VorsumActionModel;

            this.load(Y.bind(this.createActionsFromRecords, this));
        },

        createActionsFromRecords: function (err, res) {

            if(err) {
                throw new Error('createActionsFromRecords: failed to fetch actions, reason: ' + err);
            } else {
                Y.log('Got ' + res.length + ' actions', 'info', 'VorsumActionList.createActionsFromRecords');
            }

            this.setInstances(this.map(function (item) {
                return new Y.VorsumAction({
                    model: item
                });
            }));
        },

        getAllStartedInstances: function () {
            return Y.Array.filter(this.getAllInstances(), function (instance) {
                return instance.getIsStarted();
            });
        },

        // active are started ones, not just active
        getActiveInstances: function () {
            return this.getAllStartedInstances();
        }


    });
});