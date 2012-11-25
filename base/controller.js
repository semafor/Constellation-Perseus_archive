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


        applyCost: function (e) {
            var currentCurrency = this.modelGet('currency'),
                cost = e.cost,
                callback = e.callback,
                applied = false;

            if( ( currentCurrency - cost ) < 0 ) {
                Y.log('Not enough currency to do transaction', 'warn', 'Controller.applyCost');
            } else {
                Y.log('Enough currency to do transaction', 'info', 'Controller.applyCost');
                this.modelSet('currency', currentCurrency - cost);
                applied = true;
            }

            callback(applied);
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