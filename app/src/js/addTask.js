formFields = ['title', 'description', 'sum', 'deadline', 'city', 'street', 'house'];

function save() {
    
    let data = getFormData()

    if (data.isValidate()) {
        $.ajax({
            url: '/api/bill',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: "application/json",
            success: function(data) {
                if (data.status === 'done') {
                    clearForm();
                }
                alert(data.message);
            }
        });
    } else {
        alert('Там же пусто');
    }
}

function getFormData() {
    let res = {};
    formFields.forEach((id) => {
        res[id] = $(`#${id}`).val();
    });
    res.isValidate = function() {
       return this.title && this.description && this.sum;
    }
    return res;
}

function clearForm() {
    formFields.forEach((id) => {
        $(`#${id}`).val('');
    });
}

function edit() {
    $('#edit').toggle();
    $('#read').toggle();
}