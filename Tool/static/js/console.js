

const params = new URLSearchParams(window.location.search)


function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

let consolePanel


function StopScript(){
    let fullName = params.get('fullName')
    let url = '/api/stopscript?fullName=' + fullName
    data = httpGet(url)
}
function StartScript(){
    window.location.reload()
}
function SettingsModal(){
    $('#settingsModal').modal('show')
}


function stopAction(){
    $('#btn-group-stop').addClass('hide')
    $('#btn-group-start').removeClass('hide')
}

let lastLine = 0
function getConsole(){
    // файл
    let fullName = params.get('fullName')
    let url = '/api/getconsole?fullName=' + fullName
    let data = ''
    let meta
    //term.echo('[[;;;item-red]HELLO');

    if (scriptRuning){
        let dataGet = JSON.parse(httpGet(url))
        console.log(dataGet)

        data = dataGet['data']
        meta = dataGet['meta']

        dataSplit = data.split('\n')
        term.clear()
        for(let i = 0; i < dataSplit.length; i++){
            term.echo(dataSplit[i])
        }

        if (meta['end']){
            stopAction()
            term.echo()
            term.echo(endline)

            scriptRuning = false
            return
        }
    }
}

function update(){
    if (scriptRuning) {
        getConsole();
    }
}

function timer(){
    update();
    setTimeout(timer, 1000);
}


window.onload = () => {
    timer()
}