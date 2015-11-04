/*
 * Utilities to convert a text-format blast response to a map of species name
 * to counts
 */

/*
 * Take a response line and parse species name as well as bit score
 */
function extractInfo(line) {
    var info = line.match(/\|.*\|  (PREDICTED: )?\b(\w*)\b \b(\w*)\b (.*)/);
    if (info === null) {
        return null;
    }

    return [info[2] + " " + info[3], parseFloat(rest[rest.length - 2])];
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

    var map = {};
    var info = [];
    var name = "";
    var bit_score = 0.0;
    for (ii = 0; ii < ind.length; ++ii) {
        info = extractInfo(lines[ind[ii]]);
        if (info === null) {
            continue;
        }

        name = info[0];
        bit_score = info[1];
        
        if (map[name]) {
            map[name] = [map[name][0] + bit_score, -1];
        } else {
            map[name] = [bit_score, -1];
        }
    }

    return map;
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
