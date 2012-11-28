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

    Y.VorsumActionModel = Y.Base.create('actionModel', Y.VorsumModel, [], {

        sync: Y.LocalStorageSync('actions'),


    }, {
        ATTRS: {
            type: {
                value: E.DEFAULT
            },

            // stuff to do to complete this action
            steps: {
                value: []
            },

            // at what step are we
            stepIndex: {
                value: 0
            },
            started: {
                value: false
            },
            finished: {
                value: false
            },

            // whether or not it is payed for
            paid: {
                value: false
            },

            // who requested action
            requestee: {
                value: null
            },

            /**
            items ordered
            should be an array of things to build

            [
                {
                    name: ENUM,
                    cost: 1000,
                    minParticipation: 1000
                }
            ]

            **/
            order: {
                value: []
            }
        }
    });

    // base build model
    Y.VorsumActionBuildModel = Y.Base.create('actionBuildModel', Y.VorsumActionModel, [], {
    

    }, {
        ATTRS: {
            type: {
                value: E.BUILD
            },
            steps: {
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
            },
            cost: {
                value: 1000 // for now
            }
        }
    });

    // base attack model
    Y.VorsumActionAttackModel = Y.Base.create('actionAttackModel', Y.VorsumActionModel, [], {

    }, {
        ATTRS: {
            type: {
                value: E.ATTACK
            },
            steps: {
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
        }
    });

});