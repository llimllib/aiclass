var botposition = [-1,-1];
var botwidth = 30;
var botheight = 30;
var startx = 0;
var starty = 0;
var boxwidth = 60;
var boxheight = 60;
var particler = 3;

function drawopenrect(ctx, x, y, width, height) {
    ctx.beginPath();
    ctx.rect(x, y, width, height);
    ctx.closePath();
    ctx.stroke();
}

function drawfilledrect(ctx, x, y, width, height) {
    ctx.beginPath();
    ctx.rect(x, y, width, height);
    ctx.closePath();
    ctx.fill();
}

function drawbot(ctx, x, y) {
    //TODO: don't reload this guy every time
    var img = $("#robotimg")[0];
    ctx.drawImage(img, x, y);

    botposition = [x,y];
}

function gridcoords(maprow, mapcol) {
  return [starty + boxheight * maprow, startx + boxwidth * mapcol];
}

function drawparticle(ctx, particle) {
    var coords = gridcoords(particle[0], particle[1]);
    var x = coords[1];
    var y = coords[0];

    //add between particler and boxwidth/height to x to get a random pos
    x += particler + Math.random() * (boxwidth - 2*particler)
    y += particler + Math.random() * (boxheight - 2*particler)

    ctx.save();
    ctx.fillStyle = "#00A308";
    ctx.beginPath();
    ctx.arc(x, y, particler, 0, Math.PI*2, true);
    ctx.closePath;
    ctx.fill();
    ctx.restore();
}

function drawmap(ctx, map, particles) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    var x = startx;
    var y = starty;

    for (var i=0; i < map.length; i++) {
        x = startx;
        for (var j=0; j < map[i].length; j++) {
            if (map[i][j] == "X") {
                drawfilledrect(ctx, x, y, boxwidth, boxheight);
            } else {
                drawopenrect(ctx, x, y, boxwidth, boxheight);
                if (map[i][j] == "o") {
                    drawbot(ctx, x + (boxwidth/2) - (botwidth/2), y + (boxheight/2) - (botheight/2));
                }
            }
            x += boxwidth;
        }
        y += boxheight;
    }

    for (var i=0; i < particles.length; i++) {
        drawparticle(ctx, particles[i]);
    }
}
