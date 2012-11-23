YUI.add('vorsum-planet-model', function (Y) {

    Y.VorsumPlanetModel = Y.Base.create('planetModel', Y.VorsumModel, [], {
        
        sync: Y.LocalStorageSync('planet'),


    }, {
        ATTRS: {

            // currency
            currency: { value: 0 },
            currencyGainPerTick: { value: 1000 },
            currencyBonusModifier: { value: 1 },

            ticksParticipation: { value: 0 },

            // evolution
            evolution: { value: 0 },
            evolutionGainPerTick: { value: 0.001 },
            evolutionBonusModifier: { value: 1 },

            ownerId: {
                value: null
            },
            name: {
                value: 'Unnamed planet'
            }
        }
    });
});