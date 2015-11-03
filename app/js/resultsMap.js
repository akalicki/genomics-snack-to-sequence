// Utilities to convert a text-format blast response to a map of species name
// to counts
var extractName = function(line) {
    // now we have two problems
    var names = line.match(/\|.*\|  (PREDICTED: )?\b(\w*)\b \b(\w*)\b/);
    return names[2]+" "+names[3];
};

var blastToMap = function(text) {
    var ind = [];
    var lines = text.split("\n");
    for (var ii = 0; ii < lines.length; ++ii) {
        if (lines[ii].match(/Sequences producing/)) {
            ind.push(ii+2);
        }
    }
    var newMap = new Object();
    var name = "";
    for (ii = 0; ii < ind.length; ++ii) {
        name = extractName(lines[ind[ii]]);
        if (newMap[name]) {
            newMap[name] = newMap[name] + 1;
        } else {
            newMap[name] = 1;
        }
    }
    return newMap;
};

var mergeMaps = function(from, into) {
    // note: mutates the second argument
    for (var name in from) {
        if (into[name]) {
            into[name] = into[name] + from[name];
        } else {
            into[name] = from[name];
        }
    }
};

/* {'Genus species': 2, 'Genus species': 4} */
