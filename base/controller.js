YUI.add('vorsum-controller', function (Y) {
    
    Y.VorsumController = Y.Base.create('controller', Y.Base, [], {

        initializer: function () {

            this.on('*:tick', this.tick, this);

        },

        setModel: function (model) {
            this.model = model;

            // let model talk to controller
            model.addTarget(this);
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

        increaseCurrency: function () {
            var gain = this.modelGet('currency') + this.modelGet('currencyGainPerTick') * this.modelGet('currencyBonusModifier');
            this.modelSet('currency', gain);
        },

        decreaseCurrency: function (decrease) {
            this.modelSet('currency', this.modelGet('currency') - decrease);
        },

        getCanAfford: function (amount) {
            if( !( !isNaN(parseFloat(n)) && isFinite(n) ) ) {
                throw new Error('Controller.getCanAfford: NaN');
            }
            
            return parseInt(this.modelGet('currency'), 10) - amount) >= 0;
        },

        tick: function () {
            Y.log(this.getPubliclyAnnouncedInformation(), 'note', '');
        }



    }, {
        ATTRS: {
            model: {
                value: null
            }
        }
    });
});