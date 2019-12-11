formFields = [
  "title",
  "description",
  "sum",
  "deadline",
  "city",
  "street",
  "house",
  "status"
];

function save(id) {
  let updateData = getFormData();
  const method = id ? "PUT" : "POST";

  if (id) {
    updateData.id = id;
  }

  if (updateData.isValidate()) {
    $.ajax({
      url: "/api/bill",
      type: method,
      data: JSON.stringify(updateData),
      contentType: "application/json",
      success: function(data) {
        if (data.status === "done") {
          if (!id) {
            clearForm();
          } else {
            updateForm(updateData);
          }
        }
        alert(data.message);
      }
    });
  } else {
    alert("Там же пусто");
  }
}

function getFormData() {
  let res = {};
  formFields.forEach(id => {
    res[id] = $(`#${id}`).val();
  });
  res.isValidate = function() {
    return this.title && this.description && this.sum;
  };
  return res;
}

function clearForm() {
  formFields.forEach(id => {
    $(`#${id}`).val("");
  });
}

function edit(id) {
  $("#edit").toggle();
  $("#read").toggle();
}

function updateForm(updateData) {
  let keys = Object.keys(updateData);
  keys.forEach(key => {
    item = document.querySelector(`#readOnly-${key}`);
    if (item) {
      item.textContent = updateData[key];
    }
  });

  $("#hidebtn").css(
    "display",
    updateData.status === "Опубликовано" ? "block" : "none"
  );
  $("#publishbtn").css(
    "display",
    updateData.status === "Скрыто" ? "block" : "none"
  );
  $("#donebtn").css(
    "display",
    updateData.status === "Выполняется" ? "block" : "none"
  );
  $("#deletebtn").css(
    "display",
    updateData.status === "Выполняется" || updateData.status === "Выполнено"
      ? "none"
      : "block"
  );
}

function publish(id, status) {
  if (id) {
    const updateData = {
      id,
      status
    };
    const taskName = document
      .querySelector("#readOnly-title")
      .textContent.trim();
    const description = `Вы действительно хотите удалить задачу "${taskName}"`;
    if (status === "Удалено") {
      showConfirm("Сообщение", description).then(answer => {
        if (answer) {
          query();
        }
      });
    } else {
      query();
    }
    function query() {
      $.ajax({
        url: "/api/bill",
        type: "PUT",
        data: JSON.stringify(updateData),
        contentType: "application/json",
        success: function(data) {
          if (data.status === "done") {
            if (id) {
              updateForm(updateData);
            }
            if (status === "Удалено") {
              window.location.href = "/tasks";
            }
          }
        }
      });
    }
  }
}

function toResponse(taskId) {
  if (taskId) {
    const updateData = {
      taskId
    };

    $.ajax({
      url: "/task-response",
      type: "POST",
      data: JSON.stringify(updateData),
      contentType: "application/json",
      success: function(data) {
        if (data.status === "done") {
          if (taskId) {
            alert("Отклик успешно отправлен!");
          }
        } else {
          showConfirm("Ошибка", data.message, { MBOK: true });
        }
      }
    });
  }
}

function accept(userId, taskId) {
  if (userId) {
    const updateData = {
      userId,
      taskId
    };

    $.ajax({
      url: "/task-accept",
      type: "POST",
      data: JSON.stringify(updateData),
      contentType: "application/json",
      success: function(data) {
        if (data.status === "done") {
          if (userId) {
            alert("sdad");
          }
        } else {
          showConfirm("Ошибка", data.message, { MBOK: true });
        }
      }
    });
  }
}
