const viewBtnHtml =
  '<button class="table-btn" rel="view"><i class="fas fa-info-circle"></i></button>';
const editBtnHtml = (id) => {
  let editUrl = `${window.location.pathname}${id}`;
  return `<a href="${editUrl}" class="table-btn btn-edit" rel="view"><i class="fas fa-edit"></i></a>`;
};
const deleteBtnHtml = (id) => {
  let deleteUrl = `${window.location.pathname}delete/${id}`;
  return `<a href="${deleteUrl}" class="table-btn btn-delete" rel="view"><i class="fas fa-trash-alt"></i></a>`;
};
const payBtnHtml = (id) => {
  // let deleteUrl = `${window.location.pathname}delete/${id}`;
  let deleteUrl = `/`;
  return `<button class="table-btn bg-green-400" rel="payList"><i class="fas fa-coins"></i></button>`;
};
const historyBtnHtml = (id) => {
  let url = `${window.location.pathname}detail/${id}`;
  return `<a href="${url}" class="table-btn bg-zinc-800" rel="view"><i class="fas fa-history"></i></a>`;
};

// ------------ SE OBTIENEN LAS VARIABLES A USARSE ---------------
const paysListModal = document.querySelector("#payList");
const detailModal = document.querySelector("#detailModal");
const btnCloseModal = document.querySelector(".btnClose-modal");
const btnAddPay = document.querySelector("#addPay");
const addPayModal = document.querySelector("#addPayModal");
const paymentForm = document.querySelector("#paymentForm");
const addPaymentBtnSubmit = document.querySelector("#addPaymentBtnSubmit");
var pagoInfo = "";
var payId = "";

// ------------------------ FUNCION PARA CERRAR EL MODAL ------------------------
function closeModal(modal) {
  modal.classList.remove("show");
}

function closeModalClickOutput(e) {
  e.target.classList.remove("show");
}

// ------------------- FUNCION ADD PAY CLICK -------------------
btnAddPay.addEventListener("click", function () {
  // Cerrar Modal Listaode Pagos
  paysListModal.classList.remove("show");
  document.querySelector(".payInstance").innerHTML = pagoInfo;

  setTimeout(() => {
    addPayModal.classList.add("show");
  }, 300);
});

// ------------------- DEFINICION DE LA TABLA COMPRAS -------------------
let tblBuys;

btnCloseModal.addEventListener("click", function () {
  detailModal.classList.remove("show");
});

tblBuys = $("#buys-table").DataTable({
  responsive: true,
  autoWidth: false,
  destroy: true,
  deferRender: true,
  language: changeLanguageDataTable,
  ajax: {
    url: window.location.pathname,
    type: "POST",
    data: {
      action: "searchData",
    },
    dataSrc: "",
  },
  columns: [
    { data: "date" },
    { data: "serie" },
    { data: "reference" },
    { data: "provider_id" },
    { data: "is_paid" },
    { data: "chek_payment" },
    { data: "total" },
    { data: "id" },
  ],
  order: [[0, "desc"]],
  columnDefs: [
    {
      target: [1, 2],
      render: function (data, type, row) {
        if (data === null) {
          return `<p>N/I</p>`;
        } else {
          return `<p>${data}</p>`;
        }
      },
    },
    {
      target: [3],
      render: function (data, type, row) {
        return `<p>${data.company_name}</p>`;
      },
    },
    {
      target: [4],
      render: function (data, type, row) {
        if (row.chek_payment) {
          return `<i class="fas fa-check-circle text-green-500 text-4xl"></i>`;
        } else {
          return `<i class="fas fa-times-circle text-red-700 text-4xl"></i>`;
        }
      },
    },
    {
      target: [5, 6],
      render: function (data, type, row) {
        return `Q. ${parseFloat(data).toFixed(2)}`;
      },
    },
    {
      target: [7],
      render: function (data, type, row) {
        return `<div class="flex gap-4 justify-center">${viewBtnHtml} ${editBtnHtml(
          data
        )} ${deleteBtnHtml(data)} ${payBtnHtml(data)} ${historyBtnHtml(
          data
        )} </div>`;
      },
    },
  ],
});

// ------------------- EVENTO CLIC SOBRE EL BOTON LISTADO DE PAGOS MODAL ---------------------------
$("#buys-table tbody").on("click", 'button[rel="payList"]', function () {
  let tr = tblBuys.cell($(this).closest("td, li")).index();
  let data = tblBuys.row(tr.row).data();
  pagoInfo = `${data.date} - ${data.provider_id.company_name} - Q. ${data.total}`;
  payId = data.id;
  document.querySelector(".payInfo").innerHTML = pagoInfo;

  $("#tblPays").DataTable({
    responsive: true,
    autoWidth: false,
    destroy: true,
    deferRender: true,
    language: changeLanguageDataTable,
    ajax: {
      url: window.location.pathname,
      type: "POST",
      data: {
        action: "search_pays",
        id: payId,
      },
      dataSrc: "",
    },
    language: changeLanguageDataTable,
    columns: [
      { data: "id" },
      { data: "date" },
      { data: "payment_type" },
      { data: "document" },
      { data: "total" },
    ],
    columnDefs: [
      {
        targets: [0],
        render: function (data, type, row, meta) {
          return meta.row;
        },
      },
      {
        target: [3],
        render: function (date, type, row) {
          if (row.chek_payment) {
            return `<i class="fas fa-check-circle text-green-500 text-4xl"></i>`;
          } else {
            return `<i class="fas fa-times-circle text-red-700 text-4xl"></i>`;
          }
        },
      },
      {
        targets: [4],
        render: function (data, type, row, meta) {
          return `Q. ${parseFloat(data).toFixed(2)}`;
        },
      },
    ],
    pageLength: 5,
    lengthMenu: [5, 10, 20, "Todos"],
  });

  paysListModal.classList.add("show");
});

// ------------------- EVENTO CLIC SOBRE EL BOTON DETALLE COMPRA ---------------------------
$("#buys-table tbody").on("click", 'button[rel="view"]', function () {
  let tr = tblBuys.cell($(this).closest("td, li")).index();
  let data = tblBuys.row(tr.row).data();

  $("#tbl-detail").DataTable({
    responsive: true,
    autoWidth: false,
    destroy: true,
    deferRender: true,
    rowCallback: function (row, data) {
      $(row).find('input[name="quantity"]');
    },
    ajax: {
      url: window.location.pathname,
      type: "POST",
      data: {
        action: "search_details",
        id: data.id,
      },
      dataSrc: "",
    },
    language: changeLanguageDataTable,
    columns: [
      { data: "id" },
      { data: "product_id.name" },
      { data: "product_id.image" },
      { data: "product_id.price_sale" },
      { data: "quantity" },
      { data: "sub_total" },
    ],
    columnDefs: [
      {
        targets: [3, 5],
        render: function (data, type, row) {
          return `Q. ${parseFloat(data).toFixed(2)}`;
        },
      },
      {
        target: [2],
        render: function (data, type, row) {
          return `<img class="w-16 h-16 rounded-xl" src="${data}"/>`;
        },
      },
    ],
    pageLength: 5,
    lengthMenu: [5, 10, 20, "Todos"],
  });
  detailModal.classList.add("show");
});

// ------------------- EVENTO SUBMIT DEL PAGO ---------------------------
addPaymentBtnSubmit.addEventListener("click", () => {
  document.querySelector("#id_buy_id").value = payId;
  let params = new FormData(paymentForm);
  params.append("action", "addPay");

  submit_with_axios(
    window.location.pathname,
    "Notificacion",
    "Agregar pago",
    params,
    () => {
      window.location.reload();
    }
  );
});
