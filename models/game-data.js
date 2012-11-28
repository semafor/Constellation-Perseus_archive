YUI.add('vorsum-game-data', function (Y) {

    Y.VorsumGameData = Y.Base.create('gameData', Y.Model, [], {
        
        sync: Y.LocalStorageSync('game'),

        start: function () {
            // start ticker
            this.flow = window.setInterval(Y.bind(this.tick, this), this.get('dayLength'));

            return this;
        },

        tick: function () {
            this.set('ticker', this.get('ticker') + 1).save();
            
            //Y.log(this.get('ticker'), 'note', 'GameData.tick');
            
            this.fire('tick');
        },

        getRawTime: function () {
            return this.get('ticker');
        },

        getDays: function () {
            return this.get('ticker') / this.get('dayModifiers');
        },

        getSuns: function () {
            return this.get('ticker') / this.get('sunModifier');
        },

        getGalxes: function () {
            return this.get('ticker') / this.get('galaxModifier');
        }
    }, {
        ATTRS: {
            genesis: {
                value: 0
            },
            dayModifiers: {
                value: 1
            },
            sunModifier: {
                value: 100
            },
            galaxModifier: {
                value: 1000000
            },
            dayLength: {
                value: 10000
            },
            ticker: {
                value: 0
            }
        }
    });
});