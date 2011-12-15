var botposition = [-1,-1];
var botwidth = 30;
var botheight = 30;

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
    if (botposition[0] > -1) {
        ctx.clearRect(botposition[0], botposition[1], botwidth, botheight);
    }

    var img = new Image();
    img.src = 'robot.png';
    img.onload = function() {
        ctx.drawImage(img, x, y);
    }

    botposition = [x,y];
}

function drawmap(ctx, map) {
    var lines = map.split("\n");
    var x = 10;
    var y = 10;
    var width = 60;
    var height = 60;

    for (var i=0; i < lines.length; i++) {
        x = 10;
        for (var j=0; j < lines[i].length; j++) {
            if (lines[i][j] == "X") {
                drawfilledrect(ctx, x, y, width, height);
            } else {
                drawopenrect(ctx, x, y, width, height);
                if (lines[i][j] == "o") {
                    drawbot(ctx, x + (width/2) - (botwidth/2), y + (height/2) - (botheight/2));
                }
            }
            x += width;
        }
        y += height;
    }
}
