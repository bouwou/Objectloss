$(document).ready(function () {

    // Step show event
    $("#smartwizard").on("showStep", function (e, anchorObject, stepNumber, stepDirection, stepPosition) {
        //alert("You are on step "+stepNumber+" now");
        if (stepPosition === 'first') {
            $("#prev-btn").addClass('disabled');
        } else if (stepPosition === 'final') {
            $("#next-btn").addClass('disabled');
        } else {
            $("#prev-btn").removeClass('disabled');
            $("#next-btn").removeClass('disabled');
        }
    });

    // Toolbar extra buttons
    var btnFinish = $('<button></button>').text('Finish')
        .addClass('btn btn-info')
        .on('click', function () {
            //alert('Finish Clicked');
            var state = true;
            var ev0 = document.querySelector("#object-check-form");
            var ev1 = document.querySelector("#contact-check-form");
            var ev2 = document.querySelector("#personal-check-form");
            var validation = Array.prototype.filter.call(ev0, function (form) {
                if (ev0.checkValidity() === false) {
                    state = false;
                }
                ev0.classList.add('was-validated');
            });
            var validation = Array.prototype.filter.call(ev1, function (form) {
                if (ev1.checkValidity() === false) {
                    state = false;
                }
                ev1.classList.add('was-validated');
            });
            var validation = Array.prototype.filter.call(ev2, function (form) {
                if (ev2.checkValidity() === false) {
                    state = false;
                }
                ev2.classList.add('was-validated');
            });
            if (state) {
                var url = $('#step-1').attr('data');
                var picker = $('.date_naissance').pickadate('picker');
                var picker1 = $('.date_perte').pickadate('picker');
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: {
                        date_naissance: picker.get('select', 'yyyy-mm-dd'),
                        type_objet: $('#type_select').val(),
                        autre_type: $('.autre_type').val(),
                        nom_objet: $('.nom_objet').val(),
                        nom_prop: $('.nom_prop').val(),
                        prenom_prop: $('.prenom_prop').val(),
                        telephone: $('.phone1').val(),
                        email: $('.email').val(),
                        lieu_perte: $('.lieu_perte').val(),
                        date_perte: picker1.get('select', 'yyyy-mm-dd'),
                        lieu_residence: $('.lieu_residence').val(),
                        cni: $('.cni').val(),
                        passeport: $('.passeport').val(),
                        description: $('.description').val(),
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    },
                    dataType: 'json',
                    success: function (data) {
                        toastr.success("", data.response, {
                            showMethod: "slideDown",
                            hideMethod: "slideUp",
                            timeOut: 2e3,
                            progressBar: !0
                        })
                        init_form();
                        $('#smartwizard').smartWizard("reset");
                        ev0.classList.remove('was-validated');
                        ev1.classList.remove('was-validated');
                        ev2.classList.remove('was-validated');
                    }
                })
            } else {
                toastr.error("Erreur Formulaire", "Tous les champs requis n'ont pas ete rempli", {
                    showMethod: "slideDown",
                    hideMethod: "slideUp",
                    timeOut: 2e3,
                    progressBar: !0
                })
            }
        });
    var btnCancel = $('<button></button>').text('Cancel')
        .addClass('btn btn-danger')
        .on('click', function () {
            $('#smartwizard').smartWizard("reset");
            var ev0 = document.querySelector("#object-check-form");
                // Loop over them and prevent submission
                var validation = Array.prototype.filter.call(ev0, function (form) {
                    ev0.classList.remove('was-validated');
                });
                var ev1 = document.querySelector("#contact-check-form");
                // Loop over them and prevent submission
                var validation = Array.prototype.filter.call(ev1, function (form) {
                    ev1.classList.remove('was-validated');
                });
                var ev2 = document.querySelector("#personal-check-form");
                // Loop over them and prevent submission
                var validation = Array.prototype.filter.call(ev2, function (form) {
                    ev2.classList.remove('was-validated');
                });
        });


    // Smart Wizard
    $('#smartwizard').smartWizard({
        selected: 0,
        theme: 'arrows',
        transitionEffect: 'fade',
        showStepURLhash: true,
        toolbarSettings: {
            toolbarPosition: 'both',
            toolbarButtonPosition: 'end',
            toolbarExtraButtons: [btnFinish, btnCancel]
        }
    });


    // External Button Events
    $("#reset-btn").on("click", function () {
        // Reset wizard
        $('#smartwizard').smartWizard("reset");
        return true;
    });

    $("#prev-btn").on("click", function () {
        // Navigate previous
        $('#smartwizard').smartWizard("prev");
        return true;
    });

    $("#next-btn").on("click", function () {
        // Navigate next
        $('#smartwizard').smartWizard("next");
        return true;
    });

    $("#theme_selector").on("change", function () {
        // Change theme
        $('#smartwizard').smartWizard("theme", $(this).val());
        return true;
    });

    // Set selected theme on page refresh
    $("#theme_selector").change();
});