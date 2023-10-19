const clientForm = document.querySelector("#client_form");

const cb = () => {
  location.href = redirectUrl;
};

clientForm.addEventListener("submit", (e) => {
  e.preventDefault();
  let params = new FormData(clientForm);
  // params.append("action");
  submitOption(
    window.location.pathname,
    params,
    cb,
    "Desea crear el cliente",
    "Ingresar Cliente",
    "fas fa-save",
    "blue"
  );
});
