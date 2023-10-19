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
