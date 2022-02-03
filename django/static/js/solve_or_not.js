$(document).ready(function(event){
    $(document).on('click', '#solved_or_not', function(event){
        event.preventDefault();
        $.ajax({
            type: 'POST', // HTTP通信の種類を指定
            url: "{% url 'main:solved_or_not'%}", // リクエストを送信する先のURLを指定。
            data: {
                'question_id': $(this).attr('name'), // フォームデータを指定。 likeviewで処理される
                'csrfmiddlewaretoken': '{{ csrf_token }}'},
            dataType: 'json', // サーバから返されるデータの型を指定 return JsonResponse(context)
            // 通信成功時に呼ばれるコールバック関数を指定
            success: function(response){
                selector = document.getElementsByName(response.question_id);
                if(response.solved){
                    $(selector).html("解決済み");
                }
                else {
                    $(selector).html("未解決");
                }
            }
        });
    });
});
