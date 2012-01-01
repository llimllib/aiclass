function sum(list) {
  return list.reduce(function(a,b) { return a+b; })
}

var epsilon = .00000001;

function weighted_sample(weights, objects) {
  if (weights.length == 0) {
    throw "can't sample from an empty weights array";
  }

  if (weights.length != objects.length) {
    throw "weights and objects have different dimensions";
  }

  var totalweight = sum(weights);

  if (Math.abs(totalweight-1) > epsilon) {
    throw "expecting weights to be normalized: " + totalweight;
  }

  //Our stupid simple sampling algorithm:
  // * pick a random number
  // * if it's less than the first weight, return the first object
  // * if it's less than the sum of the first and second weight, return the second object
  // * ...
  // * if it's less than the sume of the first nth weights, return the nth object
  var rand = Math.random();
  var weightsum = 0;
  for (var i=0; i < weights.length; i++) {
    weightsum += weights[i];
    if (rand < weightsum) { return objects[i]; }
  }

  //If we've fallen through, we could have picked exactly 1 as our random value,
  //or we could have some sort of float addition thing going on (1.0000001 as our totalweight).
  //return the last particle.
  return weights[weights.length-1];
}
