// alert("Entro al javascript");
$("#id_category_id").select2();
$("#id_provider_id").select2();

$("#productsTbl").dataTable({
  language: changeLanguageDataTable,
  pageLength: 5,
  lengthMenu: [
    [3, 5, 10, 20, -1],
    [3, 5, 10, 20, "Todos"],
  ],
});
