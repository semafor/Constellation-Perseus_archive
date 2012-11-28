YUI.add('vorsum-list', function (Y) {

    Y.VorsumList = Y.Base.create('list', Y.ModelList, [], {

        instances: [],

        initializer: function () {

            this.on('tick', this.distributeTick, this);

            this.on('applyCost', function () {
                console.info('list received applyCost');
            })

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
            var model = instance.getModel();

            if(!model.get('id')) {
                model.save();
            }

            // register model
            this.add(model);

            // register controller instance
            instance.id = model.get('id');
            this.instances.push(instance);

            if(!instance.id) {
                throw new Error('List.addInstance: instance lacks id');
            }
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
        },

        getInstanceById: function (id) {
            var res = Y.Array.find(this.instances, function (item) {
                return item.id === id;
            });
            if(!res) {
                throw new Error('List.getInstanceById: failed to find instance with id '+id);
            }
            return res;
        }


    });
});