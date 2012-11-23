YUI.add('vorsum-controller', function (Y) {
    
    Y.VorsumController = Y.Base.create('controller', Y.Base, [], {

        initializer: function () {

            this.on('*:tick', this.tick, this);

        },

        setModel: function (model) {
            this.model = model;
        },

        getModel: function () {
            return this.model;
        },

        modelGet: function (what) {
            return this.getModel().get(what);
        },

        modelSet: function (what, value) {
            return this.getModel().set(what, value).save();
        },

        getIsActive: function () {
            return this.modelGet('active');
        },

        getId: function () {
            return this.modelGet('id');
        },

        increaseAge: function () {
            this.modelSet('age', this.modelGet('age') + 1);
        },

        increaseParticipation: function () {
            this.modelSet('ticksParticipation', this.modelGet('ticksParticipation') + 1);
        },

        tick: function () {
            Y.log(this.getPubliclyAnnouncedInformation(), 'note', '');
        },



    }, {
        ATTRS: {
            model: {
                value: null
            }
        }
    });
});