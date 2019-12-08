function updateUser() {

    let user_id = document.getElementById("userId").innerHTML
    const path = '/api/user/' + user_id;
    const select = "PUT";
    const text = {id: user_id, name: $('#name').val(),sname: $('#sname').val(),
    pname: $('#pname').val()};
    let name = document.getElementById('name');
    let sname = document.getElementById('sname');
    let pname = document.getElementById('pname');


    if (document.getElementById("pen").style.backgroundPositionX == "-42px") {
        
        document.getElementById("pen").style.backgroundPositionX = "0px";
        document.getElementById("user-update__Input").style.display = "none";
        document.getElementById("user-update__Name").style.display = "flex";

        $.ajax({
            url: path,
            type: select,
            data: JSON.stringify(text),
            contentType: "application/json",
            success: function(data) {
                const jsonData = JSON.stringify(data);
            }
        });
        document.getElementById("nameResult").innerHTML = name.value;
        document.getElementById("snameResult").innerHTML = sname.value;
        document.getElementById("pnameResult").innerHTML = pname.value;
    }
    else {
        document.getElementById("pen").style.backgroundPositionX = "-42px" 
        document.getElementById("user-update__Input").style.display = "flex";
        document.getElementById("user-update__Name").style.display = "none";
    };
}


function spoilerShow (number,countElem) {
    let tumbler = false;
    return function() {
        let count = document.getElementById('spoilerParent_'+number).children.length;
        let parent = document.getElementById('totalParent_'+number);
        let height = parent.offsetHeight;
        let text = document.getElementById('buttonMore_'+number);
        let multiple = Math.ceil(count / countElem);
        if (tumbler == false) {
                text.innerText = 'Скрыть';
                parent.style.height = (height*multiple)+'px';
                tumbler = true;
            }
        else {
            text.innerText = 'Показать еще'
            parent.style.height = (height/multiple)+'px'
            tumbler = false;
            }     
        return  tumbler   
    }
   
}

var spoilerShowZero = spoilerShow(0,5);
var spoilerShowOne = spoilerShow(1,3);


// для загрузки изображения
function sse() {
    var source = new EventSource('/stream');
    source.onmessage = function(e) {
        if (e.data == '')
            return;
        var data = $.parseJSON(e.data);

        var src = data.src;
        src = '/src/' + src.substring(src.indexOf('data/'));
        $('#userImage').attr('src', src);
        $('#userIcon_header').attr('src', src);

        updateImage(src);
        var progressbar = $('#progressbar');
        progressbar.hide();
    };
}

function file_select_handler(to_upload) {
    var progressbar = $('#progressbar');
    var xhr = new XMLHttpRequest();
    xhr.upload.addEventListener('loadstart', function(e1){
        progressbar.show();
    });
    xhr.open('POST', '/imageLoad', true);
    xhr.send(to_upload);
};

function handle_hover(e) {
    e.originalEvent.stopPropagation();
    e.originalEvent.preventDefault();
    e.target.className = (e.type == 'dragleave' || e.type == 'drop') ? '' : 'hover';
}

$('#drop').bind('drop', function(e) {
    handle_hover(e);
    if (e.originalEvent.dataTransfer.files.length < 1) {
        return;
    }
    file_select_handler(e.originalEvent.dataTransfer.files[0]);
}).bind('dragenter dragleave dragover', handle_hover);
$('#file').change(function(e){
    file_select_handler(e.target.files[0]);
    e.target.value = '';
});
sse();

var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-510348-17']);
_gaq.push(['_trackPageview']);

(function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();


function updateImage(imageName) {

    var image = imageName.substring(imageName.indexOf('data/') + 4);
    const text = JSON.stringify({id: currentUserData.id, image: image});
    
    $.ajax({
        url: '/api/user/' + currentUserData.id,
        type: 'PUT',
        data: text,
        contentType: "application/json",
        success: function(data) {
            const jsonData = JSON.stringify(data);
        }
    });
}
