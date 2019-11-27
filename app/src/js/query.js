

function run() {
    const path = $('#path').val();
    const select = $('#sel')[0].value;
    const text = $('#textArea').val();
    
    $.ajax({
        url: path,
        type: select,
        data: text,
        contentType: "application/json",
        success: function(data) {
            const jsonData = JSON.stringify(data);
            $('#tArea').val(jsonData);
        }
    });

}




function updateUser() {
    const path = '/api/user/2';
    const select = "PUT";
    const text = {'name':'Ycpex'};
    
    $.ajax({
        url: path,
        type: select,
        data: text,
        contentType: "application/json",
        success: function(data) {
            const jsonData = JSON.stringify(data);
        }
    });

}


