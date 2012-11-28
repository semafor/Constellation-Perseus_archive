YUI.add('vorsum-enums', function (Y) {
    
    Y.VorsumEnums = {

        // types enums
        ATTACK :                'ATTACK',
        BUILD :                 'BUILD',
        DEFAULT :               'DEFAULT',

        // generic
        UNFINISHED :            'UNFINISHED',
    
        // build enums
        ORDERED :               'ORDERED',
        BUILDING :              'BUILDING',
        ASSEMBLING :            'ASSEMBLING',
        TESTING :               'TESTING',
        INSTALLING :            'INSTALLING',
        BRANDING :              'BRANDING',
        SHIPPING :              'SHIPPING',
        PROVISIONING :          'PROVISIONING', // putting the built thing to use
    
        // attack enums
        ENROUTE :               'ENROUTE', // on the way
        SIEGE :                 'SIEGE', // establishing perimiter, strategic planning etc
        BATTLE :                'BATTLE',
        RETREAT :               'RETREAT', // defeat
        RETURN :                'RETURN', //  victory
        DEFECTED :              'DEFECTED', // lost force to enemy
        DEAD :                  'DEAD',
    
        // ship statuses
        ATBASE:                 'ATBASE',
        ATTACKING:              'ATTACKING',
        DEFENDING:              'DEFENDING',
        DESTROYED:              'DESTROYED',
        DEPRECATED:             'DEPRECATED',
        DAMAGED:                'DAMAGED',
        REPAIRING:              'REPAIRING',
        ONFIRE:                 'ONFIRE',
        POWERLESS:              'POWERLESS',
        UNMANNED:               'UNMANNED',
    
        // ship definitions
        SHIP_SCOUT: {
            name:               'SHIP_SCOUT',
            cost:               1000,
            travel:             3,
            minParticipation:   0
        },
        SHIP_PATROL: {
            name:               'SHIP_PATROL',
            cost:               1500,
            travel:             5,
            minParticipation:   0
        },
        SHIP_CRUISER: {
            name:               'SHIP_CRUISER',
            cost:               2500,
            travel:             6,
            minParticipation:   5000
        },
        SHIP_DESTROYER: {
            name:               'SHIP_DESTROYER',
            cost:               5500,
            travel:             8,
            minParticipation:   10000
        },
        SHIP_DREADNAUGHT: {
            name:               'SHIP_DREADNAUGHT',
            cost:               8000,
            travel:             12,
            minParticipation:   20000
        }

    };
});