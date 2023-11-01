// Funcion de mensaje de alerta y accion
const alert_action = (title, text, cb) => {
  Swal.fire({
    icon: "warning",
    title: title,
    html: text,
    confirmButtonColor: "#759AA5",
    cancleButtonColor: "#52525b",
    showCancelButton: true,
    confirmButtonText: "Si, Eliminar!",
    cancleButtonText: "No, Cancelar",
  }).then(async (result) => {
    if (result.isConfirmed) {
      cb();
    }
  });
};

// Funcion de alert y OK
const myAlert = (title, text) => {
  Swal.fire({
    icon: "warning",
    title: title,
    html: text,
    confirmButtonColor: "#759AA5",
    confirmButtonText: "Si, Eliminar!",
  });
};

const myError = (title, text) => {
  Swal.fire({
    icon: "error",
    title: title,
    html: text,
    confirmButtonColor: "#759AA5",
    confirmButtonText: "OK",
  });
};

// funcion que realiza el post con axios
async function postAxios(urlPath, params, callback) {
  let response = await axios.post(urlPath, params);
  if (!response.data.hasOwnProperty("error")) {
    callback(response.data);
    return false;
  }
  let msgError = error_alert(errorObj);
  myErrorSwal("Error", errorObj);
}

// function que realiza la inactivacion (Delete) con axios
async function deleteAxios(urlPath) {
  let response = await axios.post(urlPath, {
    Headers: {
      "X-CSRF-TOKEN": crf,
    },
  });
  if (!response.data.hasOwnProperty("error")) {
    location.href = redirectUrl;
    return false;
  }
  let msgError = error_alert(error);
  myErrorSwal("Error", msgError);
}

const myErrorSwal = (title, text) =>
  Swal.fire({
    icon: "error",
    title: "Error",
    html: text,
    confirmButtonColor: "#52525b",
  });

// Funcion para convertir los errores en una lista html
function error_to_html(obj) {
  // console.log(obj);
  let html = "";
  if (typeof obj === "object") {
    html = '<ul class="w-full justify-items-center" style="">';
    Object.entries(obj).forEach(([key, value]) => {
      html +=
        "<li class='mb-2'>" +
        "<span class='font-bold text-red-900'>" +
        key +
        "</span>" +
        ": " +
        value +
        "</li>";
    });
    html += "</ul>";
  } else {
    html = "<p>" + obj + "</p>";
  }
  return html;
}

// Funcion que muestra la alerta para la cracion
const submitOption = (
  urlPath,
  params,
  callback,
  content,
  title,
  icon,
  color
) => {
  Swal.fire({
    type: color,
    title: title,
    text: content,
    icon: "info",
    typeAnimated: true,
    confirmButtonColor: "#759AA5",
    cancleButtonColor: "#52525b",
    showCancelButton: true,
    confirmButtonText: "Si, Registrar!",
    cancleButtonText: "No, Cancelar",
  }).then(async (result) => {
    if (result.isConfirmed) {
      postAxios(urlPath, params, callback);
    }
  });
};

// Function delete
const confirmDelete = (id, object, crf) =>
  Swal.fire({
    icon: "warning",
    title: "Eliminar",
    html: `Seguro que desea elminar ${object}`,
    typeAnimated: true,
    confirmButtonColor: "#759AA5",
    cancleButtonColor: "#52525b",
    showCancelButton: true,
    confirmButtonText: "Si, Eliminar!",
    cancleButtonText: "No, Cancelar",
  }).then(async (result) => {
    if (result.isConfirmed) {
      let deleteUrl = `${location}${id}`;
      deleteAxios(deleteUrl);
    }
  });

// Funcion que permite abrir el modal para la eliminacion logica de un objeto
function openDeleteModal(id, client) {
  const deleteClient = client;
  var cliendId = id;
  const deleteModal = document.querySelector("#modal-delete");
  deleteModal.classList.toggle("show");
}

function confirmDeleteBtn(id) {
  let deleteUrl = `${location}delete/${id}/`;
  postAxios(deleteUrl, {});
}

// Funcion que cierra el modal que se usa para la eliminacion logica de un objeto
function closeDeleteModal() {
  const deleteModal = document.querySelector("#modal-delete");
  deleteModal.classList.remove("show");
}

// SideMenu Links
const linksItem = document.querySelectorAll(".nav-link");

function active_link() {
  let path = location.pathname.split("/");
  console.log(path);
  if (path.includes("clients")) {
    linksItem.forEach((link) => {
      if (link.classList.contains("clients")) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  } else if (path.includes("dashboard")) {
    linksItem.forEach((link) => {
      if (link.classList.contains("dashboard")) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  } else if (path.includes("sales")) {
    linksItem.forEach((link) => {
      if (link.classList.contains("sales")) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  } else if (path.includes("categories") || path.includes("category")) {
    linksItem.forEach((link) => {
      if (link.classList.contains("categories")) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  } else if (path.includes("providers")) {
    linksItem.forEach((link) => {
      if (link.classList.contains("providers")) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  } else if (path.includes("products")) {
    linksItem.forEach((link) => {
      if (link.classList.contains("products")) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  } else if (path.includes("buys")) {
    linksItem.forEach((link) => {
      if (link.classList.contains("buys")) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  } else if (path.includes("employees")) {
    linksItem.forEach((link) => {
      if (link.classList.contains("employees")) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  }
}

active_link();

// NavBar Links
const navLinkItems = document.querySelectorAll(".public-nav-link");

function active_public_link() {
  let path = location.pathname.split("/");
  if (path.includes(path[1] === "")) {
    navLinkItems.forEach((link) => {
      if (link.classList.contains("inicio")) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  } else if (path.includes("conocenos") || path.includes("category")) {
    navLinkItems.forEach((link) => {
      if (link.classList.contains("conocenos")) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  } else if (path.includes("contacto")) {
    navLinkItems.forEach((link) => {
      if (link.classList.contains("contacto")) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  }
}
active_public_link();

const submit_with_axios = (url, title, text, params, callback) => {
  return Swal.fire({
    icon: "info",
    title: title,
    text: text,
    confirmButtonColor: "#759AA5",
    cancleButtonColor: "#52525b",
    showCancelButton: true,
    confirmButtonText: "Si, Guardar!",
    cancleButtonText: "No, Cancelar",
  }).then(async (result) => {
    if (result.isConfirmed) {
      let response = await axios.post(url, params);
      console.log(response.status);
      console.log(response.data.hasOwnProperty("error"));
      if (!response.data.hasOwnProperty("error")) {
        callback();

        return response.data;
      } else {
        let errorHtml = error_to_html(response.data.error);
        console.log(errorHtml);
        myError("Error", errorHtml);
      }
    }
  });
};
