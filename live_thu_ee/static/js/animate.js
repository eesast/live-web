/**
 * Created by AaronXia on 2016/11/29.
 */


/**
 * Œª÷√¥¶¿Ì
 */

$(function(){
    $(function(){
        var wallHeight = $(window).width()/1920*425 + "px";
        $('#wall-paper').css("height",wallHeight);
        $(window).resize(function(){
            var wallHeight = $(window).width()/1920*425 + "px";
            $('#wall-paper').css("height",wallHeight);
        });
    });

    $(function(){
        var emb = $('div#video_container embed');
        var container = $('#video_container');
        var videoPart = $('div.video_part');
        var videoWidth = emb.width() + "px";
        var videoMargin = -$('#wall-paper').height()*0.16 + "px";
        videoPart.css("marginTop",videoMargin);
        container.css({
            "width":videoWidth
        });

        var mainHeight = videoPart.height()*0.7 + "px";
        $('div.bullet-main-box').css("height",mainHeight);


        var inputHeight = container.height()*0.3 - $('div.totalNumber').height() + "px";
        $('.bullet-input-box').css("height",inputHeight);

    });

    $(function(){
        var Image = $('img.image-area');
        var headWidth = Image.width() + "px";
        Image.css("height",headWidth);

        var sub = $('.comment-submit');
        var subWth = sub.width() + "px";
        sub.css("height",subWth);
    });
});

$(window).resize(function(){
    $(function(){
        var wallHeight = $(window).width()/1920*425 + "px";
        $('#wall-paper').css("height",wallHeight);
        $(window).resize(function(){
            var wallHeight = $(window).width()/1920*425 + "px";
            $('#wall-paper').css("height",wallHeight);
        });
    });

    $(function(){
        var emb = $('div#video_container embed');
        var container = $('#video_container');
        var videoPart = $('div.video_part');
        var videoWidth = emb.width() + "px";
        var videoMargin = -$('#wall-paper').height()*0.16 + "px";
        videoPart.css("marginTop",videoMargin);
        container.css({
            "width":videoWidth
        });

        var mainHeight = videoPart.height()*0.7 + "px";
        $('div.bullet-main-box').css("height",mainHeight);


        var inputHeight = container.height()*0.3 - $('div.totalNumber').height() + "px";
        $('.bullet-input-box').css("height",inputHeight);

    });

    $(function(){
        var Image = $('img.image-area');
        var headWidth = Image.width() + "px";
        Image.css("height",headWidth);

        var sub = $('.comment-submit');
        var subWth = sub.width() + "px";
        sub.css("height",subWth);
    });
});


