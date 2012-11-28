/**
One action per type

*/
YUI.add('vorsum-action', function (Y) {

    var E = Y.VorsumEnums;

    Y.VorsumAction = Y.Base.create('action', Y.VorsumController, [], {

        initializer: function (config) {

            if(!config.requestee) {
                throw new Error('Action.initializer: no requestee on action');
            }

            this.setModel(this.getAppropriateModel(config));
        },

        costApplied: function () {
            Y.log('Cost applied', 'note', 'Action.costApplied');
            this.setIsPaidFor();

            // re-request start
            this.requestStart();
        },

        costRefused: function () {
            Y.log('Cost refused (noop)', 'info', 'Action.costRefused');
        },

        getAppropriateModel: function (config) {
            var model;

            if(config.model) {

                switch(config.model.get('type')) {
                    case E.BUILD:
                        model = Y.extend(config.model, Y.VorsumActionBuildModel);
                        break;

                    case E.ATTACK:
                        model = Y.extend(config.model, Y.VorsumActionAttackModel);
                        break;

                    default:
                        model = Y.extend(config.model, Y.VorsumActionModel);
                        break;
                }
                
            } else {

                switch(config.type) {
                    case E.BUILD:
                        model = new Y.VorsumActionBuildModel(config);
                        break;

                    case E.ATTACK:
                        model = new Y.VorsumActionAttackModel(config);
                        break;

                    default:
                        model = new Y.VorsumActionModel(config);
                        break;
                }

            }

            return model;
        },

        requestStart: function () {

            if(!this.getIsPaidFor()) {

                this.applyCostOnRequestee();

            } else {

                this.setStart();

            }
        },

        setStart: function () {
            this.modelSet('started', true).save();
        },

        setStop: function () {
            this.modelSet('started', false).save();
        },

        getIsStarted: function () {
            return this.modelGet('started');
        },

        getIsRunning: function () {
            return this.modelGet('started') && !this.getIsFinished();
        },

        setFinished: function () {

            this.modelSetMany({
                finished: true,
                active: false
            });

            this.transferResultToRequestee();

            this.fire('finished', {
                action: this
            });
        },

        getIsFinished: function () {
            return this.modelGet('finished');
        },

        setIsPaidFor: function () {
            this.modelSet('paid', true);
        },

        getIsPaidFor: function () {
            return this.modelGet('paid');
        },

        tick: function () {



            // move to next action if running and paid for
            if(this.getIsRunning() && this.getIsPaidFor()) {

                this.processStep(this.getCurrentStep(), Y.bind(function (step, ok) {
                    
                    // remove tick on step
                    if(ok) {
                        step.ticks = step.ticks - 1;
                        console.info('processed step', step.name);
                    }

                    // if there's no more ticks left,
                    // go to next step
                    if(step.ticks === 0) {
                        this.setNextStep();
                    }

                }, this));

            }

            // if we're done
            if(!this.getCurrentStep()) {
                console.info('action reporting that it is finished', this);
                this.setStop();
                this.setFinished();
            }

            // save steps
            // fixme, check saves on this model, may be too many
            this.getModel().save();

        },

        processStep: function (step, callback) {
            var ok;
            
            // decide if this step can be done
            ok = true;

            if (!callback) {
                throw new Error('processStep: needs callback');
            }

            callback(step, ok);
        },

        setNextStep: function () {
            var newActionIndex = this.modelGet('stepIndex') + 1;

            this.modelSet('stepIndex', newActionIndex);
        },

        getCurrentStep: function () {
            return this.modelGet('steps')[this.modelGet('stepIndex')];
        },

        getCurrentStepIndex: function () {
            return this.modelGet('stepIndex');
        },

        getNextAction: function () {
            return this.modelGet('steps')[this.modelGet('stepIndex') + 1];
        },

        getCost: function () {
            var order = this.modelGet('order'),
                cost = 0;
            
            // TODO: should be validator on model
            if(order.length === 0) {
                throw new Error('Action.getCost: order length is 0');
            }

            Y.Array.each(order, function (item) {

                // if not supplied, it's free
                if(!cost) {
                    cost = 0;
                }

                cost = cost + item.cost;
            });

            return cost;
        },

        getNumberOfSteps: function () {
            return this.modelGet('steps').length;
        },

        getNumberOfStepsRemaining: function () {
            var ret;

            if(this.getIsFinished()) {
                ret = 0;
            } else if(!this.getIsStarted()) {
                ret = this.getNumberOfSteps();
            } else {
                ret = this.getNumberOfSteps() - this.getCurrentStepIndex();
            }

            return ret;
        },

        addStepToEnd: function (step) {
            this.modelGet('steps').push(step);
            this.modelGet('steps').save();
        },

        addStepToBeginning: function (step) {
            this.modelGet('steps').unshift(step);
            this.modelGet('steps').save();
        },

        addStepAfterIndex: function (step, index) {

            if(!index) {
                throw new Error('addStepToIndex: needs index argument');
            }

            this.modelGet('steps').splice(index, 0, step);
            this.modelGet('steps').save();
        },

        getRequestee: function () {
            return this.modelGet('requestee');
        },

        // returns the ENUM for what's being built
        getResult: function () {
            return Y.Array.map(this.modelGet('order'), function (item) {
                return item.name;
            });
        },

        transferResultToRequestee: function () {
            Y.log('transferring', 'note', 'Action.transferResultToRequestee');
            this.fire('transferResultToRequestee', {
                requestee: this.getRequestee(),
                result: this.getResult()
            });
        },

        applyCostOnRequestee: function () {

            if(this.getIsPaidFor()) {
                throw new Error('Action.applyCostOnRequestee: attempted to re-apply cost.');
            }
            
            this.fire('tryApplyCost', {
                requestee: this.getRequestee(),
                cost: this.getCost()
            });

            Y.log('fired tryApplyCost', 'note', 'Action.applyCostOnRequestee');
        }

    }, {
        ATTRS: {

        }
    });


    Y.VorsumActionAttack = function () {
        VorsumActionAttack.superclass.constructor.apply(this, arguments);

    };
    Y.extend(Y.VorsumActionAttack, Y.VorsumAction, {

        processStep: function (action, callback) {

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

            var attackers = this.modelGet('attackingForce'),
                defenders = this.modelGet('defendingForce'),
                returnLength = this.modelGet('steps')[0].ticks;

            if(attackers.length > defenders.length ) {

                this.addStepToEnd({
                    name: RETURN,
                    ticks: returnLength
                });

                this.modelSet('outcome', VICTORY);

            } else if ( attackers.length === defenders.length ) {

                this.addStepToEnd({
                    name: RETREAT,
                    ticks: returnLength + this.modelGet('retreatPenalty')
                });

                this.modelSet('outcome', DEFEAT);

            } else if ( attackers.length < defenders.length ) {

                this.modelSet('outcome', DEAD);

            }

        },


    });

});