function handleDragOver(e) {
    e.stopPropagation();
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
}

function handleFileSelect(e, is_dropzone, chart) {
    e.stopPropagation();
    e.preventDefault();

    var files = is_dropzone ? e.dataTransfer.files : e.target.files;
    for (var i = 0, f; f = files[i]; i++) {
        var reader = new FileReader();
        reader.onload = (e) => sendFastARequest(e.target.result, chart);
        reader.readAsText(files[i]);
    }
}

function sendFastARequest(fasta, chart) {
    // PARAM documentation: http://www.ncbi.nlm.nih.gov/blast/Doc/node68.html
    var POST_PARAMS = {
        'QUERY': fasta,
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
        'CMD': 'Put',
    }

    sendBlastRequest(POST_PARAMS, chart);
}

$(document).ready(function() {
    if (!window.File || !window.FileReader) {
        throw new Error("File APIs are not fully supported in this browser.")
    }

    // Take individual maps and make a master map to display the graph
    var ctx = document.getElementById("donut").getContext("2d");

    // start out with empty data, nothing in the chart
    var chart = new Chart(ctx).Doughnut([], { responsive : true });

    document.getElementById('files').addEventListener(
        'change',
        (e) => handleFileSelect(e, false, chart),
        false
    );

    var dropzone = document.getElementById('dropzone');
    dropzone.addEventListener('dragover', handleDragOver, false);
    dropzone.addEventListener(
        'drop',
        (e) => handleFileSelect(e, true, chart),
        false
    );
});
