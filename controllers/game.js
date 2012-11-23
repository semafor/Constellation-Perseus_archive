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

        createAttack: function (attacker, planet, force) {

        },

        allowAttack: function (request) {
            request.requestee.fire('attackAllowed', {
                request: request
            });


        },

        disallowAttack: function (request) {
            request.requestee.fire('attackDisallowed', {
                request: request
            });
        },

        allowPlanetSettle: function (request) {
            request.requestee.fire('planetSettleAllowed', {
                request: request
            });
        },

        disAllowPlanetSettle: function (request) {
            request.requestee.fire('planetSettleDisallowed', {
                request: request
            });
        },

        delegateTick: function () {
            // fire on all planets
            this.planets.fire('tick');

            // fire on all players
            this.players.fire('tick');
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

        loadActions: function () {
            
        }


    }, {
        ATTRS: {
            genesis: {
                value: 0
            }
        }
    });
});