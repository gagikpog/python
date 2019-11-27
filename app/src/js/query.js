
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












