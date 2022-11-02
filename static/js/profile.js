let inputItems = $(".input-item");
let updateBtn = $(".update-btn");
let submitBtn = $(".submit-btn");

inputItems.prop("disabled", true);
inputItems.css({ "background-color": "#fff" });

submitBtn.hide();

// Unmute input fileds when update  button is clicked
updateBtn.click(function () {
    $(this).hide();
    $(".input-item").prop("disabled", false);
    submitBtn.show();
});
