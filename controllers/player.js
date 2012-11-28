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
        },

        recieveResultsFromAction: function (result) {
            console.info('got results from action', result);
        }


    }, {
        ATTRS: {

        }
    });
});