

const params = new URLSearchParams(window.location.search)

let selectedAllFiles = false

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function httpPost(url, data)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", url, true ); // false for synchronous request

    xmlHttp.onreadystatechange = function() {
        if (this.readyState != 4) return;
        return this.responseText
    }

    xmlHttp.send(data);

}


function getPath(){
    let path = '/';
    if (params !== null && params.has('path')){
        path = params.get('path') + '/'
    }
    return path
}

function folderOpen(foldername){
    let path = getPath()
    let url = 'filemanager' + '?' + 'path=' + path + foldername
    window.location.replace(url)
}


function openFile(name){
    // Путь
    let path = params.get('path')
    //alert('open: ' + path + '/' + name)

    let url = '/editor' + '?'
    + 'path=' + path
    + '&name=' + name

    window.open(url);
}

function openDataBase(name){
    // Путь
    let path = params.get('path')

    let url = '/databasereader' + '?'
    + 'db=' + path + '/' + name

    window.open(url);
}

function openAudio(name){
    // Путь
    let path = params.get('path')

    let url = '/audio' + '?'
    + 'audio=' + path + '/' + name

    window.open(url);
}


$(function () {
    $(document).on('dblclick', '[data-toggle="lightbox"]', function(event) {
      event.preventDefault();
      $(this).ekkoLightbox({
        alwaysShowClose: true
      });
    });

    $('.filter-container').filterizr({gutterPixels: 3});
    $('.btn[data-filter]').on('click', function() {
      $('.btn[data-filter]').removeClass('active');
      $(this).addClass('active');
    });
  })



function unSelectAllFiles(){
    let files = $('body').find('.btn-file-selected')
    selectedAllFiles = !selectedAllFiles
    files.each(function (index, element) {
        element.checked = false
    })
}

// Веделение всех файлов
function selectAllFiles(){
    let files = $('body').find('.btn-file-selected')
    selectedAllFiles = !selectedAllFiles
    files.each(function (index, element) {
        element.checked = selectedAllFiles
    })
    if (selectedAllFiles){
        $('#btn-select-all-files').text('Снять выделение')
    }else{
        $('#btn-select-all-files').text('Выделить все')
    }

    deleteAllActivate()
}

// Включение / выключения кнопки удаления выделенных файлов
function deleteAllActivate(){
    let files = $('body').find('.btn-file-selected')
    let test = false
    files.each(function (index, element) {
        if (element.checked){
            // Activate
            test = true
            $('#btn-deleteAllSelectedFiles').removeClass('disabled')
        }
    })
    if (test){return}
    // Disactive
    $('#btn-deleteAllSelectedFiles').addClass('disabled')
}

// Подтверждение удаления веделенных файлов
function deleteAllSelectedFilesConfirm(){
    let filesSelected = ''
    let files = $('body').find('.btn-file-selected')
    files.each(function (index, element) {
        if (element.checked){
            //filesSelected.push(element.dataset['name'])

            if (filesSelected !== ''){
                filesSelected += ', '
            }
            filesSelected += element.dataset['name']
        }
    })

    $('#delete-files-name').html(filesSelected)
    $('#deleteFiles').modal('show')
}

// Удаление выделенных файлов
function deleteFilesEvent(){
    // Путь
    let path = params.get('path')
    let files = $('body').find('.btn-file-selected')
    files.each(function (index, element) {
        if (element.checked){
            let url = '/api/deletefile'
                + '?'
            + 'path=' + path
            + '&name=' + element.dataset['name'];
            httpGet(url)

        }
    })

    unSelectAllFiles()
    location.reload()
}


/*---------------------------------------------*/

// Новая папка
function newDir(){
    $('#create-folder-name').val('')
    $('#createFolder').modal('show')
}
function createFolder(){
    let name = $('#create-folder-name').val()

    let url = '/api/createfolder'
        + '?'
    + 'path=' + params.get('path')
    + '&name=' + name;
    httpGet(url)

    location.reload()
}

// Новый файл
function newFile(){
    $('#create-file-name').val('')
    $('#createFile').modal('show')
}
function newFileEvent(){
    // Новое имя
    let newName = $('#create-file-name').val()
    // Путь
    let path = params.get('path')

    let url = '/api/createfile'
        + '?'
    + 'path=' + path
    + '&name=' + newName;
    httpGet(url)

    location.reload()
}

// Загрузка файлов
function loadFiles(){
    $('#loadFiles').modal('show')
}
function loadFilesEvent(){
    // Путь
    let path = params.get('path')

    let url = 'api/uploadfile?path=' + path
    let fileBox = document.getElementById('formFileMultiple')
    let files = fileBox.files[0]

    console.log(files)

    let data = new FormData()
    data.append('files', files)
    //let resultSave = httpPost(url, data)
    //console.log(resultSave)


    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", url, true ); // false for synchronous request

    xmlHttp.onreadystatechange = function() {
        if (this.readyState !== 4) return;

        if (this.responseText === 'ok'){
            location.reload()
        }
    }

    xmlHttp.send(data);
}

function deleteFile(name){
    oldNameFile = name
    $('#delete-file-name').html(name)
    $('#deleteFile').modal('show')
}
function deleteFileEvent(){
    // Полное имя файла
    let name = oldNameFile
    // Путь
    let path = params.get('path')

    let url = '/api/deletefile'
        + '?'
    + 'path=' + path
    + '&name=' + name;
    httpGet(url)

    location.reload()
}

function uparchiv(name){
    // Путь
    let path = params.get('path')

    let url = '/api/uparchiv'
        + '?'
    + 'path=' + path
    + '&name=' + name;
    httpGet(url)

    location.reload()
}


function scriptStart(name){
    // Путь
    let path = params.get('path')
    let fullName = path + '/' + name

    let url = '/cmd?fullName=' + fullName
    window.open(url);

}
/*---------------------------------------------*/






let oldNameFile;

function renameFile(name){
    oldNameFile = name
    $('#rename-file-name').val(name)
    $('#renameFile').modal('show')
}
function renameFileEvent(){
    // Полное имя файла
    let name = oldNameFile
    // Новое имя
    let newName = $('#rename-file-name').val()
    // Путь
    let path = params.get('path')

    let url = '/api/renamefile'
        + '?'
    + 'path=' + path
    + '&name=' + name
    + '&newname=' + newName;
    httpGet(url)

    location.reload()
}