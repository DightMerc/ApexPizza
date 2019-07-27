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
            console.log(obj.pizzas[0].title)
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

$("button").click(function(event){
    var sender = event.target.id
    console.log(sender)
    if (sender.includes("remove")){
        if (sender.includes("pizza")){
            var father = document.getElementById(sender.replace("remove ", ""));
            father.hidden=true;

            var pizza_num = sender.split(" ")[2]
            var order_num = sender.split(" ")[3]

            $.ajax({
            url : "remove/", // the endpoint
            type : "POST", // http method
            data : { object : "pizza", number : pizza_num, order_number : order_num}, // data sent with the post request

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
        
    } else if (sender.includes("remove")){
        if (sender.includes("drink")){
            var drink_num = sender.split(" ")[1]
            var order_num = sender.split(" ")[2]

            $.ajax({
            url : "remove/"+num+"/", // the endpoint
            type : "POST", // http method
            data : { object : "drink", number : drink_num, order_number : order_num}, // data sent with the post request

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
        
    } else if (sender.includes("remove")){
        if (sender.includes("snack")){
            var snack_num = sender.split(" ")[1]
            var order_num = sender.split(" ")[2]

            $.ajax({
            url : "remove/"+num+"/", // the endpoint
            type : "POST", // http method
            data : { object : "snack", number : snack_num, order_number : order_num}, // data sent with the post request

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
        
    } else if (sender.includes("remove")){
        if (sender.includes("sauce")){
            var sauce_num = sender.split(" ")[1]
            var order_num = sender.split(" ")[2]

            $.ajax({
            url : "remove/"+num+"/", // the endpoint
            type : "POST", // http method
            data : { object : "sauce", number : sauce_num, order_number : order_num}, // data sent with the post request

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
        
    } else if (sender.includes("remove")){
        if (sender.includes("set")){
            var set_num = sender.split(" ")[1]
            var order_num = sender.split(" ")[2]

            $.ajax({
            url : "remove/"+num+"/", // the endpoint
            type : "POST", // http method
            data : { object : "set", number : set_num, order_number : order_num}, // data sent with the post request

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