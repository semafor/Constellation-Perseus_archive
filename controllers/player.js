YUI.add('vorsum-player', function (Y) {
    
    Y.VorsumPlayer = Y.Base.create('player', Y.VorsumController, [], {

        initializer: function (config) {

            if(config) {
                if(config.model) {
                    this.setModel(config.model);
                } else {
                    this.setModel(new Y.VorsumPlayerModel(config));
                }
            }

            this.getModel().addTarget(this);
        },

        settlePlanet: function () {

        },

        leavePlanet: function () {

        },

        requestAttack: function (planet, force) {
            this.fire('requestAttack', {
                planet: planet,
                force: force
            });
            console.info('requested attack');
        },

        executeAttack: function (e) {
            console.info('player: attack allowed', e);
        },

        abortAttack: function (e) {
            console.info('player: attack disallowed', e);
        },

        // tick related functions

        tick: function () {

            //Y.log(this.getPubliclyAnnouncedInformation(), 'note', '');

            this.increaseAge();
            this.increaseParticipation();

            // gain currency
            this.increaseCurrency();
        },

        getPubliclyAnnouncedInformation: function () {
            var status = this.modelGet('active') ? 'active' : 'inactive';
            return this.modelGet('name') + ' is an ' + status + ' player';
        }


    }, {
        ATTRS: {

        }
    });
});