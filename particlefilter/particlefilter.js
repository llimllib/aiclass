/* depends on sample.js being loaded first */

//Run the particle filter algorithm.
//particles is a 2-element list. Both elements are arrays; the first is
//an array of particles; the particlefilter won't explicitly know what a
//particle is, so make them whatever data type you like. The second list
//is a list of floats which correspond to the weights of the particles.
//
//update_particle is a function called with a particle and the control
//vector (which ParticleFilter also doesn't look into, so pass it whatever
//your system understands).
//
//control is the control vector, telling the particle filter what the control
//parameters have been over the last time delta
//
//update_weight is a function which is given a particle and a measurement,
//and returns the new weight for that particle.
//
//measurement is the measurement given by the robot's sensor data
function ParticleFilter(particles, update_particle, control, update_weight, measurement) {
    //particles, weights
    var newparticles = [[], []];
    var eta = 0;

    for (var i=0; i < particles[0].length; i++) {
        var j = weighted_sample(particles[1], particles[0]);

        var xp = update_particle(j, control);
        var wp = update_weight(xp, measurement);

        eta += wp;

        newparticles[0].push(xp);
        newparticles[1].push(wp);
    }

    //normalize our weights
    for (var i=0; i < newparticles[1].length; i++) {
        newparticles[1][i] = newparticles[1][i] / eta;
    }

    return newparticles;
}
