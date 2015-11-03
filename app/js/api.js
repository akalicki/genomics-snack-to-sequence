//Used YQL to solve the cross domain issue: http://icant.co.uk/articles/crossdomain-ajax-with-jquery/error-handling.html

var blastInfoRegEx = /QBlastInfoBegin.*?QBlastInfoEnd/g
var base_url = "http://www.ncbi.nlm.nih.gov/blast/Blast.cgi?"
var proxy_url = "http://query.yahooapis.com/v1/public/yql?" +
                "q=select%20*%20from%20html%20where%20url%3D%22" +
                "{BLAST_URL}" +
                "%22&format=application/x-www-form-urlencoded'&callback=?";

/*
 * Makes a new API query, retrieves its RID, and sends a BLAST request
 *
 */
function sendBlastRequest(post_params) {
    var url = base_url + jQuery.param(post_params);
	$.getJSON(
        proxy_url.replace("{BLAST_URL}", encodeURIComponent(url)),
		function (data) {
            if (data.results[0]) { // success
                var data = filterBlastData(data.results[0]);
                var info = data.match(blastInfoRegEx)[0];
                if (info.length > 0) {
    				var searchString1 = 'RID = ';
    				var searchString2 = ' RTOE';
    				var RID = info.substring(
                        info.indexOf(searchString1) + searchString1.length,
                        info.indexOf(searchString2)
                    ).replace(/ /g,'');
                    console.log("Sending FASTA sequence for matching...");
                    getBlastResult(RID);
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
function getBlastResult(RID) {
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
		    var data = filterBlastData(data.results[0]);
		    
            var info = data.match(blastInfoRegEx)[0];
            if (info.length > 0) {
        		var searchString1 = 'Status=';
        		var searchString2 = 'QBlastInfoEnd';
        		var status = info.substring(
                    info.indexOf(searchString1) + searchString1.length,
                    info.indexOf(searchString2)
                );

        		if (status.startsWith('READY')) {
        			console.log(data);
        		} else if (status.startsWith('WAITING')) {
        			console.log("QBlast Query still processing, trying again.");
        			setTimeout((_) => getBlastResult(RID), 10000);
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
function filterBlastData(data){
    // no body tags
    data = data.replace(/<?\/body[^>]*>/g,'');
    // no linebreaks
    data = data.replace(/[\r|\n]+/g,'');
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