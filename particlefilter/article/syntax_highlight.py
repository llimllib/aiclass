import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

code = """var new_weights = [];
var new_particles = [];

//For each of N particles
for (var i=0; i < particles.length; i++) {
    
    //Choose a new particle with respect to the weights of each particle
    var j = weighted_sample(weights, particles);

    //move the particle as if it were the robot. i.e. if the robot tried to 
    //move right, we move the particle right with the same probability as the 
    //robot. In our case, that means that the particle has an 80% chance of 
    //moving in the intended direction.
    var xp = update_particle(j, control);

    //Now measure how likely it is that the particle measured what the robot 
    //measured, and use that as the weight of the particle
    var wp = update_weight(xp, measurement);

    //and push the new (weight, particle) pair
    new_weights.push(xp);
    new_particles.push(wp);
}"""

lexer = get_lexer_by_name("javascript")
formatter = HtmlFormatter(noclasses=True)
code = pygments.highlight(code, lexer, formatter)
