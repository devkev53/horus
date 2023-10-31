// ------------------------ OBTENEMOS LOS MODALES EN VARIABLES ------------------------
const salesModal = $("#salesModal");
const rankingModal = $("#rankingModal");
const alertModal = $("#alertModal");

// ------------------------ FUNCION PARA CERRAR EL MODAL ------------------------
function closeModal(modal) {
  console.log(modal[0]);
  modal[0].classList.remove("show");
}

function closeModalClickOutput(e) {
  e.target.classList.remove("show");
}

// ------------------------ FUNCION PARA CERRAR EL MODAL ------------------------
function openModal(modal) {
  modal[0].classList.add("show");
}

$("#tbl-detail").DataTable({
  responsive: true,
  autoWidth: false,
  destroy: true,
  deferRender: true,
  language: changeLanguageDataTable,
});
$("#tbl-ranking").DataTable({
  responsive: true,
  autoWidth: false,
  destroy: true,
  deferRender: true,
  language: changeLanguageDataTable,
});
$("#tbl-alert").DataTable({
  responsive: true,
  autoWidth: false,
  destroy: true,
  deferRender: true,
  language: changeLanguageDataTable,
});
