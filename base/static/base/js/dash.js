// ------------------------ OBTENEMOS LOS MODALES EN VARIABLES ------------------------
const salesModal = $("#salesModal");
const rankingModal = $("#rankingModal");
const alertModal = $("#alertModal");

// ------------------------ FUNCION PARA CERRAR EL MODAL ------------------------
function closeModal(modal) {
  modal[0].classList.remove("show");
}

// ------------------------ FUNCION PARA CERRAR EL MODAL ------------------------
function openModal(modal) {
  console.log(modal[0]);
  modal[0].classList.add("show");
}
