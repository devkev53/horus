const inputImg = document.querySelector(".node-input-image");
const previewImg = document.querySelector("#preview_img");

previewImg.addEventListener("click", () => {
  inputImg.click();
});

if (previewImg !== null) {
  inputImg.addEventListener("change", (e) => {
    if (e.target.files[0]) {
      const reader = new FileReader(e.target.files[0]);
      reader.onload = (e) => {
        previewImg.setAttribute("src", e.target.result);
      };
      reader.readAsDataURL(e.target.files[0]);
    }
  });
}
