$(document).ready(function () {
    $('.basic-ladda-button').on('click', function (e) {
        var laddaBtn = e.currentTarget;
        var l = Ladda.create(laddaBtn);
        l.start();
        setTimeout(function () {
            l.stop();
        }, 3000);
    });

    $('.example-button').on('click', function (e) {
        var laddaBtn = e.currentTarget;
        var l = Ladda.create(laddaBtn);
        l.start();
        setTimeout(function () {
            l.stop();
        }, 3000)
    });

    // personnalisation
    // login

    $('#login-submit').on('click', function (e) {
        var laddaBtn = e.currentTarget;
        var l = Ladda.create(laddaBtn);
        var state = true;
        e.preventDefault();
        e.stopPropagation();
        //alert('pass')
        l.start();
        var ev2 = document.querySelector("#login-form");
        var validation = Array.prototype.filter.call(ev2, function (form) {
            if (ev2.checkValidity() === false) {
                state = false;
                e.preventDefault();
                e.stopPropagation();
            }
            ev2.classList.add('was-validated');
        });
        if (state) {
            //alert('pass')
            var url = $('#login-form').attr('data');
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    username: $('#username').val(),
                    password: $('#password').val(),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                //dataType: 'json',
                success: function (data) {
                    toastr.success("", data, {
                        showMethod: "slideDown",
                        hideMethod: "slideUp",
                        timeOut: 2e3,
                        progressBar: !0
                    })
                    ev2.classList.remove('was-validated');
                    l.stop();
                    if(data == 'Connexion successfully'){
                        var link = $('#login-form').attr('data-home');
                            window.location.href = link;
                    }
                }
            })

        } else {
            toastr.error("Erreur Formulaire", "Tous les champs requis n'ont pas ete rempli", {
                showMethod: "slideDown",
                hideMethod: "slideUp",
                timeOut: 2e3,
                progressBar: !0
            })
            setTimeout(function () {
                l.stop();
            }, 2000);
        }
    });

    // Register trouveur

    $('#register-trouveur-submit').on('click', function (e) {
        var laddaBtn = e.currentTarget;
        var l = Ladda.create(laddaBtn);
        var state = true;
        e.preventDefault();
        e.stopPropagation();
        //alert('pass')
        l.start();
        var ev2 = document.querySelector("#register-trouveur-form");
        var validation = Array.prototype.filter.call(ev2, function (form) {
            if (ev2.checkValidity() === false) {
                state = false;
                e.preventDefault();
                e.stopPropagation();
            }
            ev2.classList.add('was-validated');
        });
        if (state) {
            if($('#password').val() != $('#repassword').val() || $('#birthdate').val() == ''){
                toastr.error("Erreur Formulaire", "Veuillez verifiez que les mots de passe sont identiques et que vous avez entre la date de naissance", {
                    showMethod: "slideDown",
                    hideMethod: "slideUp",
                    timeOut: 2e3,
                    progressBar: !0
                })
                l.stop();
            }else {
                var url = $('#register-trouveur-form').attr('data');
                var picker = $('#birthdate').pickadate('picker');
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    nom_prop: $('#lastname').val(),
                    prenom_prop: $('#firstname').val(),
                    telephone: $('#phone').val(),
                    password: $('#password').val(),
                    date_naissance: picker.get('select', 'yyyy-mm-dd'),
                    lieu_residence: $('#lieu_residence').val(),
                    profession: $('#profession').val(),
                    email: $('#email').val(),
                    cni: $('#cni_number').val(),
                    date_delivrance: $('#date_delivrance').val(),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                //dataType: 'json',
                success: function (data) {
                    toastr.success("", data, {
                        showMethod: "slideDown",
                        hideMethod: "slideUp",
                        timeOut: 2e3,
                        progressBar: !0
                    })
                    ev2.classList.remove('was-validated');
                    l.stop();
                    if(data == 'Register successfully'){
                        var link = $('#register-trouveur-form').attr('data-login');
                            window.location.href = link;
                    }
                }
            })
            }


        } else {
            toastr.error("Erreur Formulaire", "Tous les champs requis n'ont pas ete rempli", {
                showMethod: "slideDown",
                hideMethod: "slideUp",
                timeOut: 2e3,
                progressBar: !0
            })
            setTimeout(function () {
                l.stop();
            }, 2000);
        }
    });

    // Register agence

    $('#register-agence-submit').on('click', function (e) {
        var laddaBtn = e.currentTarget;
        var l = Ladda.create(laddaBtn);
        var state = true;
        e.preventDefault();
        e.stopPropagation();
        //alert('pass')
        l.start();
        var ev2 = document.querySelector("#register-agence-form");
        var validation = Array.prototype.filter.call(ev2, function (form) {
            if (ev2.checkValidity() === false) {
                state = false;
                e.preventDefault();
                e.stopPropagation();
            }
            ev2.classList.add('was-validated');
        });
        if (state) {
            if($('#password').val() != $('#repassword').val()){
                toastr.error("Erreur Formulaire", "Veuillez verifiez que les mots de passe sont identiques !!!", {
                    showMethod: "slideDown",
                    hideMethod: "slideUp",
                    timeOut: 2e3,
                    progressBar: !0
                })
                l.stop();
            }else {
                var url = $('#register-agence-form').attr('data');
                //var picker = $('#birthdate').pickadate('picker');
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    nom_prop: $('#lastname').val(),
                    username: $('#username').val(),
                    telephone: $('#phone').val(),
                    password: $('#password').val(),
                    lieu_residence: $('#localisation').val(),
                    ville: $('#city').val(),
                    email: $('#email').val(),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                //dataType: 'json',
                success: function (data) {
                    toastr.success("", data, {
                        showMethod: "slideDown",
                        hideMethod: "slideUp",
                        timeOut: 2e3,
                        progressBar: !0
                    })
                    ev2.classList.remove('was-validated');
                    l.stop();
                    if(data == 'Register successfully'){
                        var link = $('#register-agence-form').attr('data-login');
                            window.location.href = link;
                    }
                }
            })
            }


        } else {
            toastr.error("Erreur Formulaire", "Tous les champs requis n'ont pas ete rempli", {
                showMethod: "slideDown",
                hideMethod: "slideUp",
                timeOut: 2e3,
                progressBar: !0
            })
            setTimeout(function () {
                l.stop();
            }, 2000);
        }
    });

        // trouveur signqler objet
    $('#obj-found-submit').on('click', function (e) {
        var laddaBtn = e.currentTarget;
        var l = Ladda.create(laddaBtn);
        var state = true;
        //alert('pass')
        l.start();
        var ev2 = document.querySelector("#obj-found-form");
        var validation = Array.prototype.filter.call(ev2, function (form) {
            if (ev2.checkValidity() === false) {
                state = false;
                e.preventDefault();
                e.stopPropagation();
            }
            ev2.classList.add('was-validated');
        });
        if (state) {
            var url = $('#obj-found-form').attr('data');
            //alert($('.description').val())
            if ($('#obj-found-form').attr('data-id') == '') {
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: {
                        type_objet: $('#type_select').val(),
                        autre_type: $('.autre_type').val(),
                        nom_objet: $('.nom_objet').val(),
                        nom_prop: $('.nom_prop').val(),
                        prenom_prop: $('.prenom_prop').val(),
                        id_objet: $('.id_obj').val(),
                        lieu_trouver: $('.lieu_trouver').val(),
                        description: $('.description').val(),
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    },
                    //dataType: 'json',
                    success: function (data) {
                        toastr.success("", data, {
                            showMethod: "slideDown",
                            hideMethod: "slideUp",
                            timeOut: 2e3,
                            progressBar: !0
                        })
                        init_form();
                        ev2.classList.remove('was-validated');
                        l.stop();
                    }
                })
            } else {
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: {
                        id: $('#obj-found-form').attr('data-id'),
                        type_objet: $('#type_select').val(),
                        autre_type: $('.autre_type').val(),
                        nom_objet: $('.nom_objet').val(),
                        nom_prop: $('.nom_prop').val(),
                        prenom_prop: $('.prenom_prop').val(),
                        id_objet: $('.id_obj').val(),
                        lieu_trouver: $('.lieu_trouver').val(),
                        description: $('.description').val(),
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    },
                    //dataType: 'json',
                    success: function (data) {
                        toastr.success("", data, {
                            showMethod: "slideDown",
                            hideMethod: "slideUp",
                            timeOut: 2e3,
                            progressBar: !0
                        })
                        init_form();
                        ev2.classList.remove('was-validated');
                        l.stop();
                    }
                })
            }

        } else {
            toastr.error("Erreur Formulaire", "Tous les champs requis n'ont pas ete rempli", {
                showMethod: "slideDown",
                hideMethod: "slideUp",
                timeOut: 2e3,
                progressBar: !0
            })
            setTimeout(function () {
                l.stop();
            }, 2000);
        }
        //ev2.addEventListener('submit', submit(e, ev2, l), false);
        //'use strict';
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        /*var forms = document.getElementsByClassName('needs-validation');
        console.log(forms)
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {

        });*/
        /*setTimeout(function() {
            l.stop();
        }, 3000)*/
    });

    //customer

    $('#customer-submit').on('click', function (e) {
        var laddaBtn = e.currentTarget;
        var l = Ladda.create(laddaBtn);
        l.start();
        var ev2 = document.querySelector("#customer-form");
        ev2.addEventListener('submit', submit_customer(e, ev2, l), false);
    });

    function submit_customer(event, ev2, l) {
        //form.replaceWith($('#command-submit').clone());
        var datebrd = $('.birthday').val();
        var url = $('#customer-form').attr('data');
        if (ev2.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
            if (datebrd == '') {
                $('.invalid-feedback-date').show();
            } else {
                $('.invalid-feedback-date').hide();
            }
            l.stop();
        } else {
            //alert(datebrd);

            if (datebrd == '') {
                event.preventDefault();
                event.stopPropagation();
                //alert('date')
                $('.invalid-feedback-date').show();
                l.stop();
            } else {
                $('.invalid-feedback-date').hide();
                event.preventDefault();
                event.stopPropagation();
                if ($('#customer-form').attr("data-id") == '') {
                    // adding command
                    var picker = $('.birthday').pickadate('picker');
                    $.ajax({
                        type: 'POST',
                        url: url,
                        data: {
                            customer_birthday_date: picker.get('select', 'yyyy-mm-dd'),
                            customer_name: $('.name').val(),
                            customer_surname: $('.surname').val(),
                            customer_cni: $('.cni').val(),
                            customer_email: $('.email').val(),
                            customer_phone1: $('.phone1').val(),
                            customer_phone2: $('.phone2').val(),
                            customer_phone_payment: $('.payment').val(),
                            customer_bank: $('.bank').val(),
                            customer_bank_account: $('.account').val(),
                            customer_sex: $('.sex').val(),
                            customer_job: $('.job').val(),
                            customer_city: $('.city').val(),
                            customer_address: $('.address').val(),
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                        },
                        success: function (response) {
                            toastr.success("", response, {
                                showMethod: "slideDown",
                                hideMethod: "slideUp",
                                timeOut: 2e3,
                                progressBar: !0
                            })
                            ev2.removeEventListener("submit", submit_customer, false);
                            var url1 = $('#tab_bcustomer').attr('data-get');
                            $.ajax({
                                url: url1,
                                success: function (response) {
                                    //console.log(response)
                                    var url = $('#tab_bcustomer').attr('data-add');
                                    //$('#tab_bcustomer').empty();
                                    var t = $('#zero_configuration_table_customer').DataTable();
                                    t.clear().draw();
                                    for (var key in response.customers) {

                                        t.row.add([
                                            response.customers[key].nom_client,
                                            response.customers[key].prenom_client,
                                            response.customers[key].sexe,
                                            response.customers[key].date_naissance,
                                            response.customers[key].numero_cni,
                                            response.customers[key].telephone1,
                                            response.customers[key].telephone2,
                                            response.customers[key].telephone_paiement,
                                            response.customers[key].banque,
                                            response.customers[key].numero_compte_bancaire,
                                            response.customers[key].profession,
                                            response.customers[key].quartier,
                                            response.customers[key].ville,
                                            '<a href="' + url + response.customers[key].id + '" type="button" class="btn btn-success" onClick=""><i class="nav-icon i-Pen-2 font-weight-bold"></i></a>'
                                            + '<button class="btn btn-danger delete-cmd alert-confirm" id="delete-cmd-' + response.customers[key].id + '" data="' + response.customers[key].id + '" onClick="deletecmd(' + response.customers[key].id + ')"><i class="nav-icon i-Close-Window font-weight-bold"></i></button>',
                                        ]).node().id = response.customers[key].id;
                                        t.draw(false);
                                    }
                                },
                                error: function (responce) {
                                    alert("An error code")
                                }
                            })
                            l.stop();
                            init_form_customer();
                        }
                    })
                } else {
                    // updating command
                    var picker = $('.birthday').pickadate('picker');
                    $.ajax({
                        type: 'POST',
                        url: url,
                        data: {
                            id: $('#customer-form').attr('data-id'),
                            customer_birthday_date: picker.get('select', 'yyyy-mm-dd'),
                            customer_name: $('.name').val(),
                            customer_surname: $('.surname').val(),
                            customer_cni: $('.cni').val(),
                            customer_email: $('.email').val(),
                            customer_phone1: $('.phone1').val(),
                            customer_phone2: $('.phone2').val(),
                            customer_phone_payment: $('.payment').val(),
                            customer_bank: $('.bank').val(),
                            customer_bank_account: $('.account').val(),
                            customer_sex: $('.sex').val(),
                            customer_job: $('.job').val(),
                            customer_city: $('.city').val(),
                            customer_address: $('.address').val(),
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                        },
                        success: function (response) {
                            toastr.success("", response, {
                                showMethod: "slideDown",
                                hideMethod: "slideUp",
                                timeOut: 2e3,
                                progressBar: !0
                            })
                            ev2.removeEventListener("submit", submit_customer, false);
                            var url1 = $('#tab_bcustomer').attr('data-get');
                            $.ajax({
                                url: url1,
                                success: function (response) {
                                    //console.log(response)
                                    var url = $('#tab_bcustomer').attr('data-add');
                                    //$('#tab_bcustomer').empty();
                                    var t = $('#zero_configuration_table_customer').DataTable();
                                    t.clear().draw();
                                    for (var key in response.customers) {

                                        t.row.add([
                                            response.customers[key].nom_client,
                                            response.customers[key].prenom_client,
                                            response.customers[key].sexe,
                                            response.customers[key].date_naissance,
                                            response.customers[key].numero_cni,
                                            response.customers[key].telephone1 + '-' + response.customers[key].telephone2,
                                            response.customers[key].telephone_paiement,
                                            response.customers[key].banque,
                                            response.customers[key].numero_compte_bancaire,
                                            response.customers[key].profession,
                                            response.customers[key].quartier,
                                            response.customers[key].ville,
                                            '<a href="' + url + response.customers[key].id + '" type="button" class="btn btn-success" onClick=""><i class="nav-icon i-Pen-2 font-weight-bold"></i></a>'
                                            + '<button class="btn btn-danger delete-cmd alert-confirm" id="delete-cmd-' + response.customers[key].id + '" data="' + response.customers[key].id + '" onClick="deletecmd(' + response.customers[key].id + ')"><i class="nav-icon i-Close-Window font-weight-bold"></i></button>',
                                        ]).node().id = response.customers[key].id;
                                        t.draw(false);
                                    }
                                },
                                error: function (responce) {
                                    alert("An error code")
                                }
                            })
                            l.stop();
                            init_form_customer();
                        }
                    })
                }


            }

        }
        ev2.classList.add('was-validated');
        //alert('pass');
    }

    function init_form_customer() {
        $('.birthday').val('');
        $('.name').val('');
        $('.surname').val('');
        $('.cni').val('');
        $('.sex').val('');
        $('.phone1').val('');
        $('.phone2').val('');
        $('.payment').val('');
        $('.bank').val('');
        $('.account').val('');
        $('.job').val('');
        $('.city').val('');
        $('.address').val('');
        $('.email').val('');
    }

    $('#subs-submit').on('click', function (e) {
        var laddaBtn = e.currentTarget;
        var l = Ladda.create(laddaBtn);
        l.start();
        var ev2 = document.querySelector("#subscribe-form");
        ev2.addEventListener('submit', submit_subscribe(e, ev2, l), false);
    });

    function submit_subscribe(event, ev2, l) {
        //form.replaceWith($('#command-submit').clone());
        var datesubs = $('.subscription_date').val();
        var url = $('#subscribe-form').attr('data');
        if (ev2.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
            if (datesubs == '') {
                $('.invalid-feedback-date').show();
            } else {
                $('.invalid-feedback-date').hide();
            }
            l.stop();
        } else {
            //alert(datebrd);

            if (datesubs == '') {
                event.preventDefault();
                event.stopPropagation();
                //alert('date')
                $('.invalid-feedback-date').show();
                l.stop();
            } else {
                $('.invalid-feedback-date').hide();
                event.preventDefault();
                event.stopPropagation();
                var picker = $('.subscription_date').pickadate('picker');
                var picker1 = $('.first_payment_date').pickadate('picker');
                var picker2 = $('.next_payment_date').pickadate('picker');
                var picker3 = $('.last_payment_date').pickadate('picker');
                // id customer
                var text = $('.customer_name').val();
                var matches = text.match(/\[(.*?)\]/);
                var id;
                if (matches) {
                    id = matches[1];
                    //alert(submatch)
                }
                if ($('#subscribe-form').attr("data-id") == '') {
                    // adding subscription
                    $.ajax({
                        type: 'POST',
                        url: url,
                        data: {
                            customer_id: id,
                            subscription_date: picker.get('select', 'yyyy-mm-dd'),
                            amount_subscription: $('.amount_subscription').val(),
                            status_subscription: $('.status_subscription').val(),
                            nbr_payment: $('.nbr_payment').val(),
                            payment_delay: $('.payment_delay').val(),
                            category: $('.category_subscribe').val(),
                            cashout: $('.cashout_subscribe').val(),
                            first_payment_date: picker1.get('select', 'yyyy-mm-dd'),
                            next_payment_date: picker2.get('select', 'yyyy-mm-dd'),
                            last_payment_date: picker3.get('select', 'yyyy-mm-dd'),
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
                            ev2.removeEventListener("submit", submit_subscribe, false);
                            l.stop();
                            var link = $('#subscribe-form').attr('data-detail') + id;
                            window.location.href = link;
                        }
                    })
                } else {
                    // updating subscription

                    $.ajax({
                        type: 'POST',
                        url: url,
                        data: {
                            id: $('#subscribe-form').attr('data-id'),
                            customer_id: id,
                            subscription_date: picker.get('select', 'yyyy-mm-dd'),
                            amount_subscription: $('.amount_subscription').val(),
                            status_subscription: $('.status_subscription').val(),
                            nbr_payment: $('.nbr_payment').val(),
                            payment_delay: $('.payment_delay').val(),
                            category: $('.category_subscribe').val(),
                            cashout: $('.cashout_subscribe').val(),
                            first_payment_date: picker1.get('select', 'yyyy-mm-dd'),
                            next_payment_date: picker2.get('select', 'yyyy-mm-dd'),
                            last_payment_date: picker3.get('select', 'yyyy-mm-dd'),
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                        },
                        success: function (response) {
                            toastr.success("", response, {
                                showMethod: "slideDown",
                                hideMethod: "slideUp",
                                timeOut: 2e3,
                                progressBar: !0
                            })
                            ev2.removeEventListener("submit", submit_subscribe, false);
                            l.stop();
                            var link = $('#subscribe-form').attr('data-detail') + id;
                            window.location.href = link;
                        }
                    })
                }


            }

        }
        ev2.classList.add('was-validated');
        //alert('pass');
    }
});