/**
 * Created by AaronXia on 2016/12/1.
 */
var islogin=-1; //0,1

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
			//console.log("islogin: " + json.islogin);  //0,1
			//console.log("pnum: "+ json.pnum);	//#program
			//console.log("status: "+ json.status);	//0 OK, 1 source error, 2 no source
			if (json.danmu.length>0)
			{
				for (i=0;i<json.danmu.length ; i++)
				{
					//danmu_name, danmu_content, danmu_time, danmu_img('' or https://mp.weixin...)
					console.log("msg: " + json.danmu[i].danmu_content + " " + json.danmu[i].danmu_time);
				}
			}
			if (json.comment.length>0)
			{
				for (i=0;i<json.comment.length ; i++)
				{
					//comment_name, comment_content, comment_time, comment_img('' or https://mp.weixin...)
					console.log("comment: " + json.comment[i].comment_content + " " + json.comment[i].comment_time);
				}
			}
			if (json.islogin==1 && islogin==0)
			{
				location.reload();
			}
			if (json.islogin==0 && islogin==1)
			{
				location.reload();
			}
			if (islogin==-1)
			{
				islogin=json.islogin;
			}
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