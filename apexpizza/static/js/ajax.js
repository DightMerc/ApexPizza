//Django basic setup for accepting ajax requests.
// Cookie obtainer Django

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
// Setup ajax connections safetly

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(){
    console.log("Trying to get data");
    $.get("getmytemp/", function(data, status){
        var data1 = JSON.stringify(data, null, 2);
        if (data1.includes("not exsists")){
            console.log("Data: " + data + "\nStatus: " + status);
        } else {
            var obj = JSON.parse(data1)
        }
      });
});

// Submit post on submit
// $('#post-form').on('submit', function(event){
//     console.log(event.target.name)
//     event.preventDefault();
//     console.log("form submitted!")  // sanity check
//     create_post(event);
// });



$('form').on('submit', function(event){
    event.preventDefault();
    
    // console.log("form submitted!")  // sanity check
    create_post(event);

});

$('input').change(function(event){
    if (event.target.name == "size_selector"){
        event.preventDefault();
        change_price(event, "pizzaprice");
    }
    if (event.target.name == "volume_selector"){
        event.preventDefault();
        change_price(event, "drinkprice");
    }
    
});





function change_price(event, name){
    var sender = event.target.id;
    var price = document.getElementById(name + " " + sender.split(" ")[0]);
    price.innerHTML = sender.split(" ")[2] + " сум"
};

// AJAX for posting
function create_post(event) {
    

    var size_selector = $("input[name='size_selector']:checked").val();
    var selector = $("input[name='selector']:checked").val();
    var volume_selector = $("input[name='volume_selector']:checked").val();

    var sender = event.target.name

    if (sender.includes("pizza")) {
        var num = sender.replace("pizza ", "");
        var toppings = [];
        var string = 'toppings'.concat(num);

        var notes = null;
        

        

        

        $.each($("input[name="+string+"]:checked"), function(){            
            toppings.push($(this).val());
        });

        toppings = toppings.join(" ")


        $.ajax({
            url : "temp/"+num+"/", // the endpoint
            type : "POST", // http method
            data : { object : "pizza", toppings : toppings, size : size_selector, type : selector}, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
                var insert_div = document.getElementById("header_cart");
                var e = document.createElement('div');
                e.setAttribute("class", "header-cart-product");
                e.setAttribute("id", 'pizza '+ json.split(" ")[0] +' '+ json.split(" ")[1]);
                
                var pizza_title = document.getElementById("pizza-name " + num).innerText

                e.innerHTML = '<button type="button" class="header-cart-product-remove" id="button_created" onclick="button_clicked(this.id)"><i class="fa fa-times" aria-hidden="true" id="remove pizza '+ json.split(" ")[0] +' '+ json.split(" ")[1] +'"></i></button><h5>'+ pizza_title +'</h5><span>'+ json.split(" ")[2] +', '+ json.split(" ")[3] +'</span><div class="amount-controllers"><button class="amount-remove" type="button" name="button" onclick="change_amount(this.id)" id="minus pizza ' + json.split(" ")[0] + ' ' + json.split(" ")[1] +'"><i class="fa fa-minus"></i></button><input type="text" name="name" value="1" id="input_value pizza ' + json.split(" ")[0]  + '"><button class="amount-add"  type="button" name="button" id="plus pizza ' + json.split(" ")[0] + ' ' + json.split(" ")[1] +'" onclick="change_amount(this.id)"><i class="fa fa-plus"></i></button></div>';
                insert_div.appendChild(e);
                document.getElementById("cart_cost").hidden=true;
                var cost = document.getElementById("cart_cost");
                insert_div.appendChild(cost);

                amount_general = parseInt(document.getElementById("cart_ammount").textContent) + 1
                document.getElementById("cart_ammount").textContent = amount_general
                document.getElementById("mobile_amount").textContent = amount_general

                

            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });

        
    } else if (sender.includes("drink")) {
        var num = sender.replace("drink ", "");
        
        $.ajax({
            url : "temp/"+num+"/", // the endpoint
            type : "POST", // http method
            data : { object : "drink",  volume : volume_selector}, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check

                var insert_div = document.getElementById("header_cart");
                var e = document.createElement('div');
                e.setAttribute("class", "header-cart-product");
                e.setAttribute("id", 'drink '+ json.split(" ")[0] +' '+ json.split(" ")[1]);

                var drink_title = document.getElementById("drinks-name " + num).innerText

                e.innerHTML = '<button type="button" class="header-cart-product-remove" id="button_created" onclick="button_clicked(this.id)"><i class="fa fa-times" aria-hidden="true" id="remove drink '+ json.split(" ")[0] +' '+ json.split(" ")[1] +'"></i></button><h5>'+ drink_title +'</h5><div class="amount-controllers"><button class="amount-remove" type="button" name="button" onclick="change_amount(this.id)" id="minus drink ' + json.split(" ")[0] + ' ' + json.split(" ")[1] +'"><i class="fa fa-minus"></i></button><input type="text" name="name" value="1" id="input_value drink ' + json.split(" ")[0]  + '"><button class="amount-add" type="button" name="button" onclick="change_amount(this.id)" id="plus drink ' + json.split(" ")[0] + ' ' + json.split(" ")[1] +'"><i class="fa fa-plus"></i></button></div>';
                insert_div.appendChild(e);
                document.getElementById("cart_cost").hidden=true;
                var cost = document.getElementById("cart_cost");
                insert_div.appendChild(cost);

                amount_general = parseInt(document.getElementById("cart_ammount").textContent) + 1
                document.getElementById("cart_ammount").textContent = amount_general
                document.getElementById("mobile_amount").textContent = amount_general
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }  else if (sender.includes("snack")) {
        var num = sender.replace("snack ", "");
        
        $.ajax({
            url : "temp/"+num+"/", // the endpoint
            type : "POST", // http method
            data : { object : "snack"}, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check

                var insert_div = document.getElementById("header_cart");
                var e = document.createElement('div');
                e.setAttribute("class", "header-cart-product");
                e.setAttribute("id", 'snack '+ json.split(" ")[0] +' '+ json.split(" ")[1]);

                var snack_title = document.getElementById("snacks-name " + num).innerText


                e.innerHTML = '<button type="button" class="header-cart-product-remove" id="button_created" onclick="button_clicked(this.id)"><i class="fa fa-times" aria-hidden="true" id="remove snack '+ json.split(" ")[0] +' '+ json.split(" ")[1] +'"></i></button><h5>' + snack_title + '</h5><div class="amount-controllers"><button class="amount-remove" type="button" name="button" onclick="change_amount(this.id)" id="minus snack ' + json.split(" ")[0] + ' ' + json.split(" ")[1] +'"><i class="fa fa-minus"></i></button><input type="text" name="name" value="1" id="input_value snack ' + json.split(" ")[0]  + '"><button class="amount-add" type="button" onclick="change_amount(this.id)" name="button" id="plus snack ' + json.split(" ")[0] + ' ' + json.split(" ")[1] +'"><i class="fa fa-plus"></i></button></div>';
                insert_div.appendChild(e);
                document.getElementById("cart_cost").hidden=true;
                var cost = document.getElementById("cart_cost");
                insert_div.appendChild(cost);

                amount_general = parseInt(document.getElementById("cart_ammount").textContent) + 1
                document.getElementById("cart_ammount").textContent = amount_general
                document.getElementById("mobile_amount").textContent = amount_general
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    } else if (sender.includes("sauce")) {
        var num = sender.replace("sauce ", "");
        
        $.ajax({
            url : "temp/"+num+"/", // the endpoint
            type : "POST", // http method
            data : { object : "sauce"}, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check

                var insert_div = document.getElementById("header_cart");
                var e = document.createElement('div');
                e.setAttribute("class", "header-cart-product");
                e.setAttribute("id", 'sauce '+ json.split(" ")[0] +' '+ json.split(" ")[1]);

                var sauce_title = document.getElementById("sauces-name " + num).innerText


                e.innerHTML = '<button type="button" class="header-cart-product-remove" id="button_created" onclick="button_clicked(this.id)"><i class="fa fa-times" aria-hidden="true" id="remove sauce '+ json.split(" ")[0] +' '+ json.split(" ")[1] +'"></i></button><h5>' + sauce_title + '</h5><div class="amount-controllers"><button class="amount-remove" onclick="change_amount(this.id)" type="button" name="button" id="minus sauce ' + json.split(" ")[0] + ' ' + json.split(" ")[1] +'"><i class="fa fa-minus"></i></button><input type="text" name="name" value="1" id="input_value sauce ' + json.split(" ")[0]  + '"><button class="amount-add" type="button"  onclick="change_amount(this.id)" name="button" id="plus sauce ' + json.split(" ")[0] + ' ' + json.split(" ")[1] +'"><i class="fa fa-plus"></i></button></div>';
                insert_div.appendChild(e);
                document.getElementById("cart_cost").hidden=true;
                var cost = document.getElementById("cart_cost");
                insert_div.appendChild(cost);

                amount_general = parseInt(document.getElementById("cart_ammount").textContent) + 1
                document.getElementById("cart_ammount").textContent = amount_general
                document.getElementById("mobile_amount").textContent = amount_general
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        
    } else if (sender.includes("set")) {
        var num = sender.replace("set ", "");
        
        $.ajax({
            url : "temp/"+num+"/", // the endpoint
            type : "POST", // http method
            data : { object : "set"}, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check

                var insert_div = document.getElementById("header_cart");
                var e = document.createElement('div');
                e.setAttribute("class", "header-cart-product");
                e.setAttribute("id", 'set '+ json.split(" ")[0] +' '+ json.split(" ")[1]);

                var set_title = document.getElementById("sets-name " + num).innerText


                e.innerHTML = '<button type="button" class="header-cart-product-remove" id="button_created" onclick="button_clicked(this.id)"><i class="fa fa-times" aria-hidden="true" id="remove set '+ json.split(" ")[0] +' '+ json.split(" ")[1] +'"></i></button><h5>' + set_title + '</h5><div class="amount-controllers"><button class="amount-remove" onclick="change_amount(this.id)" type="button" name="button" id="minus set ' + json.split(" ")[0] + ' ' + json.split(" ")[1] +'"><i class="fa fa-minus"></i></button><input type="text" name="name" value="1" id="input_value set ' + json.split(" ")[0]  + '"><button class="amount-add" onclick="change_amount(this.id)" type="button" name="button" id="plus set ' + json.split(" ")[0] + ' ' + json.split(" ")[1] +'"><i class="fa fa-plus"></i></button></div>';
                insert_div.appendChild(e);
                document.getElementById("cart_cost").hidden=true;
                var cost = document.getElementById("cart_cost");
                insert_div.appendChild(cost);

                amount_general = parseInt(document.getElementById("cart_ammount").textContent) + 1
                document.getElementById("cart_ammount").textContent = amount_general
                document.getElementById("mobile_amount").textContent = amount_general
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        
    }


};

$("button").click(function(event){
    var sender = event.target.id
    console.log(sender)
    button_clicked(sender)
    
  });

function button_clicked(sender){
    if (sender === "button_created"){
        var sender = document.getElementById(sender).childNodes[0].id
        console.log(sender)
    }
    if (sender.includes("remove")){
        if (sender.includes("pizza")){
            var father = document.getElementById(sender.replace("remove ", ""));
            if (sender.includes("cart")){
                father.parentNode.removeChild(father);

                var father = document.getElementById(sender.replace("remove ", "").replace(" cart", ""));
                father.parentNode.removeChild(father);

            } else {

                father.parentNode.removeChild(father);
                if (document.getElementById(sender.replace("remove ", "") + " cart")!==NaN){

                    var father = document.getElementById(sender.replace("remove ", "") + " cart");
                    console.log(father)

                    father.parentNode.removeChild(father);
                }
                
            }
            


            var pizza_num = sender.split(" ")[2]
            var order_num = sender.split(" ")[3]

            $.ajax({
            url : "remove/", // the endpoint
            type : "POST", // http method
            data : { object : "pizza", number : pizza_num, order_number : order_num}, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                var amount_general = parseInt(document.getElementById("cart_ammount").textContent) - 1;
                document.getElementById("cart_ammount").textContent = amount_general;
                document.getElementById("mobile_amount").textContent = amount_general;
                //console.log(json); // log the returned json to the console
                //console.log("success"); // another sanity check
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        }   else if (sender.includes("drink")){

            var father = document.getElementById(sender.replace("remove ", ""));
            if (sender.includes("cart")){
                father.parentNode.removeChild(father);

                var father = document.getElementById(sender.replace("remove ", "").replace(" cart", ""));
                father.parentNode.removeChild(father);

            } else {

                father.parentNode.removeChild(father);
                if (document.getElementById(sender.replace("remove ", "") + " cart")!==NaN){

                    var father = document.getElementById(sender.replace("remove ", "") + " cart");
                    console.log(father)

                    father.parentNode.removeChild(father);
                }
                
            }


            var drink_num = sender.split(" ")[2]
            var order_num = sender.split(" ")[3]

            $.ajax({
            url : "remove/", // the endpoint
            type : "POST", // http method
            data : { object : "drink", number : drink_num, order_number : order_num}, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
                var amount_general = parseInt(document.getElementById("cart_ammount").textContent) - 1;
                document.getElementById("cart_ammount").textContent = amount_general;
                document.getElementById("mobile_amount").textContent = amount_general;
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        }   else if (sender.includes("snack")){
            var father = document.getElementById(sender.replace("remove ", ""));
            if (sender.includes("cart")){
                father.parentNode.removeChild(father);

                var father = document.getElementById(sender.replace("remove ", "").replace(" cart", ""));
                father.parentNode.removeChild(father);

            } else {

                father.parentNode.removeChild(father);
                if (document.getElementById(sender.replace("remove ", "") + " cart")!==NaN){

                    var father = document.getElementById(sender.replace("remove ", "") + " cart");
                    console.log(father)

                    father.parentNode.removeChild(father);
                }
                
            }
            

            var snack_num = sender.split(" ")[2]
            var order_num = sender.split(" ")[3]
            

            $.ajax({
            url : "remove/", // the endpoint
            type : "POST", // http method
            data : { object : "snack", number : snack_num, order_number : order_num}, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
                var amount_general = parseInt(document.getElementById("cart_ammount").textContent) - 1;
                document.getElementById("cart_ammount").textContent = amount_general;
                document.getElementById("mobile_amount").textContent = amount_general;
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        }   else if (sender.includes("sauce")){
            var father = document.getElementById(sender.replace("remove ", ""));
            if (sender.includes("cart")){
                father.parentNode.removeChild(father);

                var father = document.getElementById(sender.replace("remove ", "").replace(" cart", ""));
                father.parentNode.removeChild(father);

            } else {

                father.parentNode.removeChild(father);
                if (document.getElementById(sender.replace("remove ", "") + " cart")!==NaN){

                    var father = document.getElementById(sender.replace("remove ", "") + " cart");
                    console.log(father)

                    father.parentNode.removeChild(father);
                }
                
            }

            var sauce_num = sender.split(" ")[2]
            var order_num = sender.split(" ")[3]

            $.ajax({
            url : "remove/", // the endpoint
            type : "POST", // http method
            data : { object : "sauce", number : sauce_num, order_number : order_num}, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
                var amount_general = parseInt(document.getElementById("cart_ammount").textContent) - 1;
                document.getElementById("cart_ammount").textContent = amount_general;
                document.getElementById("mobile_amount").textContent = amount_general;
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        }   else if (sender.includes("set")){
            var father = document.getElementById(sender.replace("remove ", ""));
            if (sender.includes("cart")){
                father.parentNode.removeChild(father);

                var father = document.getElementById(sender.replace("remove ", "").replace(" cart", ""));
                father.parentNode.removeChild(father);

            } else {

                father.parentNode.removeChild(father);
                if (document.getElementById(sender.replace("remove ", "") + " cart")!==NaN){

                    var father = document.getElementById(sender.replace("remove ", "") + " cart");
                    console.log(father)

                    father.parentNode.removeChild(father);
                }
                
            }
            
            var set_num = sender.split(" ")[2]
            var order_num = sender.split(" ")[3]

            $.ajax({
            url : "remove/", // the endpoint
            type : "POST", // http method
            data : { object : "set", number : set_num, order_number : order_num}, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
                var amount_general = parseInt(document.getElementById("cart_ammount").textContent) - 1;
                document.getElementById("cart_ammount").textContent = amount_general;
                document.getElementById("mobile_amount").textContent = amount_general;
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        } else if (sender.includes("present")){
            var father = document.getElementById(sender.replace("remove ", ""));
            if (sender.includes("cart")){
                father.parentNode.removeChild(father);

                var father = document.getElementById(sender.replace("remove ", "").replace(" cart", ""));
                father.parentNode.removeChild(father);

            } else {

                father.parentNode.removeChild(father);
                if (document.getElementById(sender.replace("remove ", "") + " cart")!==NaN){

                    var father = document.getElementById(sender.replace("remove ", "") + " cart");
                    console.log(father)

                    father.parentNode.removeChild(father);
                }
                
            }
            
            
            var present_num = sender.split(" ")[2]
            var order_num = sender.split(" ")[3]

            $.ajax({
            url : "remove/", // the endpoint
            type : "POST", // http method
            data : { object : "present", number : present_num, order_number : order_num}, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
                var amount_general = parseInt(document.getElementById("cart_ammount").textContent) - 1;
                document.getElementById("cart_ammount").textContent = amount_general;
                document.getElementById("mobile_amount").textContent = amount_general;
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        }
        
    } else if (sender.includes("cart_drinks")){
        var num = sender.replace("cart_drinks ", "");
        
        $.ajax({
            url : "temp/"+num+"/", // the endpoint
            type : "POST", // http method
            data : { object : "drink",  volume : "3"}, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check

                var insert_div = document.getElementById("header_cart");
                var e = document.createElement('div');
                e.setAttribute("class", "header-cart-product");
                e.setAttribute("id", 'drink '+ json.split(" ")[0] +' '+ json.split(" ")[1]);

                var drink_title = document.getElementById("drinks-name " + num).innerText

                e.innerHTML = '<button type="button" class="header-cart-product-remove" id="button_created" onclick="button_clicked(this.id)"><i class="fa fa-times" aria-hidden="true" id="remove drink '+ json.split(" ")[0] +' '+ json.split(" ")[1] +'"></i></button><h5>'+ drink_title +'</h5><div class="amount-controllers"><button class="amount-remove" type="button" name="button" onclick="change_amount(this.id)" id="minus drink ' + json.split(" ")[0] + ' ' + json.split(" ")[1] +'"><i class="fa fa-minus"></i></button><input type="text" name="name" value="1" id="input_value drink ' + json.split(" ")[0]  + '"><button class="amount-add" type="button" name="button" onclick="change_amount(this.id)" id="plus drink ' + json.split(" ")[0] + ' ' + json.split(" ")[1] +'"><i class="fa fa-plus"></i></button></div>';
                insert_div.appendChild(e);
                document.getElementById("cart_cost").hidden=true;
                var cost = document.getElementById("cart_cost");
                insert_div.appendChild(cost);

                var insert_div = document.getElementById("cart_wrapper");
                var e = document.createElement('div');
                e.setAttribute("class", "cart-card");
                e.setAttribute("id", 'drink '+ json.split(" ")[0] +' '+ json.split(" ")[1] + ' cart');

                var drink_title = document.getElementById("drinks-name " + num).innerText
                var drink_price = document.getElementById("drinks-name " + num + " cart").innerText

                e.innerHTML = '<div class="cart-card-name"> <h4>'+drink_title+'</h4> </div> <div class="cart-card-actions"> <div class="cart-card-quantities"> <form id="cart drink '+json.split(" ")[0] +' '+ json.split(" ")[1]+'" method="POST" action="#" > <input type="button" value="-"" class="qtyminus" id="action - '+json.split(" ")[0] +' '+ json.split(" ")[1]+'" onclick="button_clicked1(this)" field="quantity"> <input type="text" name="quantity" value="1" class="qty" id="quantity drink '+ json.split(" ")[0] + ' ' + json.split(" ")[1] +'"> <input type="button" value="+" class="qtyplus" id="action + '+json.split(" ")[0] +' '+ json.split(" ")[1]+'" onclick="button_clicked1(this)" field="quantity"> </form> </div> <div class="cart-card-price"> '+ drink_price +'</div> <button class="cart-card-delete-btn" ><i class="fa fa-close" onclick="button_clicked(this.id)" id="remove drink '+ json.split(" ")[0] + ' ' + json.split(" ")[1] +' cart"></i></button> </div>';
                insert_div.appendChild(e);

                
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    } else if (sender.includes("cart_sauces")){
        var num = sender.replace("cart_sauces ", "");
        
        $.ajax({
            url : "temp/"+num+"/", // the endpoint
            type : "POST", // http method
            data : { object : "sauce"}, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
                var insert_div = document.getElementById("header_cart");
                var e = document.createElement('div');
                e.setAttribute("class", "header-cart-product");
                e.setAttribute("id", 'sauce '+ json.split(" ")[0] +' '+ json.split(" ")[1]);

                var title = document.getElementById("sauces-name " + num).innerText

                e.innerHTML = '<button type="button" class="header-cart-product-remove" id="button_created" onclick="button_clicked(this.id)"><i class="fa fa-times" aria-hidden="true" id="remove sauce '+ json.split(" ")[0] +' '+ json.split(" ")[1] +'"></i></button><h5>'+ title +'</h5><div class="amount-controllers"><button class="amount-remove" type="button" name="button" onclick="change_amount(this.id)" id="minus sauce ' + json.split(" ")[0] + ' ' + json.split(" ")[1] +'"><i class="fa fa-minus"></i></button><input type="text" name="name" value="1" id="input_value sauce ' + json.split(" ")[0]  + '"><button class="amount-add" type="button" name="button" onclick="change_amount(this.id)" id="plus sauce ' + json.split(" ")[0] + ' ' + json.split(" ")[1] +'"><i class="fa fa-plus"></i></button></div>';
                insert_div.appendChild(e);
                document.getElementById("cart_cost").hidden=true;
                var cost = document.getElementById("cart_cost");
                insert_div.appendChild(cost);

                var insert_div = document.getElementById("cart_wrapper");
                var e = document.createElement('div');
                e.setAttribute("class", "cart-card");
                e.setAttribute("id", 'sauce '+ json.split(" ")[0] +' '+ json.split(" ")[1] + ' cart');

                var title = document.getElementById("sauces-name " + num).innerText
                var price = document.getElementById("sauces-name " + num + " cart").innerText

                e.innerHTML = '<div class="cart-card-name"> <h4>'+title+'</h4> </div> <div class="cart-card-actions"> <div class="cart-card-quantities"> <form id="cart sauce '+json.split(" ")[0] +' '+ json.split(" ")[1]+'" method="POST" action="#" > <input type="button" value="-"" class="qtyminus" id="action - '+json.split(" ")[0] +' '+ json.split(" ")[1]+'" onclick="button_clicked1(this)" field="quantity"> <input type="text" name="quantity" value="1" class="qty" id="quantity sauce '+ json.split(" ")[0] + ' ' + json.split(" ")[1] +'"> <input type="button" value="+" class="qtyplus" id="action + '+json.split(" ")[0] +' '+ json.split(" ")[1]+'" onclick="button_clicked1(this)" field="quantity"> </form> </div> <div class="cart-card-price"> '+ price +'</div> <button class="cart-card-delete-btn" ><i class="fa fa-close" id="remove sauce '+ json.split(" ")[0] + ' ' + json.split(" ")[1] +' cart"></i></button> </div>';
                insert_div.appendChild(e);

                
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    } else if (sender.includes("order_btn")){
        name = document.getElementById("order_name").value;
        phone = document.getElementById("order_phone").value;
        place = document.getElementById("order_place").value;
        info = document.getElementById("order_info").value;
        $.ajax({
            url : "new_order/", // the endpoint
            type : "POST", // http method
            

            data : { name : name, phone : phone, place : place, info : info}, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
                

                
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }
};

function button_clicked1(sender){
    if (sender.id.includes("action")){

        var action = sender.id.replace("action ")
        if (action.includes("-")){
            sender = document.getElementById(sender.id)
            console.log(sender)
            minusik(sender)
        } else {
            sender = document.getElementById(sender.id)
            console.log(sender)
            plusik(sender)
        }
    }

}


function change_amount(sender, type){
            operation = sender.split(" ")[0]
            object = sender.split(" ")[1]
            number = sender.split(" ")[2]
            order_num = sender.split(" ")[3]

            $.ajax({
                url : "change_amount/", // the endpoint
                type : "POST", // http method
                data : { object : object, operation : operation, number : number, order_number : order_num}, // data sent with the post request
    
                // handle a successful response
                success : function(json) {
                    $('#post-text').val(''); // remove the value from the input
                    console.log(json); // log the returned json to the console
                    console.log("success"); // another sanity check

                    if (operation === "minus"){
                        var amount_general = parseInt(document.getElementById("cart_ammount").textContent) - 1;
                    } else {
                        var amount_general = parseInt(document.getElementById("cart_ammount").textContent) + 1;
                    }
                    document.getElementById("cart_ammount").textContent = amount_general;
                    document.getElementById("mobile_amount").textContent = amount_general;
                    document.getElementById("cart_price").textContent = json.split(" ")[1];

                    if (type){

                    } else {
                        if (json.includes("removed")){
                            var father = document.getElementById(sender.replace(operation + " ",""));

                            father.parentNode.removeChild(father);

                            if (document.getElementById(sender.replace(operation + " ","") + " cart")!==NaN){
                                var father = document.getElementById(sender.replace(operation + " ","") + " cart");
                                father.parentNode.removeChild(father);
                            }

                            document.getElementById("cart_price").textContent = json.split(" ")[1];


                            
                        } else{
                            document.getElementById("input_value " + object  + " " + number).value = json.split(" ")[0];
                            var father = document.getElementById(sender.replace(operation + " ",""));
                            
                            
                            console.log(json.split(" ")[1]);
                        }
                    }

                },
    
                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
        }

            )
};