YUI.add('vorsum-planet', function (Y) {
    
    Y.VorsumPlanet = Y.Base.create('planet', Y.VorsumController, [], {

        initializer: function (config) {

            if(config) {
                if(config.model) {
                    this.setModel(config.model);
                } else {
                    this.setModel(new Y.VorsumPlanetModel(config));
                }
            }

            this.getModel().addTarget(this);
        },

        tick: function () {

             //Y.log(this.getPubliclyAnnouncedInformation(), 'note', '');

            this.increaseAge();
            this.increaseParticipation();

            // gain currency
            this.increaseCurrency();

        },

        increaseCurrency: function () {
            var gain = this.modelGet('currency') + this.modelGet('currencyGainPerTick') * this.modelGet('currencyBonusModifier');
            this.modelSet('currency', gain);
        },

        currencySubtract: function (decrease) {
            this.modelSet('currency', this.modelGet('currency') - decrease);
        },

        getPubliclyAnnouncedInformation: function () {
            var age = this.modelGet('age'),
                adjective = (function () {
                    var ret;

                    if(age < 10) {
                        ret = 'a newly created';
                    } else if (age >= 10 && age < 99) {
                        ret = 'a young';
                    } else if (age >= 100 && age < 999) {
                        ret = 'a mature';
                    } else if (age > 1000) {
                        ret = 'an old';
                    }

                    return ret;
                })(),
                status = this.modelGet('active') ? 'active' : 'inactive';
            
            return 'Planet ' + this.modelGet('name') + ' is a ' + adjective + ', ' + status + ' planet';
        }

    }, {
        ATTRS: {

        }
    });
});