/**
 * Created by waywc on 2016/11/13.
 */

$(function(){
    var paragraph_now = document.getElementById("now-watching");
    var total_visited = document.getElementById("total-visited");
    var temp = parseFloat(paragraph_now.innerText);
    var tm = parseFloat(total_visited.innerText);
    temp=temp+1;
    tm=tm+1;
    paragraph_now.innerText=temp.toString();
    total_visited.innerText=tm.toString();
});

$(function(){
    var video = $('#video_container');
    var em = $('div#video_container embed');
    var wid = em.width();
    var comment_height = video.height() - $('div.visited-box').height() - 20 + "px";
    video.css({
        width : wid+"px"
    });
    $('#comment-box').css("height",comment_height);
});

$(function(){
    var comment_area = $('#comment-area');
    var hei = comment_area.height();
    $('p.header').click(function(){
        var txt = $('<p></p>').text("asdasdad");
        comment_area.append(txt);
        hei += txt.height();
        comment_area.animate({
            scrollTop: hei
        },0)
    });

    $('#comment').bind('keypress',function(event){
        if(event.keyCode == 13){
            $('#submit').click();
        }
    })
});

