/**
One action per type

*/
YUI.add('vorsum-action', function (Y) {
    
    Y.VorsumAction = Y.Base.create('action', Y.VorsumController, [], {

        initializer: function (config) {

            // tock
            this.on('tock', this.tock, this);
        },

        setStart: function () {
            this.set('started', true).save();
        },

        setStop: function () {
            this.set('started', false).save();
        },

        getIsStarted: function () {
            return this.get('started');
        },

        getIsRunning: function () {
            return this.get('started') && !this.getIsFinished();
        },

        setFinished: function () {
            this.set('finished', true).save();
            this.fire('finished', {
                action: this
            });
        },

        getIsFinished: function () {
            return this.get('finished');
        },

        tick: function () {

            // move to next action
            if(this.getIsRunning()) {

                this.processAction(this.getCurrentAction(), function () {
                    // go to next action
                    this.setNextAction();
                });

            }

        },

        processAction: function (action, callback) {

            if (callback) {
                callback();
            }
        },

        setNextAction: function () {
            var newActionIndex = this.get('actionIndex') + 1;

            if(!this.get('actions')[newActionIndex]) {
                this.finished();
            } else {
                this.set('actionIndex', newActionIndex);
            }

        },

        getCurrentAction: function () {
            return this.get('actions')[this.get('actionIndex')];
        },

        getCurrentActionIndex: function () {
            return this.get('actionIndex');
        },

        getNextAction: function () {
            return this.get('actions')[this.get('actionIndex') + 1];
        },

        setCost: function (n) {
            this.set('cost', n);
        },

        getCost: function () {
            return this.get('cost');
        },

        getNumberOfSteps: function () {
            return this.get('actions').length;
        },

        getNumberOfStepsRemaining: function () {
            var ret;

            if(this.getIsFinished()) {
                ret = 0;
            } else if(!this.getIsStarted()) {
                ret = this.getNumberOfSteps();
            } else {
                ret = this.getNumberOfSteps() - this.getCurrentActionIndex();
            }

            return ret;
        },

        addStepToEnd: function (action) {
            this.get('actions').push(action);
            this.get('actions').save();
        },

        addStepToBeginning: function (action) {
            this.get('actions').unshift(action);
            this.get('actions').save();
        },

        addStepAfterIndex: function (action, index) {

            if(!index) {
                throw new Error('addStepToIndex: needs index argument');
            }

            this.get('actions').splice(index, 0, action);
            this.get('actions').save();
        }

    }, {
        ATTRS: {

        }
    });


    Y.VorsumActionAttack = function () {
        VorsumActionAttack.superclass.constructor.apply(this, arguments);

    };
    Y.extend(Y.VorsumActionAttack, Y.VorsumAction, {

        processAction: function (action, callback) {

            switch(action.name) {

                case BATTLE:
                    this.processAttack(this);
                    break;

                case RETURN:
                case RETREAT:
                    break;
            }

            if(callback) {
                callback();
            }

        },

        processAttack: function () {

            var attackers = this.get('attackingForce'),
                defenders = this.get('defendingForce'),
                returnLength = this.get('actions')[0].ticks;

            if(attackers.length > defenders.length ) {

                this.addStepToEnd({
                    name: RETURN,
                    ticks: returnLength
                });

                this.set('outcome', VICTORY);

            } else if ( attackers.length === defenders.length ) {

                this.addStepToEnd({
                    name: RETREAT,
                    ticks: returnLength + this.get('retreatPenalty')
                });

                this.set('outcome', DEFEAT);

            } else if ( attackers.length < defenders.length ) {

                this.set('outcome', DEAD);

            }

        },


    });

});