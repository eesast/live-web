/**
 * Created by AaronXia on 2016/12/1.
 */

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }
function poll(){
	$.get("poll", function(data,status){
		if (status=='success')
		{
			json=JSON.parse(data);
			console.log("JSON Data: " + str(json.islogin));
		}
		
	});
}

$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
	self.setInterval("poll();",1000);
	
});

$(document).ready(function(){
	$("#bullet-submit").click(function(){
		$.post("danmusubmit",{msg:$("#bullet-input").val()},function(data,status){});
		$("#bullet-input").val("");
	});
});