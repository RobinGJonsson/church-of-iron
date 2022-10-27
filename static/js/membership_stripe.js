// Get the public key to initialize stripe
fetch("/checkout/config/")
    .then((result) => {
        return result.json();
    })
    .then((data) => {
        const stripe = Stripe(data.publicKey);

        // Wait for the form submit button to be clicked
        $("#submit-btn").click(function (e) {
            // Get the checkout session ID
            // The session ID is used to populate the checkout
            fetch("/checkout/create-checkout-session/")
                .then((result) => {
                    return result.json();
                })
                // Go to payment this is prebuilt but can be custom
                .then((data) => {
                    console.log(data);
                    return stripe.redirectToCheckout({
                        sessionId: data.sessionId,
                    });
                })
                .then((res) => {
                    console.log(res);
                });
        });
    });
