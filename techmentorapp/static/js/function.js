$(function(){
    var $setElm = $('.address');
    var cutFigure = '25'; // カットする文字数
    var afterTxt = ' …'; // 文字カット後に表示するテキスト
 
    $setElm.each(function(){
        var textLength = $(this).text().length;
        var textTrim = $(this).text().substr(0,(cutFigure))
 
        if(cutFigure < textLength) {
            $(this).html(textTrim + afterTxt).css({visibility:'visible'});
        } else if(cutFigure >= textLength) {
            $(this).css({visibility:'visible'});
        }
    });

    // フッターフォームをajaxで送信
    $('#OpinionIndexForm').submit(function(e) {
        //submitの機能を無効
        e.preventDefault();

        //form要素を取得
        var $form = $(this);

        //送信ボタン要素を取得
        var $button = $form.find('#a_submit');

        //送信
        $.ajax({
            url: $form.attr('action'),
            type: $form.attr('method'),
            data: $form.serialize(),
            timeout: 10000,

            // 送信前
            beforeSend: function(xhr, settings) {
                //ボタンを無効化し、二重送信を防止
                $button.attr('disabled', true);
            },
            // 応答後
            complete: function(xhr, textStatus) {
                // ボタンを有効化し、再送信を許可
                $button.attr('disabled',false);
            },
            // 通信成功時の処理
            success: function(result,textStatus,xhr){
                // 入力値を初期化
                $form[0].reset();

                $('#opinion-result').text('投稿ありがとうございました');
                
            },
            // 通信失敗時の処理
            error: function(xhr,textStatus,error) {
                $('#opinion-result').text('ただいま障害により大変ご迷惑をお掛けしております。');
            }
        });
    });


    // ソート機能をajaxで送信
    $('#sort select').on('change', function() {
        var $form = $('#sort');

        // 送信
        $.ajax({
            url: $form.attr('action'),
            type: $form.attr('method'),
            data: $form.serialize(),
            timeout: 10000,

            // 送信前
            beforeSend: function(xhr, settings) {
                showLoadingImage();
            },
            // 応答後
            complete: function(xhr, textStatus) {
                
            },
            // 通信成功時の処理
            success: function(result,textStatus,xhr){
                $('.searchResultList').html($(result).find('.searchResultList'));
                $.getScript("/js/function.js");
                if( document.getElementById("false") != null  ) {
                    $.getScript("/js/default-mylist.js");
                } else if( document.getElementById("true") != null ) {
                    $.getScript("/js/mylist.js");
                }
                hideLoadingImage();
            },
            // 通信失敗時の処理
            error: function(xhr,textStatus,error) {
                
            }
        }); 
    });

    
    function showLoadingImage() {
        $('.searchResultList').fadeOut(300);
        $("#loader").fadeIn(500);
    }
    
    function hideLoadingImage() {
        $("#loader").fadeOut(300);
        $('.searchResultList').fadeIn(500);
    }

    // トップ文字数制限
    var $set = $('#feature .discText');
    var $title = $('#feature .discTitle');
    var cutTitle = '25'
    var cut = '40'; // カットする文字数
    var after = '…'; // 文字カット後に表示するテキスト
 
    $set.each(function(){
        var textlength = $(this).text().length;
        var texttrim = $(this).text().substr(0,(cut))
 
        if(cut < textlength) {
            $(this).html(texttrim + after).css({visibility:'visible'});
        } else if(cut >= textlength) {
            $(this).css({visibility:'visible'});
        }
    });

    $title.each(function(){
        var textlength = $(this).text().length;
        var texttrim = $(this).text().substr(0,(cutTitle))
 
        if(cutTitle < textlength) {
            $(this).html(texttrim + after).css({visibility:'visible'});
        } else if(cutTitle >= textlength) {
            $(this).css({visibility:'visible'});
        }
    });

    // 詳細ページの類似ページのタイトル文字数制限
    var $similarity = $('.similarity .title');
    var similaritycut = '30'; // カットする文字数
    var similarityafter = '…'; // 文字カット後に表示するテキスト
 
    $similarity.each(function(){
        var similaritylength = $(this).text().length;
        var similaritytrim = $(this).text().substr(0,(similaritycut))
 
        if(similaritycut < similaritylength) {
            $(this).html(similaritytrim + similarityafter).css({visibility:'visible'});
        } else if(similaritycut >= similaritylength) {
            $(this).css({visibility:'visible'});
        }
    });

    var $similarity_name = $('.similarity-name');
    var similarity_namecut = '10'; // カットする文字数
    var similarity_nameafter = '…'; // 文字カット後に表示するテキスト
 
    $similarity_name.each(function(){
        var similarity_namelength = $(this).text().length;
        var similarity_nametrim = $(this).text().substr(0,(similarity_namecut))
 
        if(similarity_namecut < similarity_namelength) {
            $(this).html(similarity_nametrim + similarity_nameafter).css({visibility:'visible'});
        } else if(similarity_namecut >= similarity_namelength) {
            $(this).css({visibility:'visible'});
        }
    });
});