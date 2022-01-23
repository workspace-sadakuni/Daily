function FoodInputController() {
    // 食事投稿フォームのバリデーションチェックが主の関数

    let input_title = $("#id_title");
    let input_food_name = $("#id_food_name");
    let input_content = $("#id_content");
    let input_ate_at = $("#id_ate_at");

    let input_elements = new Array(input_title, input_food_name, input_content, input_ate_at)
    // バリデーションチェック用に入力フォームにイベントトリガーを追加
    add_trigger(input_elements);

    $(document).on('keyup change', '#id_title, #id_food_name, #id_content, #id_ate_at', function(){
        // 一度エラーメッセージをクリア
        error_message_reset(this);

        let input_value = $(this).val();

        // 入力可能文字をチェック
        let is_result_regex = check_value_regex(this, input_value, regex_input, error_message_regex);
        if(is_result_regex){
            if(this.id === "id_title"){
                let is_result_length = check_value_length(this, input_value, 20, 1);
            }else if(this.id === "id_food_name"){
                let is_result_length = check_value_length(this, input_value, 18, 1);
            }else if(this.id === "id_content"){
                let is_result_length = check_value_length(this, input_value, 120, 0);
            }
        }

        // 必須項目の入力値を取得
        let value_title = document.getElementById("id_title").value;
        let value_food_name = document.getElementById("id_food_name").value;
        let value_ate_at = document.getElementById("id_ate_at").value;
        // バリデーションエラーが存在するか、エラー要素を取得
        let input_errors = $('form').find('.input-error').length;

        // バリデーションチェック結果より投稿ボタンの活性、非活性制御
        if(value_title != "" && value_food_name != "" && value_ate_at != "" && input_errors === 0){
            $('#submit').prop('disabled', '');
        }else{
            $('#submit').attr('disabled', 'disabled');
        }
    });
}

function add_trigger(input_elements){
    for (let i = 0; i < input_elements.length; i++) {
        let input_element = input_elements[i];
        input_element.trigger("keyup");
        input_element.trigger("change");
    }
}
