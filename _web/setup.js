
function init() {

  // Add drop handling
  document.getElementById("body").addEventListener("dragenter", noop_handler, false);
  document.getElementById("body").addEventListener("dragleave", noop_handler, false);
  document.getElementById("body").addEventListener("dragover", noop_handler, false);  
  document.getElementById("img_dropzone").addEventListener("drop", on_drop, false);
  document.getElementById("seg_dropzone").addEventListener("drop", on_drop, false);

};

function noop_handler(evt) {

  evt.stopPropagation();
  evt.preventDefault();
};

function on_drop(evt, elem) {

  // Get the dropped files.
  noop_handler(evt);
  var files = evt.dataTransfer.files;

  // If anything is wrong with the dropped files, exit.
  if (typeof files == "undefined" || files.length == 0) {
    return;
  }

  var list = document.getElementById(evt.target.id.split('_')[0]+'_files');
  for (var i=0; i<files.length;i++) {

    list.innerHTML += files[i].name+'<br>'

  }

  upload(files);

};

function upload(files) {

  console.log('not uploading...');

};