function updateUser() {

    let user_id = document.getElementById("userId").innerHTML
    const path = '/api/user/' + user_id;
    const select = "PUT";
    const text = {id:4, name: $('#name').val(),sname: $('#sname').val(),
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