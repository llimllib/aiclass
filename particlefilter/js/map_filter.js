/* depends on particlefilter.js being loaded first */

// makeClass - By John Resig (MIT Licensed)
function makeClass(){
    return function(args){
        if ( this instanceof arguments.callee ) {
            if ( typeof this.init == "function" )
                this.init.apply( this, args.callee ? args : arguments );
        } else
            throw "You must instantiate this class with  'new <classname>()', not '<classname>()'";
    };
}

MapFilter = (function() {

MapFilter = makeClass();

var that;

MapFilter.prototype.init = function(map, nparticles) {
    this.map = this.arraymap(map);

    this.nrows = this.map.length;
    this.ncols = this.map[0].length;

    //depends on nrows and ncols
    this.particles = this.makeparticles(nparticles);

    that = this;
};

//turn a map from a string into an array
MapFilter.prototype.arraymap = function(maps) {
    var maplines = maps.split("\n");
    var map = [];

    for (var i=0; i < maplines.length; i++) {
        map.push(maplines[i].split(""));
    }

    return map;
};

MapFilter.prototype.makeparticles = function(n) {
    var particles = [];
    var weights = [];
    var x = 0;
    var y = 0;

    for (var i=0; i < n; i++) {
        row = Math.floor(Math.random() * this.nrows);
        col = Math.floor(Math.random() * this.ncols);
        while (this.map[row][col] != "_" && this.map[row][col] != 'o') {
            row = Math.floor(Math.random() * this.nrows);
            col = Math.floor(Math.random() * this.ncols);
        }
        particles.push([row, col]);
        weights.push(1/n);
    }

    return [particles, weights];
};

MapFilter.prototype.findbot = function() {
    for (var i=0; i < this.map.length; i++) {
        for (var j=0; j < this.map[0].length; j++) {
            if (this.map[i][j] == "o") {
                return [i,j];
            }
        }
    }
};

MapFilter.prototype.getmove = function(direction) {
    var move = Math.random();
    var moves = {
        "up": ["left", "right"],
        "left": ["up", "down"],
        "down": ["right", "left"],
        "right": ["down", "up"]
    };

    //80% chance bot moves where you want. Otherwise, you fail by 90 degrees
    if (move > .8) {
        direction = moves[direction][move > .9 ? 0 : 1];
    }

    return direction;
};

MapFilter.prototype.movebot = function(direction) {
    var move = this.getmove(direction);

    var botloc = this.findbot(this.map);
    var row = botloc[0];
    var col = botloc[1];

    console.log("moving bot: " + move);

    if (move == "up")    { botloc = this.movecoords(row, col, row-1, col); }
    if (move == "left")  { botloc = this.movecoords(row, col, row, col-1); }
    if (move == "down")  { botloc = this.movecoords(row, col, row+1, col); }
    if (move == "right") { botloc = this.movecoords(row, col, row, col+1); }

    if (botloc[0] != row || botloc[1] != col) {
        this.map[row][col] = '_';
        this.map[botloc[0]][botloc[1]] = 'o';
    }

    //our bot can sense if there is a wall to the north, south, east or west
    var measurement = this.sense(botloc);

    console.log("mesaurement: "+ measurement);

    this.particles = ParticleFilter(this.particles,
                                    moveparticle,
                                    direction,
                                    this.newweight,
                                    measurement);
};

MapFilter.prototype.sense = function(botloc) {
    var row = botloc[0];
    var col = botloc[1];

    //an array of 4 integers. 1 represents a wall, 0 represents no wall.
    //ordered north, west, south, east.
    return [
        this.iswall(row-1, col),
        this.iswall(row, col-1),
        this.iswall(row+1, col),
        this.iswall(row, col+1)
    ];
};

MapFilter.prototype.iswall = function(row, col) {
    //10% of the time, return a random measurement
    var r = Math.random();
    if (r < .1) {
        return Math.floor(r*100) % 2;
    }

    //otherwise, return 1 if [row, col] is a wall
    if (row < 0 || row > this.nrows-1 ||
        col < 0 || col > this.ncols-1 ||
        this.map[row][col] == 'X') {
        return 1;
    }
    return 0;
};

//try to move from [row, col] to [newrow, newcol]. If [newrow, newcol] is not a
//valid square, return [row, col]
MapFilter.prototype.movecoords = function(row, col, newrow, newcol) {
    if (newrow < 0 || newrow > this.nrows-1 ||
        newcol < 0 || newcol > this.ncols-1 ||
        this.map[newrow][newcol] == 'X') {
        return [row, col];
    }
    return [newrow, newcol];
};


MapFilter.prototype.find_walls = function(row, col) {
    var walls = [];

    walls.push(row > 0            && this.map[row-1][col] != 'X' ? 0 : 1);
    walls.push(col > 0            && this.map[row][col-1] != 'X' ? 0 : 1);
    walls.push(row < this.nrows-1 && this.map[row+1][col] != 'X' ? 0 : 1);
    walls.push(col < this.ncols-1 && this.map[row][col+1] != 'X' ? 0 : 1);

    return walls;
};

//Has to be in here to reference "this". I mean "that". Ugh... Javascript.
var moveparticle = function(particle, direction) {
    var row = particle[0];
    var col = particle[1];

    var move = that.getmove(direction);

    if (move == "up")    { return that.movecoords(row, col, row-1, col); }
    if (move == "left")  { return that.movecoords(row, col, row, col-1); }
    if (move == "down")  { return that.movecoords(row, col, row+1, col); }
    if (move == "right") { return that.movecoords(row, col, row, col+1); }

    throw "we should never get here: <" + move + ">";
};


//Given the particle, return the likelihood of the given measurement
MapFilter.prototype.newweight = function(particle, measurement) {
    var row = particle[0];
    var col = particle[1];

    //P(wall measurement|wall) = .95
    var p_wallm_wall = .95;
    //P(wall measurement|no wall) = .05
    var p_wallm_nowall = .05;

    var probabilities = [];

    var walls = that.find_walls(row, col);

    for (var i=0; i < measurement.length; i++) {
        //if we measured wall
        if (measurement[i] == 1) {
            //push P(wall measurement|wall) if it is a wall, its complement otherwise
            probabilities.push(walls[i] == 1 ? p_wallm_wall : 1-p_wallm_wall);
        } else {
            //push P(wall measurement|no wall) if it is a wall, its complement otherwise
            probabilities.push(walls[i] == 1 ? p_wallm_nowall : 1-p_wallm_nowall);
        }
    }

    //return the product; the probabilities are all conditionally independent.
    return probabilities.reduce(function(a,b) { return a*b; });
};

return MapFilter;

})();
