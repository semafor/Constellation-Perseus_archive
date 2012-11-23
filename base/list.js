YUI.add('vorsum-list', function (Y) {

    Y.VorsumList = Y.Base.create('list', Y.ModelList, [], {

        instances: [],

        initializer: function () {

            this.on('tick', this.distributeTick, this);

        },

        distributeTick: function () {
            Y.Array.each(this.getActiveInstances(), function (instance) {
                instance.fire('tick');
            });
        },
        getAllModels: function () {
            return this.toArray();
        },

        getAllInstances: function () {
            return this.instances;
        },

        addInstance: function (instance) {
            this.add(instance.getModel());
            this.instances.push(instance);
        },

        removeInstance: function(instance) {
            // remove controller instance
            this.setInstance(Y.Array.reject(this.getAllInstances(), function (r) {
                return r.getId() === instance.getId();
            }));

            // remove model
            this.remove(instance.getModel());
        },

        setInstances: function (newInstances) {
            this.instances = newInstances;
        },

        getActiveInstances: function () {
            return Y.Array.filter(this.getAllInstances(), function (instance) {
                return instance.getIsActive();
            });
        }


    });
});