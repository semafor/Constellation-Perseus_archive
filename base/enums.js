YUI.add('vorsum-enums', function (Y) {
    
    Y.VorsumEnums = {

        // types enums
        ATTACK :            'ATTACK',
        BUILD :             'BUILD',
        DEFAULT :           'DEFAULT',

        // generic
        UNFINISHED :        'UNFINISHED',

        // build enums
        ORDERED :           'ORDERED',
        BUILDING :          'BUILDING',
        ASSEMBLING :        'ASSEMBLING',
        TESTING :           'TESTING',
        INSTALLING :        'INSTALLING',
        BRANDING :          'BRANDING',
        SHIPPING :          'SHIPPING',
        PROVISIONING :      'PROVISIONING', // putting the built thing to use

        // attack enums
        ENROUTE :           'ENROUTE', // on the way
        SIEGE :             'SIEGE', // establishing perimiter, strategic planning etc
        BATTLE :            'BATTLE',
        RETREAT :           'RETREAT', // defeat
        RETURN :            'RETURN', //  victory
        DEFECTED :          'DEFECTED', // lost force to enemy
        DEAD :              'DEAD'

    };
});