//Used YQL to solve the cross domain issue: http://icant.co.uk/articles/crossdomain-ajax-with-jquery/error-handling.html

var blastInfoRegEx = /QBlastInfoBegin.*?QBlastInfoEnd/g
var base_url = "http://www.ncbi.nlm.nih.gov/blast/Blast.cgi?"

/**
 * Makes a new API query
 * Gets its RID
 *
 **/
function getBlastRID () {
	var POST_PARAMS =
    {
    	//PARAM documentation here: http://www.ncbi.nlm.nih.gov/blast/Doc/node68.html
        'QUERY': '555', //could also query a FASTA sequence
        'DATABASE': 'nr',
        'HITLIST_SIZE': 10,
        'FILTER': 'L',
        'EXPECT': 10,

        'FORMAT_TYPE': 'Text',
        'PROGRAM': 'blastn',
        'CLIENT': 'Web',
        'SERVICE': 'plain',
        'NCBI_GI': 'on',
        'PAGE': 'Nucleotides',
        'CMD': 'Put'
    }
    var url = base_url + jQuery.param(POST_PARAMS);
	//var url = 'http://www.ncbi.nlm.nih.gov/blast/Blast.cgi?QUERY=555&DATABASE=nr&HITLIST_SIZE=10&FILTER=L&EXPECT=10&FORMAT_TYPE=TEXT&PROGRAM=blastn&CLIENT=web&SERVICE=plain&NCBI_GI=on&PAGE=Nucleotides&CMD=Put'
	$.getJSON("http://query.yahooapis.com/v1/public/yql?"+
	                "q=select%20*%20from%20html%20where%20url%3D%22"+
	                encodeURIComponent(url)+
	                "%22&format=application/x-www-form-urlencoded'&callback=?",
		function(data){
		if(data.results[0]){ //success
		    var data = filterData(data.results[0]);
		    console.log("success");
		    var info = data.match(blastInfoRegEx)[0];
			if(info.length>0) {
				var searchString1 = 'RID = ';
				var searchString2 = ' RTOE';
				var RID = info.substring(info.indexOf(searchString1)+searchString1.length, info.indexOf(searchString2));
				RID = RID.replace(/ /g,'');
				getBlastResult(RID);
				//setTimeout(function () {getBlastResult(RID);}, 3000);
			} else {
				console.log("No QBlastInfo Sent");
			}
		  } else { //error
		  	console.log('error');
		  }
		});
}

/**
 * Using the RID, determine status of the API query
 * If status is waiting, loop until the status is ready (the search results have been returned)
 *
 **/
function getBlastResult(RID) {
	var GET_PARAMS =
    {
    	'RID': RID,
        'FORMAT_TYPE': 'Text',
        'CMD': 'Get'
    }
	//var url = "http://www.ncbi.nlm.nih.gov/blast/Blast.cgi?RID="+RID+"&FORMAT_TYPE=TEXT&CMD=Get";
	var url = base_url + jQuery.param(GET_PARAMS);
	$.getJSON("http://query.yahooapis.com/v1/public/yql?"+
	                "q=select%20*%20from%20html%20where%20url%3D%22"+
	                encodeURIComponent(url)+
	                "%22&format=application/x-www-form-urlencoded'&callback=?",
		function(data){
		if(data.results[0]){ //success
		    var data = filterData(data.results[0]);
		    console.log("success");
		    var info = data.match(blastInfoRegEx)[0];
			if(info.length>0) {
				var searchString1 = 'Status=';
				var searchString2 = 'QBlastInfoEnd';
				var status = info.substring(info.indexOf(searchString1)+searchString1.length, info.indexOf(searchString2));
				console.log(status);
				if (status.startsWith('READY')) {
					//parse data stuff
					console.log(data);
				} else if (status.startsWith('WAITING')) {
					console.log("QBlast Query still processing");
					//add delay between queries so we don't get banned
					setTimeout(function () {getBlastResult(RID);}, 10000);
				} else if (status.startsWith('FAILED')) {
					console.log("QBlast Query failed.")
				}
			} else {
				console.log("No QBlastInfo Sent");
			}
		  } else { //error
		  	console.log('error');
		  }
		});
}

function filterData(data){
    // filter all the nasties out
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

 $( document ).ready(function() {
 	//getBlastRID(); //makes new query
 	getBlastResult('3FNBM9ZT014'); //This is a search of one of our fasta files that got status READY
});