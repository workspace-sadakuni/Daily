'use strict';

function error_message_set(event, error_message){
    /**
    * エラーメッセージ領域を表示する。
    */
    $(event).after(error_message_field)
    $(event).parent().children('.input-error').html(error_message);
    return false;
}

function error_message_reset(event){
    /**
    * エラーメッセージ領域をリセットする。
    */
    $(event).parent().children('.input-error').remove();
}


/*
入力チェック関数域
*/
function check_value_required(event, value){
    /**
    * 入力必須項目の判定をする。
    */
    if(value===""||value==="undefined"){
        error_message_set($(event), error_message_required);
        return false
    }else{
        return true
    }
}

function check_value_length(event, value, max_length, min_length){
    /**
    * 入力可能文字数を判定する。
    */

    if(value.length < min_length){
        error_message_set($(event), min_length+error_message_min_length);
        return false
    }else if(value.length > max_length){
        error_message_set($(event), max_length+error_message_max_length);
        return false
    }else {
        return true
    }
}

function check_value_regex(event, value, regex, error_message){
    /**
    * 入力可能文字を判定する。
    */
    if(value.match(regex)){
        return true
    }else{
        error_message_set(event, error_message);
        return false
    }
}