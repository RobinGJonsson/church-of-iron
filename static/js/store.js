function handelEnableDisable(itemId) {
    let currentValue = parseInt($(`#id_qty_${itemId}`).val());
    let minusDisabled = currentValue < 2;
    let plusDisabled = currentValue > 98;
    $(`#decrement-qty_${itemId}`).prop("disabled", minusDisabled);
    $(`#increment-qty_${itemId}`).prop("disabled", plusDisabled);
}

// Call handleEnableDisable function on all qty-inputs when page loads
let allQtyInputs = $(".qty_input");
for (input of allQtyInputs) {
    let itemId = $(input).data("item_id");
    handelEnableDisable(itemId);
}

// Run handleEnable Disable every time the value changes
$(".qty_input").change(function () {
    let itemId = $(this).data("item_id");
    handelEnableDisable(itemId);
});

// Increment quantity
$(".increment-qty").click(function (e) {
    e.preventDefault();
    let closestInput = $(this).closest(".input-group").find(".qty_input")[0];
    let currentValue = parseInt($(closestInput).val());
    $(closestInput).val(currentValue + 1);
    let itemId = $(this).data("item_id");
    handelEnableDisable(itemId);
});

// Decrement quantity
$(".decrement-qty").click(function (e) {
    e.preventDefault();
    let closestInput = $(this).closest(".input-group").find(".qty_input")[0];
    let currentValue = parseInt($(closestInput).val());
    $(closestInput).val(currentValue - 1);
    let itemId = $(this).data("item_id");
    handelEnableDisable(itemId);
});
