/**
A action is the following workflow:

    * players/planets/ships/fleets makes a request for a action
    * the request is intepreted and ruled upon by the game. If action is opened
    * the action's actions are then set in motion
    * actions in the action notifies the involved parties
    * action closed

If the game request a action, it's automatically approved

Case estimated times are no guarantees

Example action:

    * Player A requests an attack on Planet B with 100 ships
    * The game approves the attack
    * Player A sends 100 ships towards Planet B
    * At some point is Planet B notified
    * 100 ships attack Planet B
    * The first waves of attack gives Player A heavy losses
    * 30 ships are recalled by Player A
    * 30 ships return to Base
    * Case closed, filed.

**/
YUI.add('vorsum-action-models', function (Y) {

    var E = Y.VorsumEnums;

    Y.VorsumActionModel = Y.Base.create('actionModel', Y.Model, [], {

        actionType: E.DEFAULT,

        sync: Y.LocalStorageSync('actions'),


    }, {
        ATTRS: {
            actions: {
                value: []
            },
            actionIndex: {
                value: 0
            },
            started: {
                value: false
            },
            finished: {
                value: false
            },
            cost: {
                value: 0
            },
            requestee: {
                value: null
            },
            goal: {
                value: null
            }
        }
    });

    // base build model
    Y.VorsumActionBuildModel = function () {
        VorsumActionBuildModel.superclass.constructor.apply(this, arguments);
    };
    Y.VorsumActionBuildModel.ATTRS = {
        actions: {
            value: [

                {
                    name: E.ORDERED,
                    ticks: 1
                },

                {
                    name: E.BUILDING,
                    ticks: 3
                },

                {
                    name: E.ASSEMBLING,
                    ticks: 1
                },

                {
                    name: E.INSTALLING,
                    ticks: 1
                },

                {
                    name: E.TESTING,
                    ticks: 1
                },

                {
                    name: E.BRANDING,
                    ticks: 1
                },

                {
                    name: E.SHIPPING,
                    ticks: 1
                },

                {
                    name: E.PROVISIONING,
                    ticks: 1
                }

            ]
        }
    };

    Y.extend(Y.VorsumActionBuildModel, Y.VorsumActionModel, {
        actionType: E.BUILD
    });

    // base attack model
    Y.VorsumActionAttackModel = function () {
        VorsumActionAttackModel.superclass.constructor.apply(this, arguments);
    };
    Y.VorsumActionAttackModel.ATTRS = {
        actions: {
            value: [

                {
                    name: E.ENROUTE,
                    ticks: 6
                },

                {
                    name: E.SIEGE,
                    ticks: 1
                },

                {
                    name: E.BATTLE,
                    ticks: 1
                }

            ]
        },
        
        attackingForce: {
            value: null
        },

        defendingForce: {
            value: null
        },

        outcome: {
            value: E.UNFINISHED
        },

        retreatPenalty: {
            value: 2 // how much longer the return will take if defeated
        }
    };

    Y.extend(Y.VorsumActionAttackModel, Y.VorsumActionModel, {

        actionType: E.ATTACK


    });

}, '0.0.1', {
    use: [
        'vorsum-enums'
    ]
});