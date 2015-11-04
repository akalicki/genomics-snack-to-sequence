//Used YQL to solve the cross domain issue: http://icant.co.uk/articles/crossdomain-ajax-with-jquery/error-handling.html

var blastInfoRegEx = /QBlastInfoBegin.*?QBlastInfoEnd/g
var base_url = "http://www.ncbi.nlm.nih.gov/blast/Blast.cgi?"
var proxy_url = "http://query.yahooapis.com/v1/public/yql?" +
                "q=select%20*%20from%20html%20where%20url%3D%22" +
                "{BLAST_URL}" +
                "%22&format=application/x-www-form-urlencoded'&callback=?";

var species_url = "http://api.gbif.org/v1/species?";

/*
 * Makes a species API query, returns object with kingdom, class, and vernacularName (if present)
 */
//http://api.gbif.org/v1//occurrence/search?year=1800,1899
function getSpecies(species) {
    var SPECIES_PARAMS =
    {
        'name': species,
        'limit': 1
    }
    $.ajax({
        type: 'GET',
        url: species_url + jQuery.param(SPECIES_PARAMS),
        data: {
            format: 'json'
        },
        error: function () {
            throw new Error('Species API error');
        },
        dataType: 'jsonp',
        success: function(data) {
            console.log('success');
            console.log(data);
            if(data.results.length>0) {
                console.log(data.results[0].vernacularName);
                return {'kingdom': data.results[0].kingdom, 'class': data.results[0].class, 'vernacularName': data.results[0].vernacularName};
            } else {
                return null;
            }
        }
    });
}

/*
 * Makes a new API query, retrieves its RID, and sends a BLAST request
 *
 */
function sendBlastRequest(post_params, chart) {
    var url = base_url + jQuery.param(post_params);
	$.getJSON(
        proxy_url.replace("{BLAST_URL}", encodeURIComponent(url)),
		function (data) {
            if (data.results[0]) { // success
                var data = filterBlastData(data.results[0], true);
                var info = data.match(blastInfoRegEx)[0];
                if (info.length > 0) {
    				var searchString1 = 'RID = ';
    				var searchString2 = ' RTOE';
    				var RID = info.substring(
                        info.indexOf(searchString1) + searchString1.length,
                        info.indexOf(searchString2)
                    ).replace(/ /g,'');
                    console.log("Sending FASTA sequence for matching...");
                    getBlastResult(RID, chart);
                } else {
				    throw new Error("No QBlastInfo Sent.");
                }
            } else {
        	   throw new Error('Uncaught exception.');
            }
        }
    );
}



/*
 * Using the RID, determine status of the API query. If status is waiting, loop
 * until the status is ready (the search results have been returned)
 *
 */
function getBlastResult(RID, chart) {
	var GET_PARAMS = {
        'RID': RID,
        'FORMAT_TYPE': 'Text',
        'CMD': 'Get'
    }

	var url = base_url + jQuery.param(GET_PARAMS);
	$.getJSON(
        proxy_url.replace("{BLAST_URL}", encodeURIComponent(url)),
		function (data) {
            if (data.results[0]) { // success
                var info_data = filterBlastData(data.results[0], true);
		    
                var info = info_data.match(blastInfoRegEx)[0];
                if (info.length > 0) {
            		var searchString1 = 'Status=';
            		var searchString2 = 'QBlastInfoEnd';
            		var status = info.substring(
                        info.indexOf(searchString1) + searchString1.length,
                        info.indexOf(searchString2)
                    );

            		if (status.startsWith('READY')) {
                        data = filterBlastData(data.results[0], false);
                        addMapToChart(blastToMap(data), chart);
            		} else if (status.startsWith('WAITING')) {
            			console.log("QBlast Query still processing, trying again in 10 seconds...");
            			setTimeout((_) => getBlastResult(RID, chart), 10000);
            		} else if (status.startsWith('FAILED')) {
            			throw new Error("QBlast Query failed.");
            		}
                } else {
                	throw new Error("No QBlastInfo Sent");
                }
            } else {
                throw new Error('Uncaught exception.');
            }
    });
}

/*
 * Filter all the nasties out
 */
function filterBlastData(data, remove_newlines){
    // no body tags
    data = data.replace(/<?\/body[^>]*>/g,'');
    // no linebreaks
    if (remove_newlines) {
        data = data.replace(/[\r|\n]+/g,'');
    }
    // no comments
    data = data.replace(/<--[\S\s]*?-->/g,'');
    // no noscript blocks
    data = data.replace(/<noscript[^>]*>[\S\s]*?<\/noscript>/g,'');
    // no script blocks
    data = data.replace(/<script[^>]*>[\S\s]*?<\/script>/g,'');
    // no self closing scripts
    data = data.replace(/<script.*\/>/,'');
    // [... add as needed ...]
    return data;
  }