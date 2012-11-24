YUI.add('vorsum-game', function (Y) {
    
    Y.VorsumGame = Y.Base.create('game', Y.Base, [], {

        initializer: function () {
            this.gameData = new Y.VorsumGameData();
            this.gameData.load(Y.bind(this.loadGameData, this));
            
            // delegate the main tick from gameData
            this.on('gameData:tick', this.delegateTick, this);

            this.planets = new Y.VorsumPlanetList();

            this.players = new Y.VorsumPlayerList();

            this.actions = new Y.VorsumActionList();

            this.on('*:requestAttack', this.tryAttack, this);
            
            this.on('action:finished', this.actionFinished, this);

        },

        actionFinished: function (e) {
            console.info('finished action', e.action);
        },

        tryAttack: function (e) {
            var ruling = false,
                request = {
                    requestee: e.target,
                    target: e.actionet,
                    force: e.force
                };

            if(!request.target) {
                Y.log('target invalid', 'warn', 'VorsumGame.tryAttack');
            }

            if(!request.ships) {
                Y.log('target invalid', 'warn', 'VorsumGame.tryAttack');
            }

            if(request.target && request.ships) {
                ruling = true;
            }

            Y.log('Game: attack ' + ruling ? 'allowed' : 'disallowed');

            ruling ? this.allowAttack(request) : this.disallowAttack(request);

        },

        createAction: function (config) {
            var action = new Y.VorsumAction(config);

            this.actions.addInstance(action);

            action.addTarget(this);

            return action;
        },

        delegateTick: function () {
            // fire on all planets
            this.planets.fire('tick');

            // fire on all players
            this.players.fire('tick');

            // fire on all actions
            this.actions.fire('tick');
        },

        createPlanet: function (config) {
            var planet = new Y.VorsumPlanet(config);

            // add to list of planets
            this.planets.addInstance(planet);

            // let planets communicate to us
            planet.addTarget(this);

            return planet;
        },

        createPlayer: function (config) {
            var player = new Y.VorsumPlayer(config);

            // put in list
            this.players.addInstance(player);

            // let players talk to us
            player.addTarget(this);

            return player;
        },

        getAllPlanets: function () {
            return this.planets.getAll();
        },

        getAllPlayers: function () {
            return this.players.getAll();
        },

        getCurrentTick: function() {
            return this.gameData.get('ticker');
        },

        getPlayersPlanets: function (player) {
            return this.planets.getByPlayer(player.get('id'));
        },

        putPlayerOnPlanet: function (player, planet) {
            planet.set('ownerId', player.get('id')).save();
        },

        removePlayerFromPlanet: function (player, planet) {
            planet.set('ownerId', null).save();
        },


        loadGameData: function (err, res) {
            var c;
            
            if(err) {
                throw new Error('loadGameData: failed to load game data, reason: ' + err);
            } else {
                Y.log('OK', 'info', 'VorsumGame.loadGameData');
            }

            // always use the first gameData instance..
            // FIXME: use game instantiation as ref
            if(res[0]) {
                c = res[0];
            } else {
                c = {};
            }
            this.gameData = new Y.VorsumGameData(c).start();
            
            // let gameData events bubble to this
            this.gameData.addTarget(this);
        },


    }, {
        ATTRS: {
            genesis: {
                value: 0
            }
        }
    });
});