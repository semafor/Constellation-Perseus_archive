YUI.add('vorsum-model', function (Y) {

    Y.VorsumModel = Y.Base.create('model', Y.Model, [], {

        initializer: function () {
            //this.after('change', this.afterChange, this);
        },

        afterChange: function () {
            //Y.log('Model ' + this.get('name') + ' (' + this.get('id') + ') changed.' , 'note', 'Model.afterChange');
        }

    }, {
        ATTRS: {
            active: {
                value: true
            },
            name: {
                value: 'Unnamed'
            },
            ticksParticipation: {
                value: 0
            },
            age: {
                value: 0
            }
        }
    });
});