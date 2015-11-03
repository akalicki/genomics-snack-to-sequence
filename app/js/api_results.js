/*
 * Utilities to convert a text-format blast response to a map of species name
 * to counts
 */

function extractName(line) {
    // now we have two problems
    var names = line.match(/\|.*\|  (PREDICTED: )?\b(\w*)\b \b(\w*)\b/);
    return names[2] + " " + names[3];
};

/*
 * Take a stripped down BLAST result, and build a map:
 *   filename -> [count, graph_index]
 */
function blastToMap(text) {
    var ind = [];
    var lines = text.split("\n");
    for (var ii = 0; ii < lines.length; ++ii) {
        if (lines[ii].match(/Sequences producing/)) {
            ind.push(ii+2);
        }
    }

    var newMap = {};
    var name = "";
    for (ii = 0; ii < ind.length; ++ii) {
        name = extractName(lines[ind[ii]]);
        if (newMap[name]) {
            newMap[name] = [newMap[name][0] + 1, -1];
        } else {
            newMap[name] = [1, -1];
        }
    }

    return newMap;
};

function mergeMaps(from, into) {
    // note: mutates the second argument
    for (var name in from) {
        if (into[name]) {
            into[name] = [into[name][0] + from[name][0], into[name][1]];
        } else {
            into[name] = from[name];
        }
    }
};

/* {'Genus species': 2, 'Genus species': 4} */
