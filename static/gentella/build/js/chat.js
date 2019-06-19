

var socket = io('http://127.0.0.1:4000');
    socket.on('connect', function(){
	new PNotify({
                    title: 'اتصال موفق',
                    text: 'با موفقیت به سیستم چت متصل شدید.',
                    type: 'success',
                    styling: 'bootstrap3'
                });
});
    socket.on("disconnect",function(){
    	new PNotify({
                    title: 'خطا',
                    text: 'اتصال با سرور چت برقرار نیست.',
                    type: 'error',
                    styling: 'bootstrap3'
                });
	})

var current;
var chatId;
$(".chat-contact").on("click",function () {



    chatId = $(this).attr("data-chatId")
    $(".loading").addClass("running")

    socket.emit("getChats",{"chatId":chatId},function (data) {
        for(var i = 0 ; i < data.length ; i ++){
            if(data[i]["isHelper"]){
            newSelfMessage(data[i]["Text"],data[i]["AddDate"])
        }else{
            newMessage(data[i]["Text"],data[i]["AddDate"])
        }
        }

    })

    $(".loading").removeClass("running")



})

socket.on("client_message",function(data){
	if(data["isHelper"]){
		newSelfMessage( data["message"] ,data["addDate"]);
		document.getElementById(chatId).innerText = "شما: "+data["message"]
	}else{
		newMessage(data["message"],data["addDate"])
        document.getElementById(chatId).innerText = data["message"]
	}

})


$("#send_btn").click(function() {
	var input_val = $("#chat_input").val()
	  if ($.trim(input_val).length>0){
	  	socket.emit("message",{"message":input_val,"ChatId":chatId,"type":"TEXT","isHelper":true})


	  	// newSelfMessage( input_val );
	  }
	  $("#chat_input").focus()
});

function newSelfMessage(message,adddate){
	var msgStyle = "<div class=\"row\"  style=\"margin-right: 1%;margin-top: 3%\">\n" +
        "                                        <div class=\"col-md-6 col-sm-6\">\n" +
        "                                            <div class=\"row chat-bubble-self\" style=\"min-width: 80px\">\n" +
        message +
        "                                                 <div class=\"row\" style=\"padding: 3%;margin-bottom: -6%; margin-right: 2%;color:#b0b0b0; \">\n" +
        adddate +
        "                                                 </div>\n" +
        "                                            </div>\n" +
        "\n" +
        "\n" +
        "                                        </div>\n" +
        "                                    </div>"
$("#msgContent").append(msgStyle)
	$("#chat_input").val('')


var objDiv = document.getElementById("msgContent");
objDiv.scrollTop = objDiv.scrollHeight;
}

function newMessage(message,adddate){
	var msgStyle = "<div class=\"row\" ondblclick=\"openMessageHandler('"+message+"')\" style=\"margin-left: 1%;margin-top: 3%\">\n" +
        "                                        <div class=\"col-md-6 col-sm-6 left\">\n" +
        "\n" +
        "                                            <div class=\"row chat-bubble left\" style=\"min-width: 80px\">\n" +
        "\n" +
        message +
        "                                                <div class=\"row\" style=\"margin: 5%;margin-bottom: -6%; margin-left:-10%;color:#b0b0b0; \">\n" +
        "                                                    <p>"+adddate+"</p>\n" +
        "                                                </div>\n" +
        "\n" +
        "                                            </div>\n" +
        "\n" +
        "\n" +
        "                                        </div>\n" +
        "\n" +
        "                                    </div>"
$("#msgContent").append(msgStyle)
	$("#chat_input").val('')
var objDiv = document.getElementById("msgContent");
objDiv.scrollTop = objDiv.scrollHeight;
}

var question;
var AppId="5c2a861f9cb7fc0c72f8a285"
function openMessageHandler(q){
$(".addmessagehelper").modal('show')
	question = q
}


$(".submitanswer").on("click",function () {
	$(this).addClass("running")
	$('form').parsley().validate()
        if($('form').parsley().isValid()){
        	$.post("addMessageHelp",{"question":question,"answer":$("#answer").val(),"AppId":AppId},function(data, status) {
            jdata = JSON.parse(data)
            console.log(jdata)
            if (jdata["status"] == "ok") {
            	$("#answer").val('')
				$(".addmessagehelper").modal('hide')

                new PNotify({
                    title: 'موفق',
                    text: 'سوال و جواب با موفقیت اضافه شد.',
                    type: 'success',
                    styling: 'bootstrap3'
                });
            }
            else {
                new PNotify({
                    title: 'خطا',
                    text: 'خطایی رخ داده است لطفا مجددا تلاش کنید.',
                    type: 'error',
                    styling: 'bootstrap3'
                });
            }
            $(".submitanswer").removeClass("running")
        })
        }
})


$(window).on('keydown', function(e) {
  if (e.which == 13) {
  	var input_val = $("#chat_input").val()
	  if ($.trim(input_val).length>0){
	  	socket.emit("message",{"message":input_val,"ChatId":chatId,"type":"TEXT","isHelper":true})
          document.getElementById(chatId).innerText = "شما: "+input_val
	  }

    return false;
  }
});
