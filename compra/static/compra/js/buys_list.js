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
  return `<a href="${deleteUrl}" class="table-btn bg-green-400" rel="view"><i class="fas fa-coins"></i></a>`;
};
const detailModal = document.querySelector("#detailModal");
const btnCloseModal = document.querySelector(".btnClose-modal");

let tblBuys;

btnCloseModal.addEventListener("click", function () {
  detailModal.classList.remove("show");
});

tblBuys = $("#buys-table").DataTable({
  responsive: true,
  autoWidth: false,
  destroy: true,
  deferRender: true,
  // data:
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
    { data: "total" },
    { data: "id" },
  ],
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
        if (data) {
          return `<i class="fas fa-check-circle text-green-200 text-4xl"></i>`;
        } else {
          return `<i class="fas fa-times-circle text-red-700 text-4xl"></i>`;
        }
      },
    },
    {
      target: [5],
      render: function (data, type, row) {
        return `Q. ${parseFloat(data).toFixed(2)}`;
      },
    },
    {
      target: [6],
      render: function (data, type, row) {
        return `<div class="flex gap-4 justify-center">${viewBtnHtml} ${editBtnHtml(
          data
        )} ${deleteBtnHtml(data)} ${payBtnHtml(data)} </div>`;
      },
    },
  ],
});

$("#buys-table tbody").on("click", 'button[rel="view"]', function () {
  let tr = tblBuys.cell($(this).closest("td, li")).index();
  let data = tblBuys.row(tr.row).data();
  console.log(data);

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
        targets: [5],
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
  detailModal.classList.add("show");
});
