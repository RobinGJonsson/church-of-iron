$("#modal-btn").click(function () {
    $(".map-cover").addClass("d-none");
    initMap();
});

// Adding amenites
$(".add-amenities").hide();
$(".add-amenities-btn").click(function () {
    $(".add-amenities").toggle();
});

$(".image-form-container").hide();
$(".add-image").click(function () {
    $(".image-form-container").toggle();
});

// Display modal upon submit, asking if they want to proceed
$(".open-modal").click(function (event) {
    $(".modal").show();
    $(".close-btn").click(function () {
        $(".modal").hide();
    });
});

// Membership
$(".show-membership").click(function (e) {
    let membershipId = $(this).data("id");
    let targetMemberhsip = `membership-details-${membershipId}`;
    $(`.${targetMemberhsip}`).toggleClass("d-none");
});
