// funcion que realiza el post con axios
async function postAxios(urlPath, params, callback) {
  let response = await axios.post(urlPath, params);
  if (!response.data.hasOwnProperty("error")) {
    callback(response.data);
    return false;
  }
  let msgError = error_alert(response.data.error);
  myErrorSwal("Error", msgError);
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
  let msgError = error_alert(response.data.error);
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
function error_alert(obj) {
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

const linksItem = document.querySelectorAll(".nav-link");

function active_link() {
  const path = location.pathname.split("/");
  if (path.includes("clients")) {
    linksItem.forEach((link) => {
      if (link.classList.contains("clients")) {
        link.classList.add("active");
        console.log("Activar link Clientes");
      } else {
        link.classList.remove("active");
      }
    });
  } else if (path.includes("categories") || path.includes("category")) {
    linksItem.forEach((link) => {
      if (link.classList.contains("categories")) {
        link.classList.add("active");
        console.log("Activar link Categorias");
      } else {
        link.classList.remove("active");
      }
    });
  } else if (path.includes("providers")) {
    linksItem.forEach((link) => {
      if (link.classList.contains("providers")) {
        link.classList.add("active");
        console.log("Activar link Proveedores");
      } else {
        link.classList.remove("active");
      }
    });
  } else if (path.includes("products")) {
    linksItem.forEach((link) => {
      if (link.classList.contains("products")) {
        link.classList.add("active");
        console.log("Activar link Productos");
      } else {
        link.classList.remove("active");
      }
    });
  }
}

active_link();
