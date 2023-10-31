// ------------------------ OBTENEMOS EL MODAL EN UNA VARIABLE ------------------------
const detailModal = document.querySelector("#detailModal");

// ------------------------ FUNCION PARA CERRAR EL MODAL ------------------------
function closeModal(detailModal) {
  detailModal.classList.remove("show");
}

// ------------------------ CREACION DE LOS BOTONES PARA LA TABLA ------------------------
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
const printBtnHtml = (id) => {
  let url = `${window.location.pathname}invoice/${id}`;
  return `<a href="${url}" target="_blank" class="table-btn bg-zinc-800" rel="view"><i class="fas fa-print"></i></a>`;
};

// ------------------------ CREACION DE LA TABLA DE VENTAS ------------------------
let saleTbl = $("#sales-table").DataTable({
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
    { data: "time" },
    { data: "serie" },
    { data: "dte" },
    { data: "client_id" },
    { data: "subtotal" },
    { data: "discount" },
    { data: "total" },
    { data: "id" },
  ],
  columnDefs: [
    {
      target: [2, 3],
      render: function (data, type, row) {
        if (data === null) {
          return `<p>N/I</p>`;
        } else {
          return `<p>${data}</p>`;
        }
      },
    },
    {
      target: [4],
      render: function (data, type, row) {
        return `<p>${data.get_full_name}</p>`;
      },
    },
    {
      target: [5, 6, 7],
      render: function (data, type, row) {
        return `Q. ${parseFloat(data).toFixed(2)}`;
      },
    },
    {
      target: [8],
      render: function (data, type, row) {
        return `<div class="flex gap-4 justify-center">${viewBtnHtml} ${editBtnHtml(
          data
        )} ${deleteBtnHtml(data)} ${printBtnHtml(data)} </div>`;
      },
    },
  ],
});

// ------------------------ CREACION DE LA TABLA CON LISTADO DE DETALLES DE VENTA ------------------------
function getDetailSaleTable(data) {
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
      { data: "total" },
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
  });
}
// ------------------------ ABRIR EL MODAL CON LOS DETALLES DE LA VENTA ------------------------
$("#sales-table tbody").on("click", 'button[rel="view"]', function () {
  let tr = saleTbl.cell($(this).closest("td, li")).index();
  let data = saleTbl.row(tr.row).data();
  getDetailSaleTable(data);
  detailModal.classList.add("show");
});

// ------------------------ BOTTON PARA HACER EL POST Y OBTENER LA FACTURA ------------------------
$("#sales-table tbody").on("click", 'button[rel="invoice"]', function () {
  let tr = saleTbl.cell($(this).closest("td, li")).index();
  let data = saleTbl.row(tr.row).data();
  let url = `${window.location.pathname}invoice/${data.id}`;
  let params = new FormData();
  params.append("pk", data.id);
  get_invoice(url, params);
});
