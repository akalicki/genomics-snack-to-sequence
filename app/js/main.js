if (!window.File || !window.FileReader) {
    throw new Error("The File APIs are not fully supported in this browser.")
}

function handleDragOver(e) {
    e.stopPropagation();
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
}

function handleFileSelect(e, is_dropzone) {
    e.stopPropagation();
    e.preventDefault();

    var files = is_dropzone ? e.dataTransfer.files : e.target.files;
    for (var i = 0, f; f = files[i]; i++) {
        var reader = new FileReader();
        reader.onload = (e) => sendFastARequest(e.target.result);
        reader.readAsText(f);
    }
}

function sendFastARequest(fasta) {
    console.log(fasta);
}

document.getElementById('files').addEventListener(
    'change',
    (e) => handleFileSelect(e, false),
    false
);

var dropzone = document.getElementById('dropzone');
dropzone.addEventListener('dragover', handleDragOver, false);
dropzone.addEventListener('drop', (e) => handleFileSelect(e, true), false);
